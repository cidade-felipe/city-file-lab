# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import pandas as pd
import threading
from tkinterweb import HtmlFrame
import markdown2
import main as m

CORES = {
    'fundo': '#F1F5F9',
    'cartao': '#FFFFFF',
    'chat': '#F8FAFC',
    'sidebar': '#0F172A',
    'sidebar_hover': '#1E293B',
    'sidebar_texto': '#CBD5E1',
    'primaria': '#2563EB',
    'primaria_hover': '#1D4ED8',
    'texto': '#0F172A',
    'texto_secundario': '#64748B',
    'borda': '#E2E8F0',
    'sucesso': '#059669',
}

janela = tk.Tk()
janela.title('City File Lab')
janela.geometry('1280x780')
janela.minsize(1080, 680)
janela.configure(bg=CORES['fundo'])
janela.state('zoomed')
janela.resizable(True, True)

style = ttk.Style()
style.theme_use('clam')

style.configure(
    'Custom.TButton',
    font=('Segoe UI Semibold', 10),
    padding=(14, 9),
    background=CORES['primaria'],
    foreground='white',
    borderwidth=0,
    focusthickness=0,
)
style.map(
    'Custom.TButton',
    background=[('active', CORES['primaria_hover']), ('disabled', '#94A3B8')],
    foreground=[('disabled', '#E2E8F0')],
)
style.configure(
    'Modern.TEntry',
    font=('Segoe UI', 11),
    padding=(12, 10),
    fieldbackground='white',
    foreground=CORES['texto'],
    bordercolor=CORES['borda'],
    lightcolor=CORES['borda'],
    darkcolor=CORES['borda'],
)
style.configure(
    'Modern.TCombobox',
    font=('Segoe UI', 10),
    padding=8,
    fieldbackground='white',
)
style.configure(
    'Modal.TLabel',
    background=CORES['cartao'],
    foreground=CORES['texto'],
    font=('Segoe UI', 10),
)
style.configure(
    'Vertical.TScrollbar',
    background='#CBD5E1',
    troughcolor=CORES['chat'],
    bordercolor=CORES['chat'],
    arrowcolor=CORES['texto_secundario'],
)

app_shell = tk.Frame(janela, bg=CORES['fundo'])
app_shell.pack(fill='both', expand=True)

frame_menu = tk.Frame(app_shell, bg=CORES['sidebar'], width=282)
frame_menu.pack(side='left', fill='y')
frame_menu.pack_propagate(False)

brand = tk.Frame(frame_menu, bg=CORES['sidebar'])
brand.pack(fill='x', padx=24, pady=(24, 18))

try:
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figure', 'logo.png')
    img = Image.open(image_path).resize((104, 104))
    img_tk = ImageTk.PhotoImage(img)
    lbl_logo = tk.Label(brand, image=img_tk, bg=CORES['sidebar'], borderwidth=0)
    lbl_logo.image = img_tk
    lbl_logo.pack(anchor='w')
except Exception:
    tk.Label(
        brand,
        text='CFL',
        bg=CORES['primaria'],
        fg='white',
        font=('Segoe UI Semibold', 18),
        padx=14,
        pady=10,
    ).pack(anchor='w')

tk.Label(
    brand,
    text='CITY FILE LAB',
    bg=CORES['sidebar'],
    fg='white',
    font=('Segoe UI Semibold', 15),
).pack(anchor='w', pady=(14, 2))
tk.Label(
    brand,
    text='Análise inteligente de arquivos',
    bg=CORES['sidebar'],
    fg='#94A3B8',
    font=('Segoe UI', 9),
).pack(anchor='w')

tk.Frame(frame_menu, bg='#1E293B', height=1).pack(fill='x', padx=24)

sidebar_nav = tk.Frame(frame_menu, bg=CORES['sidebar'])
sidebar_nav.pack(fill='both', expand=True, padx=14, pady=14)

sidebar_footer = tk.Frame(frame_menu, bg=CORES['sidebar'])
sidebar_footer.pack(fill='x', padx=14, pady=(0, 18))

area_principal = tk.Frame(app_shell, bg=CORES['fundo'])
area_principal.pack(side='left', fill='both', expand=True, padx=28, pady=22)

cabecalho_app = tk.Frame(area_principal, bg=CORES['fundo'])
cabecalho_app.pack(fill='x', pady=(0, 16))

