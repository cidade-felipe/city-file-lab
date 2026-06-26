import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import main


class UploadFileTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        main.Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def tearDown(self):
        main.Base.metadata.drop_all(self.engine)

    def test_reuses_existing_file_when_content_hash_matches(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            first_path = Path(temp_dir) / 'primeiro.txt'
            second_path = Path(temp_dir) / 'segundo.txt'
            first_path.write_bytes(b'mesmo conteudo')
            second_path.write_bytes(b'mesmo conteudo')

            with (
                self.session_factory() as session,
                patch.object(main, 'build_or_load_index_for_file'),
                patch.object(main, 'GROQ_API_KEY', None),
            ):
                first_result = main.upload_file(session, str(first_path))
                second_result = main.upload_file(session, str(second_path))

                self.assertFalse(first_result['duplicado'])
                self.assertTrue(second_result['duplicado'])
                self.assertEqual(first_result['id'], second_result['id'])
                self.assertEqual(session.query(main.Arquivo).count(), 1)

    def test_accepts_different_content_with_the_same_filename(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            first_dir = Path(temp_dir) / 'a'
            second_dir = Path(temp_dir) / 'b'
            first_dir.mkdir()
            second_dir.mkdir()
            first_path = first_dir / 'arquivo.txt'
            second_path = second_dir / 'arquivo.txt'
            first_path.write_bytes(b'conteudo um')
            second_path.write_bytes(b'conteudo dois')

            with (
                self.session_factory() as session,
                patch.object(main, 'build_or_load_index_for_file'),
                patch.object(main, 'GROQ_API_KEY', None),
            ):
                first_result = main.upload_file(session, str(first_path))
                second_result = main.upload_file(session, str(second_path))

                self.assertFalse(first_result['duplicado'])
                self.assertFalse(second_result['duplicado'])
                self.assertNotEqual(first_result['id'], second_result['id'])
                self.assertEqual(session.query(main.Arquivo).count(), 2)

    def test_rejects_unsupported_file_before_database_changes(self):
        with tempfile.NamedTemporaryFile(suffix='.bin') as file:
            with self.session_factory() as session:
                with self.assertRaisesRegex(ValueError, 'não suportado'):
                    main.upload_file(session, file.name)
                self.assertEqual(session.query(main.TipoArquivo).count(), 0)


class ReadOnlySqlTests(unittest.TestCase):
    def test_normalizes_a_single_select(self):
        self.assertEqual(
            main.normalize_read_only_sql('  SELECT 1;  '),
            'SELECT 1',
        )

    def test_rejects_multiple_statements(self):
        with self.assertRaisesRegex(ValueError, 'uma instrução'):
            main.normalize_read_only_sql('SELECT 1; SELECT 2')

    def test_rejects_non_select_statement(self):
        with self.assertRaisesRegex(ValueError, 'SELECT'):
            main.normalize_read_only_sql('DELETE FROM arquivo')


class CustomQueryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        main.Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def tearDown(self):
        main.Base.metadata.drop_all(self.engine)

    def test_exports_and_audits_query_result(self):
        dataframe = pd.DataFrame([{'valor': 1}])
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            self.session_factory() as session,
            patch.object(main, 'RESULT_CONSULTA_DIR', temp_dir),
            patch.object(main, 'read_sql_query_read_only', return_value=dataframe),
        ):
            result = main.execute_custom_query(session, 'SELECT 1 AS valor', 'Teste')

            self.assertEqual(result['linhas'], 1)
            self.assertEqual(result['colunas'], 1)
            self.assertTrue(Path(result['caminho_arquivo']).exists())
            self.assertEqual(session.query(main.ConsultaSQL).count(), 1)
            self.assertEqual(session.query(main.ResultadoConsulta).count(), 1)


class IndexPathTests(unittest.TestCase):
    def test_rejects_index_outside_the_project_index_directory(self):
        outside_path = os.path.join(main.BASE_DIR.parent, 'indice-nao-confiavel')
        with self.assertRaisesRegex(ValueError, 'fora da pasta permitida'):
            main.resolve_safe_index_path(outside_path)


if __name__ == '__main__':
    unittest.main()
