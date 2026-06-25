# Codex - City File Lab

Este documento descreve detalhadamente a arquitetura, o modelo de dados, os fluxos de processamento de informações e a estrutura da interface gráfica do City File Lab. O objetivo do projeto é oferecer um laboratório interativo para análise inteligente de arquivos de diversos formatos (PDF, Word, Excel, CSV, Texto e Markdown) utilizando técnicas de RAG (Retrieval-Augmented Generation), bancos de dados relacionais e IA generativa (via Groq).

---

## 1. Visão Geral e Objetivo de Negócio

O City File Lab foi concebido para centralizar e automatizar a análise de documentos corporativos e técnicos. Ao combinar um banco de dados relacional robusto (PostgreSQL) para armazenamento de metadados e arquivos originais com um mecanismo de busca semântica local (FAISS + HuggingFace) e modelos de linguagem de alto desempenho (Groq), o sistema proporciona:

*   **Ganho de Eficiência Operacional**: Redução drástica do tempo gasto na busca manual de informações em documentos extensos. O usuário interage com os arquivos em linguagem natural.
*   **Mitigação de Riscos e Conformidade**: Rastreabilidade completa de todas as interações. O sistema registra quem perguntou, qual arquivo foi consultado, a resposta gerada e os tempos de execução, permitindo auditoria.
*   **Análise de Dados Integrada**: Possibilidade de executar consultas SQL customizadas para extrair dados analíticos dos arquivos diretamente para planilhas do Excel, facilitando a geração de relatórios estratégicos.

---

## 2. Arquitetura do Sistema

A aplicação adota uma estrutura em camadas para separar a interface com o usuário, a lógica de negócios, a orquestração de IA e a persistência de dados.

```mermaid
graph TD
    subgraph Camada de Apresentação
        GUI[gui.py - Interface Tkinter]
        Term[main.py - Menu de Terminal]
    end

    subgraph Camada de Aplicação e Negócio
        Extrator[Extrator de Conteúdo - PyMuPDF, python-docx, pandas]
        VectorEng[Gerenciador FAISS - sentence-transformers]
        RAGEng[Mecanismo RAG - LangChain + ChatGroq]
    end

    subgraph Camada de Persistência e Armazenamento
        DB[(Banco PostgreSQL - SQLAlchemy)]
        Disco[(Diretório Local - Índices FAISS, Gráficos e Consultas)]
    end

    GUI --> Extrator
    GUI --> VectorEng
    GUI --> RAGEng
    Term --> Extrator
    Term --> VectorEng
    Term --> RAGEng

    Extrator --> DB
    VectorEng --> Disco
    RAGEng --> DB
    RAGEng --> Disco
```

### Componentes Principais

1.  **Interface Gráfica (`gui.py`)**: Interface desktop amigável construída com Tkinter. Ela implementa um fluxo de chat dinâmico utilizando balões customizados e um renderizador HTML (`tkinterweb` com `HtmlFrame`) para exibir as respostas da inteligência artificial formatadas em Markdown (incluindo tabelas e blocos de código).
2.  **Motor Principal (`main.py`)**: Centraliza as definições do banco de dados (modelos do ORM SQLAlchemy), a extração de conteúdo dos arquivos e a orquestração do pipeline RAG. Também contém a lógica para gerar gráficos analíticos estáticos via Matplotlib e exportar tabelas via Pandas.
3.  **Ambiente Vetorial (`indices_faiss/`)**: Pasta local onde são salvos os índices vetoriais de cada arquivo após o processamento. Cada documento possui seu próprio arquivo de índice FAISS, agilizando a busca semântica segmentada e evitando vazamento de dados entre diferentes arquivos.
4.  **Armazenamento de Resultados (`consultas/` e `charts/`)**: Pastas de apoio no disco para gravar arquivos gerados sob demanda (planilhas de consultas SQL customizadas e imagens dos gráficos de estatísticas de uso).

---

## 3. Modelagem do Banco de Dados (PostgreSQL + SQLAlchemy)

O banco de dados armazena desde o binário do arquivo importado até o histórico de perguntas e respostas. Todas as tabelas são gerenciadas via SQLAlchemy ORM.