cabecalho_textos = tk.Frame(cabecalho_app, bg=CORES['fundo'])
cabecalho_textos.pack(side='left')
tk.Label(
    cabecalho_textos,
    text='Workspace de análise',
    bg=CORES['fundo'],
    fg=CORES['texto'],
    font=('Segoe UI Semibold', 22),
).pack(anchor='w')
tk.Label(
    cabecalho_textos,
    text='Converse com seus documentos e explore os dados em um só lugar.',
    bg=CORES['fundo'],
    fg=CORES['texto_secundario'],
    font=('Segoe UI', 10),
).pack(anchor='w', pady=(3, 0))

status_frame = tk.Frame(cabecalho_app, bg='#ECFDF5', padx=13, pady=7)
status_frame.pack(side='right', pady=7)
status_dot = tk.Label(
    status_frame,
    text='●',
    bg='#ECFDF5',
    fg=CORES['sucesso'],
    font=('Segoe UI', 8),
)
status_dot.pack(side='left')
status_label = tk.Label(
    status_frame,
    text='Pronto',
    bg='#ECFDF5',
    fg='#047857',
    font=('Segoe UI Semibold', 9),
)
status_label.pack(side='left', padx=(5, 0))

frame_chat = tk.Frame(
    area_principal,
    bg=CORES['cartao'],
    highlightbackground=CORES['borda'],
    highlightthickness=1,
)
frame_chat.pack(fill='both', expand=True)

chat_header = tk.Frame(frame_chat, bg=CORES['cartao'], height=70)
chat_header.pack(fill='x')
chat_header.pack_propagate(False)

chat_header_text = tk.Frame(chat_header, bg=CORES['cartao'])
chat_header_text.pack(side='left', padx=22, pady=14)
tk.Label(
    chat_header_text,
    text='Assistente de documentos',
    bg=CORES['cartao'],
    fg=CORES['texto'],
    font=('Segoe UI Semibold', 13),
).pack(anchor='w')
tk.Label(
    chat_header_text,
    text='As respostas usam somente o conteúdo do arquivo selecionado.',
    bg=CORES['cartao'],
    fg=CORES['texto_secundario'],
    font=('Segoe UI', 9),
).pack(anchor='w', pady=(2, 0))

arquivo_badge = tk.Frame(chat_header, bg='#EFF6FF', padx=12, pady=7)
arquivo_badge.pack(side='right', padx=22, pady=17)
tk.Label(
    arquivo_badge,
    text='ARQUIVO',
    bg='#EFF6FF',
    fg=CORES['primaria'],
    font=('Segoe UI Semibold', 8),
).pack(side='left')
label_arquivo_status = tk.Label(
    arquivo_badge,
    text='Nenhum selecionado',
    bg='#EFF6FF',
    fg='#1E40AF',
    font=('Segoe UI', 9),
)
label_arquivo_status.pack(side='left', padx=(7, 0))

tk.Frame(frame_chat, bg=CORES['borda'], height=1).pack(fill='x')

frame_canvas = tk.Frame(frame_chat, bg=CORES['chat'])
frame_canvas.pack(fill='both', expand=True)

canvas = tk.Canvas(frame_canvas, bg=CORES['chat'], highlightthickness=0)
scrollbar = ttk.Scrollbar(frame_canvas, orient='vertical', command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)

frame_mensagens = tk.Frame(canvas, bg=CORES['chat'])
mensagens_window = canvas.create_window((0, 0), window=frame_mensagens, anchor='nw')


def atualizar_scroll(event=None):
    canvas.configure(scrollregion=canvas.bbox('all'))


def ajustar_largura_mensagens(event):
    canvas.itemconfigure(mensagens_window, width=event.width)


frame_mensagens.bind('<Configure>', atualizar_scroll)
canvas.bind('<Configure>', ajustar_largura_mensagens)


def _rounded_rect(canvas_obj, x1, y1, x2, y2, r=12, **kwargs):
    pontos = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas_obj.create_polygon(pontos, smooth=True, **kwargs)


def md_to_html(md_text: str) -> str:
    html_body = markdown2.markdown(
        md_text,
        extras=[
            "fenced-code-blocks",
            "tables",
            "strike",
            "break-on-newline",
            "code-friendly",
            "smarty-pants"
        ]
    )
    style = """
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            color: #1E293B;
            background: #FFFFFF;
            font-size: 14px;
            line-height: 1.55;
        }
        p { margin: 0.45em 0; }
        pre, code { font-family: Consolas, Menlo, monospace; }
        code { color: #1D4ED8; }
        pre {
            background:#F1F5F9;
            padding:12px;
            border-radius:10px;
            overflow:auto;
        }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th {
            background: #F8FAFC;
            color: #334155;
        }
        th, td {
            border: 1px solid #E2E8F0;
            padding: 8px 10px;
            text-align: left;
        }
        h1, h2, h3, h4 { margin: 0.4em 0 0.2em; }
        a { color: #2563EB; text-decoration: none; }
    </style>
    """
    return f'<!doctype html><html><head>{style}</head><body>{html_body}</body></html>'


