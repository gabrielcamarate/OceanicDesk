import tkinter as tk
from tkinter import ttk
from utils.helpers import calcular_expressao
from utils.financeiro import preenchendo_sangria
from tkinter import messagebox
import os
import sys


def abrir_janela_valores(respostas: dict[str, bool]) -> None:
    """
    Interface gráfica refinada para entrada de valores por forma de pagamento
    e informações úteis no processo de fechamento de caixa.
    """

    # === JANELA ===
    root = tk.Toplevel()

    root.title("OceanicDesk - Fechamento de Caixa – Inserção de Valores")
    root.geometry("700x600")
    root.resizable(False, False)
    
    # Carrega o ícone da janela
    _carregar_icone_janela(root)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f9f9f9")
    style.configure("TLabel", background="#f9f9f9", font=("Segoe UI", 10))
    style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
    style.configure("TEntry", padding=3)

    # === CONTAINER PRINCIPAL ===
    frame_externo = ttk.Frame(root)
    frame_externo.pack(fill="both", expand=True)

    # === CANVAS SCROLL ===
    canvas = tk.Canvas(frame_externo, borderwidth=0, bg="#f9f9f9")
    scrollbar = ttk.Scrollbar(frame_externo, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame_principal = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_principal, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_principal.bind("<Configure>", on_configure)

    # === Separar categorias ===
    formas_pagamento = [
        k for k, v in respostas.items() if v and k not in ["Sangria", "Desconto"]
    ]
    informacoes_uteis = [k for k in ["Sangria", "Desconto"] if respostas.get(k)]
    if not formas_pagamento and not informacoes_uteis:
        messagebox.showinfo(
            "Nada selecionado",
            "Nenhuma forma de pagamento ou informação útil foi marcada.",
        )
        return

    entradas = {}

    def atualizar_total(event, key: str) -> None:
        texto = entradas[key]["entry"].get().replace(",", ".")
        valor = calcular_expressao(texto)
        entradas[key]["label"].config(text=f"Total: R$ {valor:,.2f}")

    # === Seção: Formas de Pagamento ===
    if formas_pagamento:
        frame_pagamento = ttk.LabelFrame(frame_principal, text="Formas de Pagamento")
        frame_pagamento.pack(fill="x", padx=20, pady=(20, 10))

        for item in formas_pagamento:
            linha = ttk.Frame(frame_pagamento)
            linha.pack(fill="x", pady=4, padx=10)

            ttk.Label(linha, text=item, width=20).pack(side="left")
            entry = ttk.Entry(linha, width=18)
            entry.pack(side="left", padx=5)
            entry.insert(0, "")

            label_total = ttk.Label(linha, text="Total: R$ 0.00", width=18)
            label_total.pack(side="left", padx=5)

            entry.bind("<KeyRelease>", lambda e, k=item: atualizar_total(e, k))

            entradas[item] = {"entry": entry, "label": label_total}

    # === Seção: Informações Úteis ===
    if informacoes_uteis:
        frame_infos = ttk.LabelFrame(frame_principal, text="Informações Úteis")
        frame_infos.pack(fill="x", padx=20, pady=(10, 20))

        for item in informacoes_uteis:
            linha = ttk.Frame(frame_infos)
            linha.pack(fill="x", pady=4, padx=10)

            ttk.Label(linha, text=item, width=20).pack(side="left")
            entry_valor = ttk.Entry(linha, width=18)
            entry_valor.pack(side="left", padx=5)
            entry_valor.insert(0, "")

            label_total = ttk.Label(linha, text="Total: R$ 0.00", width=18)
            label_total.pack(side="left", padx=5)

            entry_valor.bind("<KeyRelease>", lambda e, k=item: atualizar_total(e, k))

            entradas[item] = {"entry": entry_valor, "label": label_total}

            if item == "Sangria":
                ttk.Label(linha, text="Operador:", width=10).pack(
                    side="left", padx=(15, 2)
                )
                entry_operador = ttk.Entry(linha, width=15)
                entry_operador.pack(side="left", padx=5)
                entradas[item]["operador"] = entry_operador

    # === Finalização ===
    def on_submit() -> None:
        resultados_finais = {}
        for chave, widgets in entradas.items():
            valor_str = widgets["entry"].get().replace(",", ".")
            valor_calc = calcular_expressao(valor_str)
            operador = widgets.get("operador").get() if "operador" in widgets else None
            resultados_finais[chave] = {
                "valor": valor_calc,
                "texto": valor_str,
                "operador": operador,
            }

        # 🔽 NOVO TRECHO
        from utils.duplicata_ocr import preencher_cartoes_com_duplicatas

        root.destroy()

        if "Sangria" in resultados_finais:
            dados = resultados_finais["Sangria"]
            if dados["valor"] > 0 and dados["operador"]:
                preenchendo_sangria(dados["texto"], dados["operador"])

        # Cartões
        preencher_cartoes_com_duplicatas(resultados_finais)

    # === Botão fixo no rodapé ===
    frame_botao = ttk.Frame(root)
    frame_botao.pack(fill="x", padx=20, pady=(5, 15))

    btn = ttk.Button(frame_botao, text="Finalizar", command=on_submit)
    btn.pack(anchor="center")

    root.mainloop()


def _carregar_icone_janela(janela):
    """
    Carrega o ícone da janela com múltiplas tentativas e fallbacks
    """
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
        from utils.path_utils import get_image_path
        ico_path = get_image_path("favicon.ico")
        if ico_path and os.path.exists(ico_path):
            possible_paths.insert(0, ico_path)  # Coloca no início da lista
    except Exception:
        pass
    
    # Procura o primeiro ícone que existe
    for ico_path in possible_paths:
        try:
            if os.path.exists(ico_path):
                # Tenta carregar o ícone
                janela.iconbitmap(ico_path)
                print(f"✅ Ícone carregado com sucesso: {ico_path}")
                break
            else:
                print(f"⚠️ Ícone não encontrado: {ico_path}")
        except Exception as e:
            print(f"❌ Erro ao carregar ícone {ico_path}: {e}")
            continue
