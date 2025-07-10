import tkinter as tk
from tkinter import ttk


def coletar_formas_pagamento() -> dict[str, bool]:
    """
    Abre uma interface gráfica para seleção das formas de pagamento e informações adicionais.
    Retorna um dicionário com as opções marcadas pelo usuário.
    """

    respostas = {}
    opcoes = {}

    def on_confirm():
        for texto, var in opcoes.items():
            respostas[texto] = var.get()
        root.quit()

    # === JANELA ===
    root = tk.Toplevel()
    root.title("Fechamento de Caixa – Formas de Pagamento")
    root.geometry("700x400")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f4f4f4")
    style.configure("TLabel", background="#f4f4f4", font=("Segoe UI", 10))
    style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))

    container = ttk.Frame(root)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # === Formas de pagamento ===
    frame_pagamento = ttk.LabelFrame(container, text="Formas de Pagamento")
    frame_pagamento.grid(row=0, column=0, sticky="nw", padx=10)

    formas_pagamento = [
        "GOOCARD",
        "PRIME",
        "PREPAGO MASTER",
        "PREPAGO VISA",
        "PREPAGO ELO",
        "MASTERCARD DEB",
        "MASTERCARD CRED",
        "PLUXE",
        "VR",
        "VISA CRED",
        "VISA DEB",
        "ALELO",
        "AMEX",
        "ELO CRED",
        "ELO DEB",
        "FITCARD",
        "PIX",
        "NEO",
        "WIZEL",
        "AGILE",
        "LINK"
    ]

    col, row = 0, 0
    for item in formas_pagamento:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_pagamento, text=item, variable=var)
        chk.grid(row=row, column=col, sticky="w", padx=5, pady=2)
        opcoes[item] = var

        row += 1
        if row > 5:
            row = 0
            col += 1

    # === Informações adicionais ===
    frame_infos = ttk.LabelFrame(container, text="Informações Úteis")
    frame_infos.grid(row=0, column=1, sticky="nw", padx=30)

    informacoes_uteis = ["Sangria", "Desconto"]
    for item in informacoes_uteis:
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(frame_infos, text=item, variable=var)
        chk.pack(anchor="w", pady=2)
        opcoes[item] = var

    # === Botão de confirmação ===
    frame_botao = ttk.Frame(root)
    frame_botao.pack(pady=(0, 15))

    ttk.Button(frame_botao, text="Confirmar", command=on_confirm).pack()

    root.mainloop()
    root.destroy()

    return respostas