def exibir_mensagem(remetente, texto, cor=None):
    largura_msg = max(frame_chat.winfo_width() - 280, 460)

    wrap = tk.Frame(frame_mensagens, bg=CORES['chat'])
    wrap.pack(fill='x', padx=22, pady=10)

    if remetente == 'Você':
        anchor_side = 'e'
        cor_bg = cor or CORES['primaria']
        cor_borda = CORES['primaria']
        cor_texto = 'white'
        titulo = 'VOCÊ'
        margem = (150, 0)
    elif remetente == 'IA':
        anchor_side = 'w'
        cor_bg = cor or CORES['cartao']
        cor_borda = CORES['borda']
        cor_texto = CORES['texto']
        titulo = 'ASSISTENTE'
        margem = (0, 150)
    else:
        anchor_side = 'w'
        cor_bg = cor or '#EEF2FF'
        if cor == '#ffe6e6' or remetente == 'Erro':
            cor_borda = '#FECACA'
            cor_texto = '#991B1B'
        elif cor == '#e6ffe6':
            cor_borda = '#BBF7D0'
            cor_texto = '#166534'
        elif cor == '#fff8dc':
            cor_borda = '#FDE68A'
            cor_texto = '#92400E'
        else:
            cor_borda = '#C7D2FE'
            cor_texto = '#3730A3'
        titulo = 'ATIVIDADE' if remetente != 'Erro' else 'ERRO'
        margem = (0, 210)

    cabecalho = tk.Label(
        wrap,
        text=titulo,
        bg=CORES['chat'],
        fg=CORES['texto_secundario'],
        font=('Segoe UI Semibold', 8),
        anchor='e' if anchor_side == 'e' else 'w',
        justify='right' if anchor_side == 'e' else 'left'
    )
    cabecalho.pack(fill='x', padx=3, pady=(0, 4))

    c = tk.Canvas(wrap, bg=CORES['chat'], highlightthickness=0, borderwidth=0, height=10)
    if anchor_side == 'e':
        spacer = tk.Frame(wrap, bg=CORES['chat'])
        spacer.pack(side='left', expand=True, fill='x')
        c.pack(side='right', padx=margem, fill='x')
    else:
        c.pack(side='left', padx=margem, fill='x')

    inner = tk.Frame(c, bg=cor_bg)
    pad_int = 13
    max_width = largura_msg

    if remetente == 'IA':
        html = md_to_html(texto)
        content = HtmlFrame(inner, horizontal_scrollbar='auto', messages_enabled=False)
        content.load_html(html)
        content.pack(fill='both', expand=True, padx=pad_int, pady=pad_int)
    else:
        content = tk.Message(
            inner,
            text=texto,
            bg=cor_bg,
            fg=cor_texto,
            width=max_width,
            justify='left',
            anchor='w',
            padx=pad_int,
            pady=pad_int,
            font=('Segoe UI', 10),
        )
        content.pack(fill='both', expand=True)

    window_id = c.create_window(0, 0, window=inner, anchor='nw')

    def ajustar():
        c.update_idletasks()
        inner.update_idletasks()

        w = min(inner.winfo_reqwidth(), max_width)
        inner.config(width=w)
        c.config(width=w)

        if remetente == 'IA' and hasattr(content, 'fit_height'):
            content.fit_height()

        c.update_idletasks()
        inner.update_idletasks()

        h = max(
            inner.winfo_reqheight(),
            content.winfo_reqheight() + 2 * pad_int if remetente == 'IA' else inner.winfo_reqheight()
        )
        c.config(height=h)

        c.coords(window_id, 0, 0)
        c.delete('bubble')
        _rounded_rect(
            c,
            1,
            1,
            w - 1,
            h - 1,
            r=18,
            fill=cor_bg,
            outline=cor_borda,
            width=1,
            tags='bubble',
        )
        c.tag_lower('bubble')

        frame_mensagens.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))
        canvas.yview_moveto(1.0)

    ajustar()
    wrap.after(50, ajustar)


exibir_mensagem(
    'Sistema',
    'Tudo pronto. Faça upload de um arquivo ou selecione um documento existente para começar.',
)


_tarefas_ativas = 0


def atualizar_status(texto, cor_texto, cor_fundo):
    status_frame.configure(bg=cor_fundo)
    status_dot.configure(bg=cor_fundo, fg=cor_texto)
    status_label.configure(bg=cor_fundo, fg=cor_texto, text=texto)


