import tkinter as tk
from tkinter import filedialog, messagebox
from config import MODO_DEV
from utils.logger import registrar_log
from interfaces.alerta_visual import mostrar_alerta_visual


class JanelaPrincipal:
    def __init__(self, root, control):
        self.root = root
        self.control = control
        self.caminho_planilha_dinamico = None

        self.root.title("OceanicDesk - Painel de Controle - Relatórios Oceanico")
        self.root.geometry("650x600")
        self.root.configure(padx=10, pady=10)
        
        # Carrega o ícone da janela
        self._carregar_icone()

        self._criar_interface()
        mostrar_alerta_visual("Bem-vindo ao OceanicDesk!", "Sistema pronto para uso.", tipo="info")

    def _carregar_icone(self):
        """
        Carrega o ícone da janela com múltiplas tentativas e fallbacks
        """
        import os
        import sys
        from utils.path_utils import get_image_path
        
        # Lista de possíveis caminhos para o ícone
        possible_paths = []
        
        if getattr(sys, 'frozen', False):
            # Se é um executável PyInstaller
            base_dir = os.path.dirname(sys.executable)
            possible_paths.extend([
                os.path.join(base_dir, 'images', 'favicon.ico'),
                os.path.join(base_dir, 'favicon.ico'),
                os.path.join(base_dir, '..', 'images', 'favicon.ico'),
            ])
        else:
            # Se é desenvolvimento
            base_dir = os.path.dirname(os.path.abspath(__file__))
            possible_paths.extend([
                os.path.join(base_dir, '..', 'images', 'favicon.ico'),
                os.path.join(base_dir, '..', 'favicon.ico'),
                os.path.join(base_dir, 'images', 'favicon.ico'),
            ])
        
        # Tenta usar a função de path_utils
        try:
            ico_path = get_image_path("favicon.ico")
            if ico_path and os.path.exists(ico_path):
                possible_paths.insert(0, ico_path)  # Coloca no início da lista
        except Exception:
            pass
        
        # Procura o primeiro ícone que existe
        ico_loaded = False
        for ico_path in possible_paths:
            try:
                if os.path.exists(ico_path):
                    # Tenta carregar o ícone
                    self.root.iconbitmap(ico_path)
                    print(f"✅ Ícone carregado com sucesso: {ico_path}")
                    ico_loaded = True
                    break
                else:
                    print(f"⚠️ Ícone não encontrado: {ico_path}")
            except Exception as e:
                print(f"❌ Erro ao carregar ícone {ico_path}: {e}")
                continue
        
        if not ico_loaded:
            print("❌ Nenhum ícone foi carregado. Usando ícone padrão do sistema.")
            # Tenta definir um ícone padrão do Windows
            try:
                if os.name == 'nt':  # Windows
                    import ctypes
                    myappid = 'oceanicdesk.app.1.0'  # ID único para o aplicativo
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception as e:
                print(f"⚠️ Não foi possível definir ID do aplicativo: {e}")

    def _criar_interface(self):
        tk.Label(self.root, text="Painel de Etapas", font=("Arial", 12, "bold")).pack(
            pady=5
        )

        canvas = tk.Canvas(self.root, height=400)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        etapas = [
            (
                "[1] Criar Backup e Atualizar Preços",
                lambda: self._perguntar_continuar(self.control.etapa1, 1),
            ),
            (
                "[2] Relatório Mini-mercado",
                lambda: self._perguntar_continuar(self.control.etapa2, 2),
            ),
            (
                "[3] Relatório Litros e Descontos",
                lambda: self._perguntar_continuar(self.control.etapa3, 3),
            ),
            (
                "[4] Relatório Cashback e Pix",
                lambda: self._perguntar_continuar(self.control.etapa4, 4),
            ),
            (
                "[5] Inserir Litros Manualmente",
                lambda: self._perguntar_continuar(self.control.etapa5, 5),
            ),
            (
                "[6] Enviar Relatório de Vendas",
                lambda: self._perguntar_continuar(self.control.etapa6, 6),
            ),
            (
                "[7] Fechamento de Caixa",
                lambda: self._perguntar_continuar(self.control.etapa7, 7),
            ),
            (
                "[8] Projeção de vendas",
                lambda: self._perguntar_continuar(self.control.etapa8, 8),
            ),
            ("[▶] Executar Processo Completo", self.control.executar_todas),
        ]

        for texto, comando in etapas:
            tk.Button(
                scroll_frame, text=texto, command=comando, width=40, height=2
            ).pack(pady=4)

        tk.Button(
            self.root, text="Selecionar Planilha", command=self._selecionar_planilha
        ).pack(pady=6)

        tk.Button(
            self.root, text="Sobre", command=self._mostrar_sobre
        ).pack(pady=2)

        self.painel_log = tk.Text(self.root, height=6, width=70, bg="#f4f4f4")
        self.painel_log.pack(pady=6)

        self.log_buffer = []
        self.modo_dev = MODO_DEV
        self._atualizar_painel("Pronto para iniciar...")

        tk.Checkbutton(
            self.root, text="Modo Desenvolvedor", command=self._alternar_modo
        ).pack()

        tk.Button(
            self.root,
            text="[⏹] Fechar",
            command=self.root.quit,
            width=40,
            height=2,
            bg="tomato",
        ).pack(pady=10)

    def _perguntar_continuar(self, funcao_etapa, etapa_numero):
        resposta = messagebox.askquestion(
            f"Etapa {etapa_numero}",
            "Deseja executar apenas esta etapa?\nClique em 'Não' para continuar até o final.",
        )
        funcao_etapa(completo=(resposta == "no"))

    def _selecionar_planilha(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha", filetypes=[("Excel files", "*.xlsx")]
        )
        if caminho:
            self.caminho_planilha_dinamico = caminho
            messagebox.showinfo(
                "Planilha selecionada", f"Planilha definida:\n{caminho}"
            )
            mostrar_alerta_visual("Planilha selecionada", f"{caminho}", tipo="success")
        else:
            mostrar_alerta_visual("Seleção cancelada", "Nenhuma planilha foi selecionada.", tipo="info")

    def _atualizar_painel(self, texto):
        if self.modo_dev:
            self.log_buffer.append(texto)
            self.painel_log.delete("1.0", tk.END)
            self.painel_log.insert(tk.END, "\n".join(self.log_buffer[-100:]))
        else:
            self.painel_log.delete("1.0", tk.END)
            self.painel_log.insert(tk.END, texto)

    def _alternar_modo(self):
        self.modo_dev = not self.modo_dev
        if self.modo_dev:
            mostrar_alerta_visual("Modo desenvolvedor ativado", "Logs detalhados serão exibidos.", tipo="dev")
        else:
            mostrar_alerta_visual("Modo simples ativado", "Logs resumidos.", tipo="info")
        self._atualizar_painel(
            "Modo desenvolvedor ativado." if self.modo_dev else "Modo simples."
        )

    def log_mensagem(self, mensagem):
        self._atualizar_painel(mensagem)
        if self.modo_dev:
            registrar_log(mensagem)

    def obter_caminho_planilha_dinamico(self):
        return self.caminho_planilha_dinamico

    def _mostrar_sobre(self):
        # Tenta ler a versão do arquivo VERSION
        try:
            import os, sys
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            version_path = os.path.join(base_dir, '..', 'VERSION')
            if os.path.exists(version_path):
                with open(version_path, 'r', encoding='utf-8') as f:
                    versao = f.read().strip()
            else:
                versao = 'desconhecida'
        except Exception:
            versao = 'desconhecida'
        messagebox.showinfo(
            "Sobre",
            f"Automação de Relatórios - Posto Oceanico\n\nAutor: Gabriel Camarate\nContato: gabrielcamarate@icloud.com\nLinkedIn: linkedin.com/in/gabrielcamarate\n\nVersão: {versao}\n\nPara dúvidas ou suporte, entre em contato."
        )
