# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
from datetime import datetime

class UniversidadeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento Universitário")
        self.root.geometry("1200x700")
        
        # Conectar ao banco
        self.conn = psycopg2.connect(
            dbname="universidade",
            user="postgres",
            password="22201969",
            host="localhost"
        )
        self.cursor = self.conn.cursor()
        
        # Criar interface
        self.create_widgets()
        
        # Carregar opções para os comboboxes
        self.load_combobox_options()
        
    def create_widgets(self):
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de Alunos
        self.alunos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alunos_frame, text='Alunos')
        self.create_alunos_tab()
        
        # Aba de Trabalhos
        self.trabalhos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trabalhos_frame, text='Trabalhos Acadêmicos')
        self.create_trabalhos_tab()
        
        # Aba de Consultas
        self.consultas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.consultas_frame, text='Consultas')
        self.create_consultas_tab()
        
        # Nova aba para gerenciar trabalhos
        self.gerenciar_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.gerenciar_frame, text='Gerenciar Trabalhos')
        self.create_gerenciar_tab()
        
        # Nova aba para atualização de etapas
        self.atualizacao_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.atualizacao_frame, text='Atualização de Trabalhos')
        self.create_atualizacao_tab()
        
    def create_alunos_tab(self):
        # Treeview para exibir alunos
        columns = ("ID", "Nome", "Email", "Curso", "Orientador")
        self.alunos_tree = ttk.Treeview(self.alunos_frame, columns=columns, show='headings')
        
        for col in columns:
            self.alunos_tree.heading(col, text=col)
            self.alunos_tree.column(col, width=100)
        
        self.alunos_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botão para carregar dados
        btn_frame = ttk.Frame(self.alunos_frame)
        btn_frame.pack(fill='x', pady=10)
        
        btn_carregar = ttk.Button(btn_frame, text="Carregar Alunos", command=self.load_alunos)
        btn_carregar.pack(side='left', padx=5)
        
        btn_perfil = ttk.Button(btn_frame, text="Ver Perfil Completo", command=self.show_aluno_profile)
        btn_perfil.pack(side='left', padx=5)
        
        # Botão para adicionar novo aluno
        btn_novo_aluno = ttk.Button(btn_frame, text="Adicionar Novo Aluno", command=self.adicionar_novo_aluno)
        btn_novo_aluno.pack(side='left', padx=5)
        
    def create_trabalhos_tab(self):
        # Treeview para exibir trabalhos
        columns = ("ID", "Título", "Data Submissão", "Aluno", "Orientador")
        self.trabalhos_tree = ttk.Treeview(self.trabalhos_frame, columns=columns, show='headings')
        
        for col in columns:
            self.trabalhos_tree.heading(col, text=col)
            self.trabalhos_tree.column(col, width=150)
        
        self.trabalhos_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botões
        btn_frame = ttk.Frame(self.trabalhos_frame)
        btn_frame.pack(fill='x', pady=10)
        
        btn_carregar = ttk.Button(btn_frame, text="Carregar Trabalhos", command=self.load_trabalhos)
        btn_carregar.pack(side='left', padx=5)
        
    def create_consultas_tab(self):
        # Frame principal
        main_frame = ttk.Frame(self.consultas_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de controles (parte superior)
        ctrl_frame_top = ttk.Frame(main_frame)
        ctrl_frame_top.pack(fill='x', pady=10)
        
        # Botões de consulta
        ttk.Button(ctrl_frame_top, text="Trabalhos e Orientadores", 
                  command=lambda: self.run_query("""
                  SELECT t.titulo, a.nome AS aluno, p.nome AS orientador
                  FROM gerenciamento_trabalhos.Trabalho_Academico t
                  JOIN gerenciamento_trabalhos.Aluno a ON t.id_aluno = a.id_aluno
                  JOIN gerenciamento_trabalhos.Professor p ON t.id_professor = p.id_professor
                  """, 
                  ("Título", "Aluno", "Orientador"))).pack(side='left', padx=5)
        
        ttk.Button(ctrl_frame_top, text="Orientador Mais Ativo", 
                  command=lambda: self.run_query("""
                  SELECT p.nome AS orientador, COUNT(t.id_trabalho) AS total
                  FROM gerenciamento_trabalhos.Professor p
                  JOIN gerenciamento_trabalhos.Trabalho_Academico t ON p.id_professor = t.id_professor
                  GROUP BY p.nome
                  ORDER BY total DESC
                  LIMIT 1
                  """, 
                  ("Orientador", "Total Trabalhos"))).pack(side='left', padx=5)
        
        ttk.Button(ctrl_frame_top, text="Publicações Aprovadas", 
                  command=lambda: self.run_query("""
                  SELECT pub.nome AS publicador, t.titulo, a.data
                  FROM gerenciamento_trabalhos.Aprova a
                  JOIN gerenciamento_trabalhos.Publicador pub ON a.id_publicador = pub.id_publicador
                  JOIN gerenciamento_trabalhos.Trabalho_Academico t ON a.id_trabalho = t.id_trabalho
                  ORDER BY pub.nome, a.data
                  """, 
                  ("Publicador", "Trabalho", "Data Aprovação"))).pack(side='left', padx=5)
        
        ttk.Button(ctrl_frame_top, text="Avaliações", 
                  command=lambda: self.run_query("""
                  SELECT p.nome AS avaliador, ta.titulo AS trabalho
                  FROM gerenciamento_trabalhos.Avalia a
                  JOIN gerenciamento_trabalhos.Trabalho_Academico ta ON a.id_trabalho = ta.id_trabalho
                  JOIN gerenciamento_trabalhos.Professor p ON a.id_professor = p.id_professor
                  """, 
                  ("Avaliador", "Trabalho"))).pack(side='left', padx=5)
        
        # Frame de controles (parte inferior)
        ctrl_frame_bottom = ttk.Frame(main_frame)
        ctrl_frame_bottom.pack(fill='x', pady=10)
        
        # Filtros com combobox
        ttk.Label(ctrl_frame_bottom, text="Filtrar por Curso:").pack(side='left', padx=5)
        self.cursos_combobox = ttk.Combobox(ctrl_frame_bottom, state="readonly", width=30)
        self.cursos_combobox.pack(side='left', padx=5)
        ttk.Button(ctrl_frame_bottom, text="Aplicar", command=self.filtrar_por_curso).pack(side='left', padx=5)
        
        ttk.Label(ctrl_frame_bottom, text="Filtrar por Etapa:").pack(side='left', padx=5)
        self.etapas_combobox = ttk.Combobox(ctrl_frame_bottom, state="readonly", width=30)
        self.etapas_combobox.pack(side='left', padx=5)
        ttk.Button(ctrl_frame_bottom, text="Aplicar", command=self.filtrar_por_etapa).pack(side='left', padx=5)
        
        # Botão adicional
        ttk.Button(ctrl_frame_bottom, text="Visualizar Tabela", command=self.show_tabela_selection).pack(side='left', padx=5)
        
        # Treeview para resultados
        self.consultas_tree = ttk.Treeview(main_frame, show='headings')
        self.consultas_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.consultas_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.consultas_tree.configure(yscrollcommand=scrollbar.set)
        
    def create_gerenciar_tab(self):
        # Frame principal
        main_frame = ttk.Frame(self.gerenciar_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de formulário
        form_frame = ttk.LabelFrame(main_frame, text="Adicionar/Editar Trabalho")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Campos do formulário
        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.titulo_entry = ttk.Entry(form_frame, width=50)
        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(form_frame, text="Data Submissão (AAAA-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.data_entry = ttk.Entry(form_frame)
        self.data_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Frame para aluno
        aluno_frame = ttk.Frame(form_frame)
        aluno_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ttk.Label(aluno_frame, text="Aluno:").pack(side='left', padx=(0, 5))
        self.aluno_combobox = ttk.Combobox(aluno_frame, state="readonly", width=30)
        self.aluno_combobox.pack(side='left', padx=(0, 5))
        ttk.Button(aluno_frame, text="Novo Aluno", command=self.adicionar_novo_aluno).pack(side='left')
        
        # Frame para orientador
        orientador_frame = ttk.Frame(form_frame)
        orientador_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ttk.Label(orientador_frame, text="Orientador:").pack(side='left', padx=(0, 5))
        self.orientador_combobox = ttk.Combobox(orientador_frame, state="readonly", width=30)
        self.orientador_combobox.pack(side='left', padx=(0, 5))
        ttk.Button(orientador_frame, text="Novo Orientador", command=self.adicionar_novo_orientador).pack(side='left')
        
        # Botões do formulário
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.btn_adicionar = ttk.Button(btn_frame, text="Adicionar Trabalho", command=self.adicionar_trabalho)
        self.btn_adicionar.pack(side='left', padx=5)
        
        self.btn_atualizar = ttk.Button(btn_frame, text="Atualizar Trabalho", command=self.atualizar_trabalho, state=tk.DISABLED)
        self.btn_atualizar.pack(side='left', padx=5)
        
        self.btn_limpar = ttk.Button(btn_frame, text="Limpar Formulário", command=self.limpar_formulario)
        self.btn_limpar.pack(side='left', padx=5)
        
        # Treeview para trabalhos
        tree_frame = ttk.LabelFrame(main_frame, text="Trabalhos Cadastrados")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID", "Título", "Data Submissão", "Aluno", "Orientador")
        self.gerenciar_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.gerenciar_tree.heading(col, text=col)
            self.gerenciar_tree.column(col, width=150)
        
        self.gerenciar_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.gerenciar_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.gerenciar_tree.configure(yscrollcommand=scrollbar.set)
        
        # Botão para carregar trabalhos
        btn_frame2 = ttk.Frame(tree_frame)
        btn_frame2.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame2, text="Carregar Trabalhos", command=self.load_gerenciar_trabalhos).pack(side='left', padx=5)
        
        # Evento de seleção na treeview
        self.gerenciar_tree.bind('<<TreeviewSelect>>', self.on_trabalho_select)
        
        # Carregar dados iniciais
        self.load_gerenciar_trabalhos()
    
    def create_atualizacao_tab(self):
        """Cria aba para atualização de etapas de trabalhos"""
        main_frame = ttk.Frame(self.atualizacao_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para seleção de trabalho
        trabalho_frame = ttk.LabelFrame(main_frame, text="Selecionar Trabalho")
        trabalho_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(trabalho_frame, text="Trabalho:").pack(side='left', padx=5)
        self.trabalho_etapa_combobox = ttk.Combobox(trabalho_frame, state="readonly", width=50)
        self.trabalho_etapa_combobox.pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(trabalho_frame, text="Carregar", command=self.carregar_etapas_trabalho).pack(side='left', padx=5)
        
        # Treeview para etapas do trabalho
        etapas_frame = ttk.LabelFrame(main_frame, text="Etapas do Trabalho")
        etapas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("ID Etapa", "Tipo Etapa", "Status", "Prazo", "Funcionário")
        self.etapas_tree = ttk.Treeview(etapas_frame, columns=columns, show='headings')
        
        for col in columns:
            self.etapas_tree.heading(col, text=col)
            self.etapas_tree.column(col, width=120)
        
        self.etapas_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(etapas_frame, orient="vertical", command=self.etapas_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.etapas_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame para atualização de etapas
        atualizar_frame = ttk.LabelFrame(main_frame, text="Atualizar/Adicionar Etapa")
        atualizar_frame.pack(fill='x', padx=10, pady=10)
        
        # Campos do formulário
        ttk.Label(atualizar_frame, text="Tipo Etapa:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.tipo_etapa_combobox = ttk.Combobox(atualizar_frame, state="readonly", width=30)
        self.tipo_etapa_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(atualizar_frame, text="Funcionário:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.funcionario_combobox = ttk.Combobox(atualizar_frame, state="readonly", width=30)
        self.funcionario_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(atualizar_frame, text="Prazo (AAAA-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.prazo_entry = ttk.Entry(atualizar_frame)
        self.prazo_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(atualizar_frame, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.status_combobox = ttk.Combobox(atualizar_frame, state="readonly", values=["Pendente", "Em andamento", "Concluído"])
        self.status_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        # Botões
        btn_frame = ttk.Frame(atualizar_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Adicionar Etapa", command=self.adicionar_etapa).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Atualizar Etapa", command=self.atualizar_etapa).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_formulario_etapa).pack(side='left', padx=5)
        
        # Evento de seleção na treeview
        self.etapas_tree.bind('<<TreeviewSelect>>', self.on_etapa_select)
    
    def load_combobox_options(self):
        """Carrega opções para todos os comboboxes"""
        try:
            # Carregar cursos
            self.cursor.execute("SELECT nome FROM gerenciamento_trabalhos.Curso")
            cursos = [row[0] for row in self.cursor.fetchall()]
            if hasattr(self, 'cursos_combobox') and self.cursos_combobox:
                self.cursos_combobox['values'] = cursos
                if cursos:
                    self.cursos_combobox.current(0)
                
            # Carregar etapas
            self.cursor.execute("SELECT nome FROM gerenciamento_trabalhos.Tipo_Etapa")
            etapas = [row[0] for row in self.cursor.fetchall()]
            if hasattr(self, 'etapas_combobox') and self.etapas_combobox:
                self.etapas_combobox['values'] = etapas
                if etapas:
                    self.etapas_combobox.current(0)
                
            # Carregar alunos
            self.cursor.execute("SELECT id_aluno, nome FROM gerenciamento_trabalhos.Aluno")
            alunos = [f"{row[1]} ({row[0]})" for row in self.cursor.fetchall()]
            if hasattr(self, 'aluno_combobox') and self.aluno_combobox:
                self.aluno_combobox['values'] = alunos
                if alunos:
                    self.aluno_combobox.current(0)
                
            # Carregar professores
            self.cursor.execute("SELECT id_professor, nome FROM gerenciamento_trabalhos.Professor")
            professores = [f"{row[1]} ({row[0]})" for row in self.cursor.fetchall()]
            if hasattr(self, 'orientador_combobox') and self.orientador_combobox:
                self.orientador_combobox['values'] = professores
                if professores:
                    self.orientador_combobox.current(0)
            
            # Carregar trabalhos para aba de atualização
            self.cursor.execute("SELECT id_trabalho, titulo FROM gerenciamento_trabalhos.Trabalho_Academico")
            trabalhos = [f"{row[1]} (ID: {row[0]})" for row in self.cursor.fetchall()]
            if hasattr(self, 'trabalho_etapa_combobox') and self.trabalho_etapa_combobox:
                self.trabalho_etapa_combobox['values'] = trabalhos
                if trabalhos:
                    self.trabalho_etapa_combobox.current(0)
            
            # Carregar tipos de etapa para aba de atualização
            if hasattr(self, 'tipo_etapa_combobox') and self.tipo_etapa_combobox:
                self.tipo_etapa_combobox['values'] = etapas
                if etapas:
                    self.tipo_etapa_combobox.current(0)
            
            # Carregar funcionários
            self.cursor.execute("SELECT id_funcionario, nome FROM gerenciamento_trabalhos.Funcionario")
            funcionarios = [f"{row[1]} ({row[0]})" for row in self.cursor.fetchall()]
            if hasattr(self, 'funcionario_combobox') and self.funcionario_combobox:
                self.funcionario_combobox['values'] = funcionarios
                if funcionarios:
                    self.funcionario_combobox.current(0)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar opções: {str(e)}")
    
    def adicionar_novo_aluno(self):
        """Abre formulário para adicionar novo aluno"""
        form_window = tk.Toplevel(self.root)
        form_window.title("Novo Aluno")
        form_window.geometry("400x300")
        
        # Campos do formulário
        ttk.Label(form_window, text="Nome:").pack(pady=(10, 0))
        nome_entry = ttk.Entry(form_window, width=40)
        nome_entry.pack(pady=5)
        
        ttk.Label(form_window, text="Email:").pack()
        email_entry = ttk.Entry(form_window, width=40)
        email_entry.pack(pady=5)
        
        # Frame para curso
        curso_frame = ttk.Frame(form_window)
        curso_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(curso_frame, text="Curso:").pack(side='left')
        curso_combobox = ttk.Combobox(curso_frame, state="readonly", width=25)
        curso_combobox.pack(side='left', padx=5)
        ttk.Button(curso_frame, text="Novo Curso", command=lambda: self.adicionar_novo_curso(curso_combobox)).pack(side='left')
        
        # Frame para orientador
        orientador_frame = ttk.Frame(form_window)
        orientador_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(orientador_frame, text="Orientador:").pack(side='left')
        orientador_combobox = ttk.Combobox(orientador_frame, state="readonly", width=25)
        orientador_combobox.pack(side='left', padx=5)
        ttk.Button(orientador_frame, text="Novo Orientador", command=lambda: self.adicionar_novo_orientador(orientador_combobox)).pack(side='left')
        
        # Carregar opções para comboboxes
        try:
            self.cursor.execute("SELECT nome FROM gerenciamento_trabalhos.Curso")
            cursos = [row[0] for row in self.cursor.fetchall()]
            curso_combobox['values'] = cursos
            if cursos:
                curso_combobox.current(0)
                
            self.cursor.execute("SELECT id_professor, nome FROM gerenciamento_trabalhos.Professor")
            professores = [f"{row[1]} ({row[0]})" for row in self.cursor.fetchall()]
            orientador_combobox['values'] = professores
            if professores:
                orientador_combobox.current(0)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar opções: {str(e)}")
        
        def salvar_aluno():
            """Salva o novo aluno no banco de dados"""
            nome = nome_entry.get()
            email = email_entry.get()
            curso = curso_combobox.get()
            orientador = orientador_combobox.get()
            
            if not nome or not email or not curso or not orientador:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
                
            try:
                # Obter ID do orientador
                id_orientador = self.get_id_from_combobox(orientador)
                
                # Obter ID do curso
                self.cursor.execute("SELECT id_curso FROM gerenciamento_trabalhos.Curso WHERE nome = %s", (curso,))
                id_curso = self.cursor.fetchone()[0]
                
                # Obter próximo ID disponível
                self.cursor.execute("SELECT MAX(id_aluno) FROM gerenciamento_trabalhos.Aluno")
                max_id = self.cursor.fetchone()[0]
                novo_id = max_id + 1 if max_id else 20180001
                
                # Inserir novo aluno
                self.cursor.execute("""
                    INSERT INTO gerenciamento_trabalhos.Aluno 
                    (id_aluno, nome, email, id_curso, id_professor)
                    VALUES (%s, %s, %s, %s, %s)
                """, (novo_id, nome, email, id_curso, id_orientador))
                
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
                self.load_combobox_options()  # Atualizar comboboxes
                form_window.destroy()
                
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Erro", f"Erro ao adicionar aluno: {str(e)}")
        
        # Botão de salvar
        ttk.Button(form_window, text="Salvar", command=salvar_aluno).pack(pady=10)
    
    def adicionar_novo_orientador(self, combobox_ref=None):
        """Abre formulário para adicionar novo orientador"""
        form_window = tk.Toplevel(self.root)
        form_window.title("Novo Orientador")
        form_window.geometry("400x250")
        
        # Campos do formulário
        ttk.Label(form_window, text="Nome:").pack(pady=(10, 0))
        nome_entry = ttk.Entry(form_window, width=40)
        nome_entry.pack(pady=5)
        
        ttk.Label(form_window, text="Email:").pack()
        email_entry = ttk.Entry(form_window, width=40)
        email_entry.pack(pady=5)
        
        # Frame para curso
        curso_frame = ttk.Frame(form_window)
        curso_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(curso_frame, text="Curso:").pack(side='left')
        curso_combobox = ttk.Combobox(curso_frame, state="readonly", width=25)
        curso_combobox.pack(side='left', padx=5)
        ttk.Button(curso_frame, text="Novo Curso", command=lambda: self.adicionar_novo_curso(curso_combobox)).pack(side='left')
        
        # Carregar opções para combobox
        try:
            self.cursor.execute("SELECT nome FROM gerenciamento_trabalhos.Curso")
            cursos = [row[0] for row in self.cursor.fetchall()]
            curso_combobox['values'] = cursos
            if cursos:
                curso_combobox.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar cursos: {str(e)}")
        
        def salvar_orientador():
            """Salva o novo orientador no banco de dados"""
            nome = nome_entry.get()
            email = email_entry.get()
            curso = curso_combobox.get()
            
            if not nome or not email or not curso:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
                
            try:
                # Obter ID do curso
                self.cursor.execute("SELECT id_curso FROM gerenciamento_trabalhos.Curso WHERE nome = %s", (curso,))
                id_curso = self.cursor.fetchone()[0]
                
                # Obter próximo ID disponível
                self.cursor.execute("SELECT MAX(id_professor) FROM gerenciamento_trabalhos.Professor")
                max_id = self.cursor.fetchone()[0]
                novo_id = max_id + 1 if max_id else 1
                
                # Inserir novo professor
                self.cursor.execute("""
                    INSERT INTO gerenciamento_trabalhos.Professor 
                    (id_professor, nome, email, id_curso)
                    VALUES (%s, %s, %s, %s)
                """, (novo_id, nome, email, id_curso))
                
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Orientador adicionado com sucesso!")
                self.load_combobox_options()  # Atualizar comboboxes
                
                # Atualizar combobox de referência se fornecido
                if combobox_ref:
                    self.cursor.execute("SELECT id_professor, nome FROM gerenciamento_trabalhos.Professor")
                    professores = [f"{row[1]} ({row[0]})" for row in self.cursor.fetchall()]
                    combobox_ref['values'] = professores
                    combobox_ref.current(len(professores) - 1)
                
                form_window.destroy()
                
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Erro", f"Erro ao adicionar orientador: {str(e)}")
        
        # Botão de salvar
        ttk.Button(form_window, text="Salvar", command=salvar_orientador).pack(pady=10)
    
    def adicionar_novo_curso(self, combobox_ref=None):
        """Abre formulário para adicionar novo curso"""
        form_window = tk.Toplevel(self.root)
        form_window.title("Novo Curso")
        form_window.geometry("400x200")
        
        # Campos do formulário
        ttk.Label(form_window, text="Nome do Curso:").pack(pady=(10, 0))
        nome_entry = ttk.Entry(form_window, width=40)
        nome_entry.pack(pady=5)
        
        ttk.Label(form_window, text="Coordenador:").pack()
        coordenador_entry = ttk.Entry(form_window, width=40)
        coordenador_entry.pack(pady=5)
        
        ttk.Label(form_window, text="Departamento:").pack()
        departamento_entry = ttk.Entry(form_window, width=40)
        departamento_entry.pack(pady=5)
        
        def salvar_curso():
            """Salva o novo curso no banco de dados"""
            nome = nome_entry.get()
            coordenador = coordenador_entry.get()
            departamento = departamento_entry.get()
            
            if not nome or not coordenador or not departamento:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
                
            try:
                # Obter próximo ID disponível
                self.cursor.execute("SELECT MAX(id_curso) FROM gerenciamento_trabalhos.Curso")
                max_id = self.cursor.fetchone()[0]
                novo_id = max_id + 1 if max_id else 1
                
                # Inserir novo curso
                self.cursor.execute("""
                    INSERT INTO gerenciamento_trabalhos.Curso 
                    (id_curso, nome, coordenador, departamento)
                    VALUES (%s, %s, %s, %s)
                """, (novo_id, nome, coordenador, departamento))
                
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Curso adicionado com sucesso!")
                self.load_combobox_options()  # Atualizar comboboxes
                
                # Atualizar combobox de referência se fornecido
                if combobox_ref:
                    self.cursor.execute("SELECT nome FROM gerenciamento_trabalhos.Curso")
                    cursos = [row[0] for row in self.cursor.fetchall()]
                    combobox_ref['values'] = cursos
                    combobox_ref.current(len(cursos) - 1)
                
                form_window.destroy()
                
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Erro", f"Erro ao adicionar curso: {str(e)}")
        
        # Botão de salvar
        ttk.Button(form_window, text="Salvar", command=salvar_curso).pack(pady=10)
    
    def carregar_etapas_trabalho(self):
        """Carrega as etapas para o trabalho selecionado"""
        trabalho = self.trabalho_etapa_combobox.get()
        if not trabalho:
            return
            
        try:
            # Extrair ID do trabalho
            id_trabalho = trabalho.split("(ID: ")[1].split(")")[0].strip()
            
            # Limpar treeview
            self.etapas_tree.delete(*self.etapas_tree.get_children())
            
            # Carregar etapas do trabalho
            self.cursor.execute("""
                SELECT e.id_etapa, te.nome, e.status, e.prazo, f.nome
                FROM gerenciamento_trabalhos.Etapa e
                JOIN gerenciamento_trabalhos.Tipo_Etapa te ON e.id_tipo_etapa = te.id_tipo_etapa
                JOIN gerenciamento_trabalhos.Funcionario f ON e.id_funcionario = f.id_funcionario
                WHERE e.id_trabalho = %s
            """, (id_trabalho,))
            
            for row in self.cursor.fetchall():
                self.etapas_tree.insert("", "end", values=row)
                
            # Guardar ID do trabalho selecionado
            self.selected_trabalho_id_etapa = id_trabalho
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar etapas: {str(e)}")
    
    def on_etapa_select(self, event):
        """Preenche o formulário quando uma etapa é selecionada"""
        selected = self.etapas_tree.focus()
        if selected:
            values = self.etapas_tree.item(selected, 'values')
            self.selected_etapa_id = values[0]  # ID da etapa selecionada
            
            # Preencher formulário com dados da etapa
            if hasattr(self, 'tipo_etapa_combobox'):
                for i, etapa in enumerate(self.tipo_etapa_combobox['values']):
                    if values[1] == etapa:
                        self.tipo_etapa_combobox.current(i)
                        break
            
            if hasattr(self, 'funcionario_combobox'):
                for i, func in enumerate(self.funcionario_combobox['values']):
                    if values[4] in func:
                        self.funcionario_combobox.current(i)
                        break
            
            if hasattr(self, 'prazo_entry'):
                self.prazo_entry.delete(0, tk.END)
                self.prazo_entry.insert(0, values[3])
            
            if hasattr(self, 'status_combobox'):
                for i, status in enumerate(self.status_combobox['values']):
                    if values[2] == status:
                        self.status_combobox.current(i)
                        break
    
    def limpar_formulario_etapa(self):
        """Limpa o formulário de etapas"""
        if hasattr(self, 'tipo_etapa_combobox') and self.tipo_etapa_combobox['values']:
            self.tipo_etapa_combobox.current(0)
        if hasattr(self, 'funcionario_combobox') and self.funcionario_combobox['values']:
            self.funcionario_combobox.current(0)
        if hasattr(self, 'prazo_entry'):
            self.prazo_entry.delete(0, tk.END)
        if hasattr(self, 'status_combobox') and self.status_combobox['values']:
            self.status_combobox.current(0)
        
        # Desselecionar item na treeview
        self.etapas_tree.selection_remove(self.etapas_tree.selection())
        
        # Limpar seleção
        if hasattr(self, 'selected_etapa_id'):
            del self.selected_etapa_id
    
    def adicionar_etapa(self):
        """Adiciona uma nova etapa para o trabalho"""
        if not hasattr(self, 'selected_trabalho_id_etapa'):
            messagebox.showerror("Erro", "Selecione um trabalho primeiro!")
            return
            
        tipo_etapa = self.tipo_etapa_combobox.get()
        funcionario = self.funcionario_combobox.get()
        prazo = self.prazo_entry.get()
        status = self.status_combobox.get()
        
        if not tipo_etapa or not funcionario or not prazo or not status:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
            
        try:
            # Validar data
            datetime.strptime(prazo, '%Y-%m-%d')
            
            # Obter IDs
            self.cursor.execute("SELECT id_tipo_etapa FROM gerenciamento_trabalhos.Tipo_Etapa WHERE nome = %s", (tipo_etapa,))
            id_tipo_etapa = self.cursor.fetchone()[0]
            
            id_funcionario = self.get_id_from_combobox(funcionario)
            
            # Obter próximo ID disponível
            self.cursor.execute("SELECT MAX(id_etapa) FROM gerenciamento_trabalhos.Etapa")
            max_id = self.cursor.fetchone()[0]
            novo_id = max_id + 1 if max_id else 1
            
            # Inserir nova etapa
            self.cursor.execute("""
                INSERT INTO gerenciamento_trabalhos.Etapa 
                (id_etapa, prazo, status, id_trabalho, id_funcionario, id_tipo_etapa)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (novo_id, prazo, status, self.selected_trabalho_id_etapa, id_funcionario, id_tipo_etapa))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Etapa adicionada com sucesso!")
            self.carregar_etapas_trabalho()
            self.limpar_formulario_etapa()
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use AAAA-MM-DD")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Erro", f"Erro ao adicionar etapa: {str(e)}")
    
    def atualizar_etapa(self):
        """Atualiza uma etapa existente"""
        if not hasattr(self, 'selected_etapa_id'):
            messagebox.showerror("Erro", "Selecione uma etapa primeiro!")
            return
            
        tipo_etapa = self.tipo_etapa_combobox.get()
        funcionario = self.funcionario_combobox.get()
        prazo = self.prazo_entry.get()
        status = self.status_combobox.get()
        
        if not tipo_etapa or not funcionario or not prazo or not status:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
            
        try:
            # Validar data
            datetime.strptime(prazo, '%Y-%m-%d')
            
            # Obter IDs
            self.cursor.execute("SELECT id_tipo_etapa FROM gerenciamento_trabalhos.Tipo_Etapa WHERE nome = %s", (tipo_etapa,))
            id_tipo_etapa = self.cursor.fetchone()[0]
            
            id_funcionario = self.get_id_from_combobox(funcionario)
            
            # Atualizar etapa
            self.cursor.execute("""
                UPDATE gerenciamento_trabalhos.Etapa
                SET id_tipo_etapa = %s, id_funcionario = %s, prazo = %s, status = %s
                WHERE id_etapa = %s
            """, (id_tipo_etapa, id_funcionario, prazo, status, self.selected_etapa_id))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Etapa atualizada com sucesso!")
            self.carregar_etapas_trabalho()
            self.limpar_formulario_etapa()
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use AAAA-MM-DD")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Erro", f"Erro ao atualizar etapa: {str(e)}")
    
    def filtrar_por_curso(self):
        """Filtra trabalhos por curso selecionado"""
        curso = self.cursos_combobox.get()
        if curso:
            try:
                self.run_query(f"""
                    SELECT t.titulo, a.nome AS aluno, c.nome AS curso
                    FROM gerenciamento_trabalhos.Trabalho_Academico t
                    JOIN gerenciamento_trabalhos.Aluno a ON t.id_aluno = a.id_aluno
                    JOIN gerenciamento_trabalhos.Curso c ON a.id_curso = c.id_curso
                    WHERE c.nome = '{curso}'
                """, ("Trabalho", "Aluno", "Curso"))
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na consulta: {str(e)}")
    
    def filtrar_por_etapa(self):
        """Filtra trabalhos por etapa selecionada"""
        etapa = self.etapas_combobox.get()
        if etapa:
            try:
                self.run_query(f"""
                    SELECT ta.titulo AS trabalho, te.nome AS etapa, e.status, e.prazo
                    FROM gerenciamento_trabalhos.Etapa e
                    JOIN gerenciamento_trabalhos.Tipo_Etapa te ON e.id_tipo_etapa = te.id_tipo_etapa
                    JOIN gerenciamento_trabalhos.Trabalho_Academico ta ON e.id_trabalho = ta.id_trabalho
                    WHERE te.nome = '{etapa}'
                """, ("Trabalho", "Etapa", "Status", "Prazo"))
            except Exception as e:
                messagebox.showerror("Erro", f"Erro na consulta: {str(e)}")
    
    def show_tabela_selection(self):
        """Mostra janela para seleção de tabela"""
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Selecionar Tabela")
        selection_window.geometry("300x150")
        
        ttk.Label(selection_window, text="Selecione uma tabela:").pack(pady=10)
        
        # Combobox com tabelas disponíveis
        tabelas_combobox = ttk.Combobox(selection_window, state="readonly", width=30)
        tabelas_combobox['values'] = [
            'Aluno', 'Professor', 'Curso', 'Trabalho_Academico',
            'Funcionario', 'Tipo_Etapa', 'Etapa', 'Publicador',
            'Comite_Etica', 'Submete', 'Avalia', 'Aprova'
        ]
        tabelas_combobox.current(0)
        tabelas_combobox.pack(pady=5)
        
        ttk.Button(selection_window, text="Visualizar", 
                  command=lambda: self.visualizar_tabela(tabelas_combobox.get(), selection_window)).pack(pady=10)
    
    def visualizar_tabela(self, tabela, window):
        """Visualiza tabela selecionada"""
        if tabela:
            try:
                self.cursor.execute(f"SELECT * FROM gerenciamento_trabalhos.{tabela}")
                
                # Obter nomes das colunas
                colunas = [desc[0] for desc in self.cursor.description]
                
                # Executar consulta para obter dados
                self.run_query(f"SELECT * FROM gerenciamento_trabalhos.{tabela}", colunas)
                
                # Fechar janela de seleção
                window.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao visualizar tabela: {str(e)}")
    
    def load_alunos(self):
        try:
            self.alunos_tree.delete(*self.alunos_tree.get_children())
            self.cursor.execute("""
                SELECT a.id_aluno, a.nome, a.email, c.nome, p.nome 
                FROM gerenciamento_trabalhos.aluno a
                JOIN gerenciamento_trabalhos.curso c ON a.id_curso = c.id_curso
                JOIN gerenciamento_trabalhos.professor p ON a.id_professor = p.id_professor
            """)
            for row in self.cursor.fetchall():
                self.alunos_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar alunos: {str(e)}")
    
    def load_trabalhos(self):
        try:
            self.trabalhos_tree.delete(*self.trabalhos_tree.get_children())
            self.cursor.execute("""
                SELECT t.id_trabalho, t.titulo, t.data_submissao, a.nome, p.nome 
                FROM gerenciamento_trabalhos.trabalho_academico t
                JOIN gerenciamento_trabalhos.aluno a ON t.id_aluno = a.id_aluno
                JOIN gerenciamento_trabalhos.professor p ON t.id_professor = p.id_professor
            """)
            for row in self.cursor.fetchall():
                self.trabalhos_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar trabalhos: {str(e)}")
            
    def load_gerenciar_trabalhos(self):
        try:
            self.gerenciar_tree.delete(*self.gerenciar_tree.get_children())
            self.cursor.execute("""
                SELECT t.id_trabalho, t.titulo, t.data_submissao, a.nome, p.nome 
                FROM gerenciamento_trabalhos.trabalho_academico t
                JOIN gerenciamento_trabalhos.aluno a ON t.id_aluno = a.id_aluno
                JOIN gerenciamento_trabalhos.professor p ON t.id_professor = p.id_professor
            """)
            for row in self.cursor.fetchall():
                self.gerenciar_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar trabalhos: {str(e)}")
            
    def run_query(self, query, columns):
        try:
            # Limpar treeview
            for item in self.consultas_tree.get_children():
                self.consultas_tree.delete(item)
                
            # Configurar colunas
            self.consultas_tree['columns'] = columns
            for col in columns:
                self.consultas_tree.heading(col, text=col)
                self.consultas_tree.column(col, width=150, anchor='w')
            
            # Executar consulta
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            # Inserir resultados
            for row in results:
                self.consultas_tree.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na consulta: {str(e)}")
            
    def show_aluno_profile(self):
        aluno_id = simpledialog.askinteger("Perfil do Aluno", "Digite o ID do aluno:")
        if aluno_id:
            try:
                self.cursor.execute("""
                    SELECT a.nome, t.titulo, p.nome 
                    FROM gerenciamento_trabalhos.Aluno a
                    JOIN gerenciamento_trabalhos.Submete s ON s.id_aluno = a.id_aluno
                    JOIN gerenciamento_trabalhos.Trabalho_Academico t ON t.id_trabalho = s.id_trabalho
                    JOIN gerenciamento_trabalhos.Professor p ON t.id_professor = p.id_professor
                    WHERE a.id_aluno = %s
                """, (aluno_id,))
                
                result = self.cursor.fetchall()
                if result:
                    message = "Perfil do Aluno:\n\n"
                    for row in result:
                        message += f"Nome: {row[0]}\nTrabalho: {row[1]}\nOrientador: {row[2]}\n\n"
                    messagebox.showinfo("Perfil Completo", message)
                else:
                    messagebox.showinfo("Info", "Nenhum dado encontrado para este aluno")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar perfil: {str(e)}")
    
    def on_trabalho_select(self, event):
        """Preenche o formulário quando um trabalho é selecionado"""
        selected = self.gerenciar_tree.focus()
        if selected:
            values = self.gerenciar_tree.item(selected, 'values')
            self.selected_trabalho_id = values[0]  # ID do trabalho selecionado
            
            # Preencher formulário com dados do trabalho
            self.titulo_entry.delete(0, tk.END)
            self.titulo_entry.insert(0, values[1])
            
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, values[2])
            
            # Encontrar aluno e orientador nos comboboxes
            aluno_nome = values[3]
            if hasattr(self, 'aluno_combobox') and self.aluno_combobox['values']:
                for i, aluno in enumerate(self.aluno_combobox['values']):
                    if aluno_nome in aluno:
                        self.aluno_combobox.current(i)
                        break
                    
            orientador_nome = values[4]
            if hasattr(self, 'orientador_combobox') and self.orientador_combobox['values']:
                for i, prof in enumerate(self.orientador_combobox['values']):
                    if orientador_nome in prof:
                        self.orientador_combobox.current(i)
                        break
            
            # Habilitar botão de atualizar
            self.btn_atualizar['state'] = tk.NORMAL
            self.btn_adicionar['state'] = tk.DISABLED
    
    def limpar_formulario(self):
        """Limpa o formulário e reseta os botões"""
        self.titulo_entry.delete(0, tk.END)
        self.data_entry.delete(0, tk.END)
        if hasattr(self, 'aluno_combobox') and self.aluno_combobox['values']:
            self.aluno_combobox.current(0)
        if hasattr(self, 'orientador_combobox') and self.orientador_combobox['values']:
            self.orientador_combobox.current(0)
        
        self.btn_adicionar['state'] = tk.NORMAL
        self.btn_atualizar['state'] = tk.DISABLED
        if hasattr(self, 'gerenciar_tree'):
            self.gerenciar_tree.selection_remove(self.gerenciar_tree.selection())
    
    def get_id_from_combobox(self, combobox_text):
        """Extrai o ID do texto do combobox (formato: Nome (ID))"""
        if '(' in combobox_text and ')' in combobox_text:
            return combobox_text.split('(')[1].split(')')[0].strip()
        return None
    
    def adicionar_trabalho(self):
        """Adiciona um novo trabalho ao banco de dados"""
        titulo = self.titulo_entry.get()
        data = self.data_entry.get()
        aluno = self.aluno_combobox.get()
        orientador = self.orientador_combobox.get()
        
        if not titulo or not data or not aluno or not orientador:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
            
        try:
            # Validar data
            datetime.strptime(data, '%Y-%m-%d')
            
            # Obter IDs dos comboboxes
            id_aluno = self.get_id_from_combobox(aluno)
            id_professor = self.get_id_from_combobox(orientador)
            
            if not id_aluno or not id_professor:
                messagebox.showerror("Erro", "Seleção inválida de aluno ou orientador")
                return
            
            # Obter próximo ID disponível
            self.cursor.execute("SELECT MAX(id_trabalho) FROM gerenciamento_trabalhos.Trabalho_Academico")
            max_id = self.cursor.fetchone()[0]
            novo_id = max_id + 1 if max_id else 1
            
            # Inserir novo trabalho
            self.cursor.execute("""
                INSERT INTO gerenciamento_trabalhos.Trabalho_Academico 
                (id_trabalho, titulo, data_submissao, id_aluno, id_professor)
                VALUES (%s, %s, %s, %s, %s)
            """, (novo_id, titulo, data, id_aluno, id_professor))
            
            # Inserir na tabela Submete
            self.cursor.execute("""
                INSERT INTO gerenciamento_trabalhos.Submete (id_aluno, id_trabalho)
                VALUES (%s, %s)
            """, (id_aluno, novo_id))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Trabalho adicionado com sucesso!")
            self.load_gerenciar_trabalhos()
            self.limpar_formulario()
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use AAAA-MM-DD")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Erro", f"Erro ao adicionar trabalho: {str(e)}")
    
    def atualizar_trabalho(self):
        """Atualiza um trabalho existente"""
        if not hasattr(self, 'selected_trabalho_id'):
            messagebox.showerror("Erro", "Nenhum trabalho selecionado!")
            return
            
        titulo = self.titulo_entry.get()
        data = self.data_entry.get()
        aluno = self.aluno_combobox.get()
        orientador = self.orientador_combobox.get()
        
        if not titulo or not data or not aluno or not orientador:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
            
        try:
            # Validar data
            datetime.strptime(data, '%Y-%m-%d')
            
            # Obter IDs dos comboboxes
            id_aluno = self.get_id_from_combobox(aluno)
            id_professor = self.get_id_from_combobox(orientador)
            
            if not id_aluno or not id_professor:
                messagebox.showerror("Erro", "Seleção inválida de aluno ou orientador")
                return
            
            # Atualizar trabalho
            self.cursor.execute("""
                UPDATE gerenciamento_trabalhos.Trabalho_Academico
                SET titulo = %s, data_submissao = %s, id_aluno = %s, id_professor = %s
                WHERE id_trabalho = %s
            """, (titulo, data, id_aluno, id_professor, self.selected_trabalho_id))
            
            # Atualizar tabela Submete
            self.cursor.execute("""
                UPDATE gerenciamento_trabalhos.Submete
                SET id_aluno = %s
                WHERE id_trabalho = %s
            """, (id_aluno, self.selected_trabalho_id))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Trabalho atualizado com sucesso!")
            self.load_gerenciar_trabalhos()
            self.limpar_formulario()
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use AAAA-MM-DD")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Erro", f"Erro ao atualizar trabalho: {str(e)}")
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversidadeApp(root)
    root.mainloop()