def executar_em_background(tarefa, ao_concluir, ao_falhar):
    global _tarefas_ativas
    _tarefas_ativas += 1
    janela.configure(cursor='watch')
    atualizar_status('Processando', '#B45309', '#FFFBEB')

    def finalizar():
        global _tarefas_ativas
        _tarefas_ativas = max(0, _tarefas_ativas - 1)
        if _tarefas_ativas == 0:
            janela.configure(cursor='')
            atualizar_status('Pronto', '#047857', '#ECFDF5')

    def executar():
        try:
            resultado = tarefa()
        except Exception as e:
            mensagem = str(e)

            def reportar_erro():
                finalizar()
                ao_falhar(mensagem)

            janela.after(0, reportar_erro)
            return

        def reportar_sucesso():
            finalizar()
            ao_concluir(resultado)

        janela.after(0, reportar_sucesso)

    threading.Thread(target=executar, daemon=True).start()


def configurar_modal(modal, titulo, geometria):
    modal.title(titulo)
    modal.geometry(geometria)
    modal.configure(bg=CORES['cartao'])
    modal.resizable(False, False)
    modal.transient(janela)
    modal.grab_set()


def criar_tabelas():
    try:
        msg = m.create_all()
        exibir_mensagem('Sistema', msg)
        messagebox.showinfo('INFO', msg)
    except Exception as e:
        exibir_mensagem('Erro', str(e))
        messagebox.showerror('Erro', str(e))


def remover_tabelas():
    if not m.verificar_banco() or not m.verificar_tabelas():
        msg = 'Não é possível remover as tabelas, porque elas ainda não existem. Clique em "Criar tabelas" primeiro.'
        exibir_mensagem('Sistema', msg)
        messagebox.showinfo('Aviso', msg)
        return

    conf = messagebox.askyesno('Confirmação', 'Tem certeza que deseja remover todas as tabelas e pastas?')
    if not conf:
        return messagebox.showerror('ERRO', 'Ação cancelada pelo usuário.')
    janela.bell()
    aviso = messagebox.askyesno('AVISO', 'Essa ação é irreversível! Deseja continuar?')
    if not aviso:
        return messagebox.showerror('ERRO', 'Ação cancelada pelo usuário.')
    try:
        msg = m.drop_all()
        exibir_mensagem('Sistema', msg)
        messagebox.showinfo('INFO', msg)
    except Exception as e:
        exibir_mensagem('Erro', str(e))
        messagebox.showerror('Erro', str(e))


def upload_arquivo():
    if not m.verificar_banco() or not m.verificar_tabelas():
        msg = 'Não é possível fazer upload de arquivos, porque o banco ainda não foi inicializado. Clique em "Criar tabelas" primeiro.'
        exibir_mensagem('Sistema', msg)
        messagebox.showerror('Erro', msg)
        return

    caminho = filedialog.askopenfilename(
        title='Selecione um arquivo',
        filetypes=[
            ('Todos os suportados', '*.pdf; *.docx; *.xlsx; *.xls; *.csv; *.txt; *.md'),
            ('PDF', '*.pdf'),
            ('Word', '*.docx'),
            ('Excel', '*.xlsx; *.xls'),
            ('CSV', '*.csv'),
            ('TXT', '*.txt'),
            ('Markdown', '*.md'),
        ]
    )
    if not caminho:
        return

    def processar_upload():
        with m.SessionLocal() as sess:
            resultado = m.upload_file(sess, caminho)

        arq_id = resultado['id']
        with m.SessionLocal() as sess:
            log = (
                sess.query(m.Log)
                .filter_by(arquivo_id=arq_id)
                .order_by(m.Log.data.desc())
                .first()
            )
            dados_log = (
                (log.acao, log.detalhe, log.data)
                if log
                else None
            )
        return resultado, dados_log

    def concluir_upload(payload):
        resultado, dados_log = payload
        arq_id = resultado['id']
        if resultado['duplicado']:
            nome_existente = resultado['nome']
            exibir_mensagem(
                'Sistema',
                f'O conteúdo já existe no arquivo "{nome_existente}". ID={arq_id}. Upload pulado.',
            )
        else:
            exibir_mensagem('Sistema', f'Upload concluído com sucesso. ID={arq_id}')

        if dados_log:
            acao, detalhe, data = dados_log
            cor = '#ffe6e6' if 'erro' in acao.lower() else '#e6ffe6'
            if 'duplicado' in acao.lower():
                cor = '#fff8dc'
            hora = pd.to_datetime(data).strftime('%d-%m-%y-%H:%M:%S')
            exibir_mensagem('Log', f'[{hora}] {acao} → {detalhe}', cor)

    def falhar_upload(mensagem):
        exibir_mensagem('Erro', mensagem)
        messagebox.showerror('Erro', mensagem)

    exibir_mensagem('Sistema', f'Processando o arquivo "{os.path.basename(caminho)}"...')
    executar_em_background(processar_upload, concluir_upload, falhar_upload)