```mermaid
erDiagram
    tipo_arquivo ||--o{ arquivo : "possui"
    arquivo ||--|| conteudo_extraido : "gera"
    arquivo ||--o{ pergunta : "recebe"
    arquivo ||--o{ log : "registra"
    arquivo ||--|| resumo : "contem"
    conteudo_extraido ||--o{ embedding : "possui"
    pergunta ||--|| resposta_ia : "obtem"
    consulta_sql ||--|| resultado_consulta : "gera"

    tipo_arquivo {
        int id PK
        string nome UK
    }
    arquivo {
        int id PK
        string nome
        int tipo_id FK
        datetime data_upload
        bytea conteudo
        int tamanho
        string hash_sha256
    }
    conteudo_extraido {
        int id PK
        int arquivo_id FK "unique"
        text texto
    }
    embedding {
        int id PK
        int conteudo_id FK
        int num_chunks
        int dim
        string index_path
    }
    pergunta {
        int id PK
        int arquivo_id FK
        text texto
        datetime data
    }
    resposta_ia {
        int id PK
        int pergunta_id FK
        text resposta
        float tempo_execucao
        int tokens_input
        int tokens_output
    }
    resumo {
        int id PK
        int arquivo_id FK "unique"
        text texto
        datetime data
    }
    log {
        int id PK
        int arquivo_id FK "nullable"
        string acao
        text detalhe
        datetime data
    }
    consulta_sql {
        int id PK
        text sql
        text descricao
        datetime data
    }
    resultado_consulta {
        int id PK
        int consulta_id FK "unique"
        string caminho_arquivo
        json dados_json
        int linhas
        int colunas
        datetime data_execucao
    }
```

### Detalhamento das Tabelas

#### `tipo_arquivo`
Cadastro de extensões permitidas no sistema. Prevenida a inserção de formatos não mapeados.
*   `id` (Integer, PK): Identificador único do tipo.
*   `nome` (String, Unique): Nome da extensão do arquivo (ex: 'pdf', 'docx', 'csv', 'xlsx', 'xls', 'txt', 'md').

#### `arquivo`
Tabela central que guarda a cópia física dos arquivos em formato binário, permitindo que a aplicação reconstrua ou re-processe os arquivos sem depender do armazenamento do disco original do usuário.
*   `id` (Integer, PK): Identificador único do arquivo.
*   `nome` (String): Nome original do arquivo importado.
*   `tipo_id` (Integer, FK -> `tipo_arquivo.id`): Relacionamento com o tipo do arquivo.
*   `data_upload` (DateTime): Registro cronológico de inserção no banco.
*   `conteudo` (LargeBinary): Arquivo bruto armazenado como campo binário (bytea).
*   `tamanho` (Integer): Tamanho do arquivo em bytes.
*   `hash_sha256` (String): Hash SHA-256 do arquivo para controle de integridade e prevenção de uploads duplicados.

#### `conteudo_extraido`
Armazena a representação textual limpa extraída do binário.
*   `id` (Integer, PK): Identificador único.
*   `arquivo_id` (Integer, FK -> `arquivo.id`, Unique): Garante relação de 1 para 1 com o arquivo.
*   `texto` (Text): Conteúdo em texto puro extraído.

#### `embedding`
Metadados referentes à vetorização do texto extraído.
*   `id` (Integer, PK): Identificador do embedding.
*   `conteudo_id` (Integer, FK -> `conteudo_extraido.id`): Vinculação direta ao texto.
*   `num_chunks` (Integer): Quantidade de divisões geradas para o RAG.
*   `dim` (Integer): Dimensão do vetor do modelo (384 para o modelo do sentence-transformers utilizado).
*   `index_path` (String): Caminho local do arquivo de índice FAISS correspondente em disco.

#### `resumo`
Resumo automático gerado pela IA ou excerto inicial em caso de ausência de chaves de API.
*   `id` (Integer, PK): Identificador único.
*   `arquivo_id` (Integer, FK -> `arquivo.id`, Unique): Relação 1 para 1 com o arquivo.
*   `texto` (Text): Conteúdo do resumo.
*   `data` (DateTime): Data de geração do resumo.

