import tkinter as tk
from tkinter import messagebox
import os
import sys


def coletar_litros_usuario():
    valores = {}

    def confirmar():
        try:
            valores["etanol"] = float(entry_etanol.get())
            valores["aditivada"] = float(entry_aditivada.get())
            valores["diesel"] = float(entry_diesel.get())
            valores["comum"] = float(entry_comum.get())
            janela.quit()
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números válidos.")

    janela = tk.Tk()
    janela.title("OceanicDesk - Inserir Litros do Posto")
    janela.geometry("300x300")
    janela.configure(padx=20, pady=20)
    
    # Carrega o ícone da janela
    _carregar_icone_janela(janela)

    tk.Label(janela, text="Etanol Comum (L):").pack()
    entry_etanol = tk.Entry(janela)
    entry_etanol.pack()

    tk.Label(janela, text="Gasolina Aditivada (L):").pack()
    entry_aditivada = tk.Entry(janela)
    entry_aditivada.pack()

    tk.Label(janela, text="Diesel S10 (L):").pack()
    entry_diesel = tk.Entry(janela)
    entry_diesel.pack()

    tk.Label(janela, text="Gasolina Comum (L):").pack()
    entry_comum = tk.Entry(janela)
    entry_comum.pack()

    tk.Button(janela, text="Confirmar", command=confirmar).pack(pady=15)

    janela.mainloop()

    return (
        valores.get("comum", 0),
        valores.get("aditivada", 0),
        valores.get("diesel", 0),
        valores.get("etanol", 0),
    )


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