id_arquivo_escolhido = None


def perguntar_arquivo():
    if not m.verificar_banco() or not m.verificar_tabelas():
        msg = 'Não é possível perguntar sobre arquivos, porque o banco ainda não foi inicializado. Clique em "Criar tabelas" primeiro.'
        exibir_mensagem('Sistema', msg)
        messagebox.showerror('Erro', msg)
        return

    global id_arquivo_escolhido

    try:
        df = pd.read_sql_query("SELECT id, nome FROM arquivo ORDER BY id DESC", con=m.engine)
    except Exception as e:
        exibir_mensagem('Erro', f'Erro ao listar arquivos: {e}')
        return messagebox.showerror('Erro', str(e))
    if df.empty:
        return messagebox.showerror('ERRO', 'Nenhum arquivo encontrado. Faça upload primeiro.')

    janela_id = tk.Toplevel(janela)
    configurar_modal(janela_id, 'Selecionar arquivo', '460x210')

    ttk.Label(
        janela_id,
        text='Qual documento você quer consultar?',
        style='Modal.TLabel',
        font=('Segoe UI Semibold', 12),
    ).pack(anchor='w', padx=24, pady=(24, 5))
    ttk.Label(
        janela_id,
        text='A conversa ficará vinculada ao arquivo selecionado.',
        style='Modal.TLabel',
        foreground=CORES['texto_secundario'],
    ).pack(anchor='w', padx=24)
    combo = ttk.Combobox(
        janela_id,
        width=52,
        values=df['nome'].tolist(),
        state='readonly',
        style='Modern.TCombobox',
    )
    combo.pack(fill='x', padx=24, pady=(18, 8))

    def confirmar():
        global id_arquivo_escolhido
        nome = combo.get().strip()
        if not nome:
            messagebox.showwarning('Aviso', 'Selecione um arquivo.')
            return
        try:
            id_arquivo_escolhido = int(df.loc[df['nome'] == nome, 'id'].iloc[0])
        except Exception as e:
            messagebox.showerror('Erro', f'Seleção inválida: {e}')
            return
        label_arquivo_status.configure(text=nome)
        exibir_mensagem('Sistema', f'Arquivo "{nome}" selecionado (ID={id_arquivo_escolhido}) para perguntas.')
        janela_id.destroy()

    ttk.Button(
        janela_id,
        text='Usar este arquivo',
        style='Custom.TButton',
        command=confirmar,
    ).pack(anchor='e', padx=24, pady=12)


def enviar_pergunta():
    global id_arquivo_escolhido
    pergunta = entry_enviar.get().strip()
    if not pergunta:
        return
    if id_arquivo_escolhido is None:
        messagebox.showwarning('Aviso', 'Selecione um arquivo antes de perguntar.')
        return
    exibir_mensagem('Você', pergunta)
    entry_enviar.delete(0, tk.END)
    entry_enviar.configure(state='disabled')
    botao_enviar.configure(state='disabled', bg='#94A3B8', cursor='arrow')
    arquivo_id = id_arquivo_escolhido

    def processar_pergunta():
        with m.SessionLocal() as sess:
            return m.answer_question(sess, arquivo_id, pergunta)

    def concluir_pergunta(resposta):
        exibir_mensagem('IA', resposta)
        entry_enviar.configure(state='normal')
        botao_enviar.configure(state='normal', bg=CORES['primaria'], cursor='hand2')
        entry_enviar.focus_set()

    def falhar_pergunta(mensagem):
        exibir_mensagem('Erro', mensagem)
        messagebox.showerror('Erro', mensagem)
        entry_enviar.configure(state='normal')
        botao_enviar.configure(state='normal', bg=CORES['primaria'], cursor='hand2')
        entry_enviar.focus_set()

    executar_em_background(processar_pergunta, concluir_pergunta, falhar_pergunta)