#### `pergunta`
Registro das perguntas feitas pelo usuário.
*   `id` (Integer, PK): Identificador único da pergunta.
*   `arquivo_id` (Integer, FK -> `arquivo.id`): Qual arquivo foi consultado.
*   `texto` (Text): O texto da pergunta digitada.
*   `data` (DateTime): Data e hora da interação.

#### `resposta_ia`
Guarda as respostas fornecidas pela inteligência artificial e métricas associadas.
*   `id` (Integer, PK): Identificador único da resposta.
*   `pergunta_id` (Integer, FK -> `pergunta.id`): Vinculação direta com a pergunta do usuário.
*   `resposta` (Text): Resposta textual gerada.
*   `tempo_execucao` (Float): Tempo decorrido (em segundos) entre a consulta vetorial e o retorno da LLM.
*   `tokens_input` e `tokens_output` (Integer, Nullable): Reservados para métricas de custos de API (se suportado pelo provedor).

#### `consulta_sql` e `resultado_consulta`
Tabelas destinadas à auditoria e controle de relatórios gerados por meio do módulo de consultas SQL customizadas.
*   `consulta_sql` registra a query SQL executada e sua descrição.
*   `resultado_consulta` guarda o caminho da planilha gerada em disco, a quantidade de linhas e colunas retornadas, além de uma cópia dos dados em formato JSON no banco relacional.

#### `log`
Centraliza o rastreamento de ações do sistema (erros de indexação, uploads duplicados, falhas de API ou exclusões de arquivos).
*   `id` (Integer, PK): Identificador do log.
*   `arquivo_id` (Integer, FK -> `arquivo.id`, Nullable): Arquivo associado ao evento (se houver).
*   `acao` (String): Categoria da ação (ex: 'upload_ok', 'erro_extracao', 'resumo_gerado').
*   `detalhe` (Text): Detalhamento do erro ou sucesso ocorrido.
*   `data` (DateTime): Timestamp do evento.

---

## 4. Pipeline de Processamento e Fluxos de Dados

Esta seção explica a lógica por trás de cada fluxo operacional.

### 4.1. Fluxo de Importação e Extração de Texto

O usuário escolhe um arquivo e o sistema processa os dados em lote.

```mermaid
sequenceDiagram
    participant U as Usuário
    participant G as gui.py
    participant M as main.py
    participant DB as PostgreSQL (SQLAlchemy)

    U->>G: Seleciona arquivo e clica em Upload
    G->>M: upload_file(sess, filepath)
    M->>M: Calcula SHA-256 e infere tipo
    M->>DB: Busca por hash duplicado
    alt Hash já existe no Banco
        DB-->>M: Retorna registro existente
        M-->>G: Alerta de arquivo duplicado
    else Hash não existe no Banco
        M->>DB: Salva binário em "arquivo"
        M->>M: Executa extrator específico (PDF, Word, Excel, CSV, TXT, MD)
        M->>DB: Salva texto em "conteudo_extraido"
        M->>M: Gera resumo (Groq ou offline de 500 chars)
        M->>DB: Salva texto em "resumo" e gera Log no banco
        M-->>G: Confirma upload concluído com ID do registro
    end
```

#### Regras de Extração por Tipo de Arquivo
*   **PDF**: Processado via `PyMuPDF` (`fitz`), iterando por cada página e agrupando o texto cru.
*   **DOCX (Word)**: Processado via `python-docx`, concatenando o conteúdo de todos os parágrafos do documento.
*   **CSV**: Carregado via `pandas` e convertido para uma string CSV padronizada.
*   **XLSX / XLS (Excel)**: Carregado via `pandas`, processando todas as planilhas existentes (abas) no arquivo de forma iterativa, adicionando o prefixo `# Sheet: <nome_da_aba>` e convertendo a tabela em texto CSV.
*   **TXT**: Decodificado diretamente como texto puro UTF-8 (tratando possíveis caracteres inválidos com o modo de escape `ignore`).
*   **MD (Markdown)**: Convertido primeiramente para HTML usando `markdown2` e limpo de tags HTML via expressões regulares para garantir que os embeddings vetoriais processem apenas a informação textual útil.

