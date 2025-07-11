import tkinter as tk
from tkinter import filedialog, messagebox
from config import MODO_DEV
from utils.logger import registrar_log


class JanelaPrincipal:
    def __init__(self, root, control):
        self.root = root
        self.control = control
        self.caminho_planilha_dinamico = None

        self.root.title("Painel de Controle - Relatórios Oceanico")
        self.root.geometry("650x600")
        self.root.configure(padx=10, pady=10)
        try:
            import os
            import sys
            from tkinter import PhotoImage
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(base_dir, '..', 'images', 'logo.png')
            if os.path.exists(logo_path):
                logo_img = PhotoImage(file=logo_path)
                self.root.iconphoto(True, logo_img)
        except Exception as e:
            print(f"[Aviso] Não foi possível definir o ícone da janela: {e}")

        self._criar_interface()

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
        messagebox.showinfo(
            "Sobre",
            "Automação de Relatórios - Posto Oceanico\n\nAutor: Gabriel Camarate\nContato: gabrielcamarate@icloud.com\nLinkedIn: linkedin.com/in/gabrielcamarate\n\nVersão: 1.0\n\nPara dúvidas ou suporte, entre em contato."
        )