def graficos_prontos():
    if not m.verificar_banco() or not m.verificar_tabelas():
        msg = 'Não é possível gerar gráficos, porque o banco ainda não foi inicializado. Clique em "Criar tabelas" primeiro.'
        exibir_mensagem('Sistema', msg)
        messagebox.showerror('Erro', msg)
        return

    try:
        df = pd.read_sql_query('SELECT id, nome FROM arquivo ORDER BY id DESC', con=m.engine)
    except Exception as e:
        exibir_mensagem('Erro', f'Erro ao gerar os gráficos: {e}')
        messagebox.showerror('Erro', str(e))
        return

    if df.empty:
        messagebox.showerror('Aviso', 'Nenhum arquivo encontrado. Faça upload primeiro.')
        return

    exibir_mensagem('Sistema', 'Executando consultas e gráficos prontos...')
    try:
        sqls = [
            (
                "Quantidade de arquivos x tipo",
                "Tipo",
                "Quantidade",
                '''
                SELECT t.nome AS tipo, COUNT(a.id) AS qtde
                FROM tipo_arquivo t
                LEFT JOIN arquivo a ON a.tipo_id = t.id
                GROUP BY t.nome ORDER BY qtde DESC
                ''',
                "Arquivos por tipo",
                "barras"
            ),
            (
                "Perguntas x arquivo",
                "Arquivo",
                "Nº perguntas",
                '''
                SELECT a.nome AS arquivo, COUNT(p.id) AS perguntas
                FROM arquivo a
                LEFT JOIN pergunta p ON p.arquivo_id = a.id
                GROUP BY a.nome ORDER BY perguntas DESC
                ''',
                "Perguntas por arquivo",
                "barras"
            ),
            (
                "Tempo médio de resposta x tipo",
                "Tipo",
                "Tempo (s)",
                '''
                SELECT t.nome AS tipo, COALESCE(AVG(r.tempo_execucao),0) AS tempo_medio_s
                FROM tipo_arquivo t
                LEFT JOIN arquivo a ON a.tipo_id = t.id
                LEFT JOIN pergunta p ON p.arquivo_id = a.id
                LEFT JOIN resposta_ia r ON r.pergunta_id = p.id
                GROUP BY t.nome ORDER BY tempo_medio_s DESC
                ''',
                "Tempo médio de resposta",
                "linhas"
            ),
        ]
        for args in sqls:
            m.run_and_plot(*args)
        exibir_mensagem('Sistema', 'Consultas e gráficos prontos concluídos.')
    except Exception as e:
        exibir_mensagem('Erro', str(e))
        messagebox.showerror('Erro', str(e))


def consulta_sql():
    if not m.verificar_banco() or not m.verificar_tabelas():
        msg = 'Não é possível executar consultas, porque o banco ainda não foi inicializado. Clique em "Criar tabelas" primeiro.'
        exibir_mensagem('Sistema', msg)
        messagebox.showerror('Erro', msg)
        return
    try:
        df = pd.read_sql_query(
            '''SELECT a.id as id,
                                a.nome as nome
                                FROM arquivo a
                                ORDER BY nome''',
            con=m.engine
        )
        if df.empty:
            return messagebox.showerror('ERRO', 'Nenhum arquivo disponível para consulta.')
    except Exception as e:
        return messagebox.showerror('Erro', f'Falha ao buscar arquivos: {e}')

    janela_sql = tk.Toplevel(janela)
    configurar_modal(janela_sql, 'Consulta SQL', '680x500')

    ttk.Label(
        janela_sql,
        text='Consulta SQL personalizada',
        style='Modal.TLabel',
        font=('Segoe UI Semibold', 14),
    ).pack(anchor='w', padx=24, pady=(22, 4))
    ttk.Label(
        janela_sql,
        text='Somente uma instrução SELECT é permitida. O resultado será exportado para Excel.',
        style='Modal.TLabel',
        foreground=CORES['texto_secundario'],
    ).pack(anchor='w', padx=24)
    editor_sql = tk.Frame(
        janela_sql,
        bg=CORES['borda'],
        highlightbackground=CORES['borda'],
        highlightthickness=1,
    )
    editor_sql.pack(padx=24, pady=18, fill='both', expand=True)
    entry_sql = tk.Text(
        editor_sql,
        height=15,
        width=80,
        font=('Cascadia Mono', 10),
        bg='#0F172A',
        fg='#E2E8F0',
        insertbackground='white',
        selectbackground=CORES['primaria'],
        relief='flat',
        padx=14,
        pady=14,
        undo=True,
    )
    entry_sql.pack(fill='both', expand=True)

    def executar():
        sql = entry_sql.get('1.0', 'end').strip()

        def processar_consulta():
            with m.SessionLocal() as sess:
                return m.execute_custom_query(
                    sess,
                    sql,
                    'Consulta executada pela interface gráfica',
                )

        def concluir_consulta(resultado):
            botao_executar.configure(state='normal')
            caminho = resultado['caminho_arquivo']
            linhas = resultado['linhas']
            colunas = resultado['colunas']
            mensagem = (
                f'Consulta executada com sucesso: {linhas} linhas × {colunas} colunas. '
                f'Resultado salvo em {caminho}'
            )
            exibir_mensagem('Sistema', mensagem)
            messagebox.showinfo('Sucesso', mensagem)

        def falhar_consulta(mensagem):
            botao_executar.configure(state='normal')
            exibir_mensagem('Erro', mensagem)
            messagebox.showerror('Erro', mensagem)

        botao_executar.configure(state='disabled')
        executar_em_background(processar_consulta, concluir_consulta, falhar_consulta)

    botao_executar = ttk.Button(
        janela_sql,
        text='Executar e exportar',
        style='Custom.TButton',
        command=executar,
    )
    botao_executar.pack(anchor='e', padx=24, pady=(0, 20))