---

### 4.2. Fluxo de Indexação e Criação de Embeddings

Após a gravação do texto extraído, o sistema inicia a vetorização.
1.  **Divisão em Chunks**: O texto é fracionado utilizando o `RecursiveCharacterTextSplitter` da biblioteca LangChain. O tamanho ideal configurado é de 1200 caracteres (`CHUNK_SIZE`) com uma sobreposição de 150 caracteres (`CHUNK_OVERLAP`) para não perder contextos que fiquem nos limites das quebras.
2.  **Modelo de Embeddings**: É utilizado o modelo local e gratuito `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace. Ele gera vetores densos de 384 dimensões.
3.  **Estruturação FAISS**: A coleção de vetores é adicionada a um índice FAISS local.
4.  **Gravação em Disco**: O índice é gravado localmente na pasta `indices_faiss/` no formato `faiss_<arquivo_id>.index`.
5.  **Registro de Metadados**: A tabela `embedding` é populada com o caminho do arquivo físico e o total de chunks criados.

---

### 4.3. Fluxo de Pergunta e Resposta (RAG)

Quando o usuário realiza uma pergunta na interface gráfica sobre um arquivo previamente selecionado:

```mermaid
sequenceDiagram
    participant U as Usuário
    participant G as gui.py (Interface)
    participant M as main.py (RAG)
    participant F as FAISS (Índice Local)
    participant API as API da Groq

    U->>G: Digita pergunta e envia
    G->>M: answer_question(sess, arquivo_id, pergunta_texto)
    M->>F: Carrega índice faiss_<arquivo_id>.index correspondente
    M->>F: Realiza busca semântica (similarity_search, k=5)
    F-->>M: Retorna 5 trechos de contexto mais relevantes
    alt Groq API Key Configurada
        M->>API: Envia System Prompt + Contexto + Pergunta
        API-->>M: Retorna Resposta Gerada em Markdown
    else Groq API Key Ausente
        M-->>M: Gera Resposta com o contexto cru recuperado
    end
    M->>G: Retorna string da resposta final
    G->>U: Renderiza no painel de chat (com suporte a Markdown e HTML)
