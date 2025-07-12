#!/usr/bin/env python3
"""
Teste específico para verificar o carregamento do ícone
"""

import tkinter as tk
import os
import sys
from pathlib import Path

def test_icon_loading():
    """Testa o carregamento do ícone"""
    print("=== Teste de Carregamento do Ícone ===")
    
    # Cria uma janela de teste
    root = tk.Tk()
    root.title("Teste de Ícone")
    root.geometry("300x200")
    
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
            os.path.join(base_dir, 'images', 'favicon.ico'),
            os.path.join(base_dir, 'favicon.ico'),
            os.path.join(base_dir, '..', 'images', 'favicon.ico'),
        ])
    
    # Tenta usar a função de path_utils
    try:
        from utils.path_utils import get_image_path
        ico_path = get_image_path("favicon.ico")
        if ico_path and os.path.exists(ico_path):
            possible_paths.insert(0, ico_path)  # Coloca no início da lista
            print(f"✅ Path utils encontrou: {ico_path}")
    except Exception as e:
        print(f"⚠️ Path utils falhou: {e}")
    
    # Procura o primeiro ícone que existe
    ico_loaded = False
    for ico_path in possible_paths:
        try:
            if os.path.exists(ico_path):
                print(f"📁 Tentando carregar: {ico_path}")
                # Tenta carregar o ícone
                root.iconbitmap(ico_path)
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
                print("✅ ID do aplicativo definido")
        except Exception as e:
            print(f"⚠️ Não foi possível definir ID do aplicativo: {e}")
    
    # Adiciona um label para mostrar o status
    status_text = "✅ Ícone carregado!" if ico_loaded else "❌ Ícone não carregado"
    tk.Label(root, text=status_text, font=("Arial", 12)).pack(pady=20)
    tk.Label(root, text="Feche esta janela para continuar", font=("Arial", 10)).pack()
    
    print(f"\nStatus final: {status_text}")
    print("Janela de teste aberta. Feche-a para continuar.")
    
    # Mostra a janela
    root.mainloop()

if __name__ == "__main__":
    test_icon_loading() 