def remover_arquivo():
    if not m.verificar_banco() or not m.verificar_tabelas():
        msg = 'Não é possível remover arquivos, porque o banco ainda não foi inicializado. Clique em "Criar tabelas" primeiro.'
        exibir_mensagem('Sistema', msg)
        messagebox.showerror('Erro', msg)
        return
    try:
        df = pd.read_sql_query(
            '''SELECT a.id as id,
                                a.nome as nome
                                FROM arquivo a
                                ORDER BY nome''',
            con=m.engine
        )
        if df.empty:
            return messagebox.showerror('ERRO', 'Nenhum arquivo disponível para remoção.')
    except Exception as e:
        return messagebox.showerror('Erro', f'Falha ao buscar arquivos: {e}')

    janela_remover = tk.Toplevel(janela)
    configurar_modal(janela_remover, 'Remover arquivo', '480x240')

    ttk.Label(
        janela_remover,
        text='Remover documento',
        style='Modal.TLabel',
        font=('Segoe UI Semibold', 14),
    ).pack(anchor='w', padx=24, pady=(24, 4))
    ttk.Label(
        janela_remover,
        text='Esta ação também remove perguntas, respostas, resumo e índice vetorial.',
        style='Modal.TLabel',
        foreground=CORES['texto_secundario'],
    ).pack(anchor='w', padx=24)
    combo = ttk.Combobox(
        janela_remover,
        width=60,
        values=df['nome'].to_list(),
        state='readonly',
        style='Modern.TCombobox',
    )
    combo.pack(fill='x', padx=24, pady=(20, 10))

    def confirmar_remocao():
        global id_arquivo_escolhido
        nome = combo.get()
        if not nome:
            messagebox.showwarning('Aviso', 'Selecione um arquivo.')
            return
        arq_id = int(df.loc[df['nome'] == nome, 'id'].iloc[0])
        conf = messagebox.askyesno('Confirmação', f'Tem certeza que deseja remover o arquivo "{nome}" (ID={arq_id})?')
        if conf:
            janela_remover.bell()
            aviso = messagebox.askyesno('Confirmação', 'Essa ação é irreversível! Deseja continuar?')
            if not aviso:
                return messagebox.showerror('ERRO', 'Ação cancelada pelo usuário.')
            with m.SessionLocal() as sess:
                resultado = m.remove_file(sess, arq_id)
            exibir_mensagem('Sistema', resultado)
            if '[OK]' in resultado:
                if id_arquivo_escolhido == arq_id:
                    id_arquivo_escolhido = None
                    label_arquivo_status.configure(text='Nenhum selecionado')
                messagebox.showinfo('Sucesso', resultado)
            else:
                messagebox.showerror('Erro', resultado)
            janela_remover.destroy()
        return

    ttk.Button(
        janela_remover,
        text='Remover documento',
        style='Custom.TButton',
        command=confirmar_remocao,
    ).pack(anchor='e', padx=24, pady=14)


def listar_arquivos():
    if not m.verificar_banco() or not m.verificar_tabelas():
        msg = 'Não é possível listar arquivos, porque o banco ainda não foi inicializado. Clique em "Criar tabelas" primeiro.'
        exibir_mensagem('Sistema', msg)
        messagebox.showerror('Erro', msg)
        return

    try:
        df_arquivos = pd.read_sql_query(
            '''
            SELECT a.id, a.nome
            FROM arquivo a
            ORDER BY a.id
        ''',
            m.engine
        )
        lista_arquivos_ids = df_arquivos['id'].tolist()
        lista_arquivos_nomes = df_arquivos['nome'].tolist()
        arquivos = '\n'.join(f'ID: {id} | Nome: {nome}' for id, nome in zip(lista_arquivos_ids, lista_arquivos_nomes))
        if df_arquivos.empty:
            return messagebox.showerror('ERRO', 'Nenhum arquivo encontrado. Faça upload primeiro.')
    except Exception as e:
        exibir_mensagem('Erro', str(e))
        messagebox.showerror('Erro', str(e))
        return

    messagebox.showinfo('Lista de Arquivos', arquivos)