```

#### Parâmetros do RAG
*   **Quantidade de Contextos (k)**: 5 chunks são recuperados do FAISS a cada pergunta.
*   **Prompt do Sistema (System Prompt)**: Instrui a LLM a atuar de forma prestativa, fundamentar a resposta exclusivamente no contexto fornecido (evitando alucinações), utilizar formatação Markdown rica (tabelas e listas quando necessário) e perguntar ao usuário se ele necessita de mais detalhes.

---

### 4.4. Fluxo de Gráficos e Consultas SQL

O sistema conta com rotinas de análise internas.

*   **Gráficos de Estatísticas de Uso**: Gerados sob demanda por meio de consultas diretas ao banco de dados utilizando bibliotecas de dados (`pandas` e `matplotlib`).
    *   *Gráfico 1*: Quantidade de arquivos por tipo de extensão (gráfico de barras).
    *   *Gráfico 2*: Contagem de perguntas realizadas por arquivo cadastrado (gráfico de barras).
    *   *Gráfico 3*: Tempo médio de processamento/resposta da inteligência artificial por tipo de arquivo (gráfico de linhas).
    *   Os gráficos são salvos na pasta `charts/` com carimbos de tempo (timestamps) de geração e exibidos na tela.
*   **Consultas SQL Customizadas**: O usuário pode redigir queries SELECT brutas diretamente na interface.
    1.  A query é validada para garantir que contém apenas a instrução SELECT (evitando alterações acidentais de tabelas).
    2.  O `pandas` executa a query e cria um dataframe.
    3.  Os dados são salvos em formato de planilha do Excel (.xlsx) na pasta `consultas/`.
    4.  O banco grava o histórico da consulta (`consulta_sql` e `resultado_consulta`), registrando a query estruturada, número de linhas e colunas resultantes e os registros completos em formato JSON.

---

### 4.5. Fluxo de Remoção Segura de Dados

Para remover um arquivo e limpar o banco de dados completamente, garantindo a integridade referencial e o consumo de disco:
1.  **Exclusão dos Índices Físicos**: O sistema força a coleta de lixo do Python (`gc.collect()`), aplica permissões de escrita e apaga os arquivos de índices FAISS na pasta `indices_faiss/`.
2.  **Exclusão em Cascata das Respostas e Perguntas**: Remove todos os registros vinculados à tabela `resposta_ia` e depois da tabela `pergunta` relacionados ao arquivo.
3.  **Remoção de Logs e Resumos**: Remove os logs e o resumo atrelados ao arquivo específico.
4.  **Exclusão dos Metadados e Binários**: Remove os metadados do texto extraído (`conteudo_extraido`) e finalmente a linha principal na tabela `arquivo`.
5.  **Rollback Automático**: Caso ocorra alguma falha durante os passos de remoção física ou no banco de dados, o SQLAlchemy executa um rollback para evitar estados inconsistentes ou dados órfãos.

---

## 5. Estrutura e Estilização da Interface Gráfica (`gui.py`)

A interface foi implementada com Tkinter tradicional integrado com a biblioteca `tkinterweb` para contornar a limitação de formatação textual rica do Tkinter.

### Características Visuais e UX
*   **Tema Clam**: Configurado no `ttk.Style` para fornecer botões e campos de texto com estética limpa (cantos retos, cores suaves).
*   **Divisão em Painéis**:
    *   *Painel Esquerdo (Chat)*: Ocupa a maior parte da tela. Contém a visualização das mensagens e a caixa de texto para envio de perguntas.
    *   *Painel Direito (Menu)*: Barra de ferramentas que exibe a logomarca do projeto (carregada dinamicamente da pasta `figure/logo.png`) e os botões de ação do sistema dispostos verticalmente.
*   **Balões de Chat Dinâmicos**: O sistema calcula a largura disponível da tela e cria retângulos com bordas arredondadas no Canvas para delimitar as mensagens:
    *   *Mensagens do Usuário*: Balões verdes localizados no canto direito da tela.
    *   *Mensagens do Sistema e Logs*: Balões cinzas ou coloridos (vermelho para erros) que exibem notificações de status do sistema.
    *   *Mensagens da Inteligência Artificial*: Balões azuis alinhados à esquerda, contendo um objeto `HtmlFrame` integrado que interpreta as tags HTML geradas a partir do Markdown do Groq.
*   **Rolagem Automática**: Toda nova mensagem inserida força o reposicionamento do scroll do canvas para o final (`yview_moveto(1.0)`).

---

## 6. Configuração e Dependências do Ambiente

### Variáveis de Ambiente (`.env`)
O arquivo `.env` deve ser mantido na raiz do projeto com as chaves:
```properties
DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/nome_do_banco
GROQ_API_KEY=gsk_suachaveaqui
GROQ_API_MODEL=llama-3.3-70b-versatile
```

### Principais Bibliotecas e Responsabilidades
*   `SQLAlchemy`: Ferramenta ORM para interface relacional com o PostgreSQL.
*   `psycopg2-binary`: Driver de conexão com o banco de dados.
*   `langchain` e `langchain-community`: Criação do fluxo de encadeamento RAG (chains) e gerenciamento de prompts.
*   `langchain-huggingface`: Encapsula a conversão de textos utilizando o sentence-transformers local.
*   `langchain-groq`: Integração para chamada da API de LLMs da Groq.
*   `faiss-cpu`: Processador vetorial para armazenamento dos índices locais em disco.
*   `pymupdf` (`fitz`): Extração de textos de PDFs de alta performance.
*   `python-docx`: Leitor e extrator de documentos do Microsoft Word.
*   `pandas` e `openpyxl`: Manipulação de dataframes, conversões estruturadas e exportação para Excel.
*   `matplotlib`: Plotagem e salvamento dos arquivos de gráficos.
*   `markdown2`: Conversor de Markdown para HTML.
*   `tkinterweb`: Renderizador de HTML/CSS integrado ao Tkinter para exibição dos textos de resposta formatados.