def sair():
    sair_resp = messagebox.askyesno('SAIR', 'Tem certeza que deseja sair?')
    if sair_resp:
        janela.destroy()


def criar_botao_navegacao(parent, texto, icone, comando, variante='normal'):
    estilos = {
        'normal': (CORES['sidebar'], CORES['sidebar_hover'], CORES['sidebar_texto']),
        'primario': (CORES['primaria'], CORES['primaria_hover'], 'white'),
        'perigo': (CORES['sidebar'], '#3F1D2B', '#FCA5A5'),
    }
    fundo, hover, texto_cor = estilos[variante]
    botao = tk.Button(
        parent,
        text=f'{icone}   {texto}',
        command=comando,
        bg=fundo,
        fg=texto_cor,
        activebackground=hover,
        activeforeground='white',
        relief='flat',
        borderwidth=0,
        highlightthickness=0,
        anchor='w',
        cursor='hand2',
        font=('Segoe UI Semibold', 10),
        padx=14,
        pady=10,
    )
    botao.pack(fill='x', pady=2)
    botao.bind('<Enter>', lambda event: botao.configure(bg=hover))
    botao.bind('<Leave>', lambda event: botao.configure(bg=fundo))
    return botao


def adicionar_secao_menu(titulo, itens):
    tk.Label(
        sidebar_nav,
        text=titulo,
        bg=CORES['sidebar'],
        fg='#64748B',
        font=('Segoe UI Semibold', 8),
    ).pack(anchor='w', padx=12, pady=(14, 6))
    for texto, icone, comando, variante in itens:
        criar_botao_navegacao(sidebar_nav, texto, icone, comando, variante)


adicionar_secao_menu(
    'ARQUIVOS',
    [
        ('Fazer upload', '↑', upload_arquivo, 'primario'),
        ('Selecionar arquivo', '◎', perguntar_arquivo, 'normal'),
        ('Listar arquivos', '☷', listar_arquivos, 'normal'),
        ('Remover arquivo', '−', remover_arquivo, 'perigo'),
    ],
)
adicionar_secao_menu(
    'ANÁLISE',
    [
        ('Visão geral', '▥', graficos_prontos, 'normal'),
        ('Consulta SQL', '⌘', consulta_sql, 'normal'),
    ],
)
adicionar_secao_menu(
    'SISTEMA',
    [
        ('Preparar banco', '＋', criar_tabelas, 'normal'),
        ('Limpar banco', '×', remover_tabelas, 'perigo'),
    ],
)

tk.Frame(sidebar_footer, bg='#1E293B', height=1).pack(fill='x', pady=(0, 12))
criar_botao_navegacao(sidebar_footer, 'Sair', '↪', sair, 'normal')
tk.Label(
    sidebar_footer,
    text='City File Lab  •  ambiente local',
    bg=CORES['sidebar'],
    fg='#475569',
    font=('Segoe UI', 8),
).pack(anchor='w', padx=12, pady=(10, 0))

frame_entry = tk.Frame(frame_chat, bg=CORES['cartao'])
frame_entry.pack(side='bottom', fill='x', before=frame_canvas)
tk.Frame(frame_entry, bg=CORES['borda'], height=1).pack(fill='x')

composer = tk.Frame(frame_entry, bg=CORES['cartao'])
composer.pack(fill='x', padx=22, pady=(15, 8))

entry_container = tk.Frame(
    composer,
    bg='white',
    highlightbackground=CORES['borda'],
    highlightthickness=1,
)
entry_container.pack(side='left', fill='x', expand=True, padx=(0, 10))

entry_enviar = ttk.Entry(entry_container, style='Modern.TEntry')
entry_enviar.pack(fill='x')

botao_enviar = tk.Button(
    composer,
    text='Enviar  →',
    command=enviar_pergunta,
    bg=CORES['primaria'],
    fg='white',
    activebackground=CORES['primaria_hover'],
    activeforeground='white',
    disabledforeground='#E2E8F0',
    relief='flat',
    borderwidth=0,
    highlightthickness=0,
    cursor='hand2',
    font=('Segoe UI Semibold', 10),
    padx=22,
    pady=10,
)
botao_enviar.pack(side='right')

tk.Label(
    frame_entry,
    text='Pressione Enter para enviar. Selecione um arquivo antes de iniciar a conversa.',
    bg=CORES['cartao'],
    fg='#94A3B8',
    font=('Segoe UI', 8),
).pack(anchor='w', padx=23, pady=(0, 13))

entry_enviar.bind('<Return>', lambda event: enviar_pergunta())


if __name__ == '__main__':
    janela.mainloop()
