#!/usr/bin/env python3
"""
Script de teste para verificar se o favicon e .env estão funcionando
"""

import os
import sys
from pathlib import Path

def test_env_loading():
    """Testa se o .env está sendo carregado corretamente"""
    print("=== Teste de Carregamento do .env ===")
    
    try:
        import config
        print("✅ Config carregado com sucesso!")
        
        # Verifica se as variáveis estão definidas
        from config import CAMINHO_PLANILHA, LOGIN_SISTEMA, SENHA_SISTEMA
        print(f"✅ CAMINHO_PLANILHA: {'Definido' if CAMINHO_PLANILHA else 'Não definido'}")
        print(f"✅ LOGIN_SISTEMA: {'Definido' if LOGIN_SISTEMA else 'Não definido'}")
        print(f"✅ SENHA_SISTEMA: {'Definido' if SENHA_SISTEMA else 'Não definido'}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar config: {e}")
        return False

def test_favicon_path():
    """Testa se o favicon pode ser encontrado"""
    print("\n=== Teste do Favicon ===")
    
    possible_paths = []
    
    # Se é um executável PyInstaller
    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent
        possible_paths.extend([
            exe_dir / "images" / "favicon.ico",
            exe_dir / "favicon.ico"
        ])
    
    # Caminho do script atual
    script_dir = Path(__file__).parent
    possible_paths.extend([
        script_dir / "images" / "favicon.ico",
        script_dir / "favicon.ico"
    ])
    
    # Pasta atual de trabalho
    possible_paths.append(Path.cwd() / "images" / "favicon.ico")
    possible_paths.append(Path.cwd() / "favicon.ico")
    
    found_paths = []
    for path in possible_paths:
        if path.exists():
            found_paths.append(path)
            print(f"✅ Favicon encontrado: {path}")
    
    if not found_paths:
        print("❌ Favicon não encontrado nos caminhos:")
        for path in possible_paths:
            print(f"   - {path}")
        return False
    
    return True

def test_required_folders():
    """Testa se as pastas necessárias existem"""
    print("\n=== Teste das Pastas Necessárias ===")
    
    required_folders = [
        ('images', 'Pasta de ícones'),
        ('planilhas', 'Pasta de planilhas'),
        ('capturas_ocr_pyautogui', 'Pasta de capturas OCR'),
        ('config', 'Pasta de configuração')
    ]
    
    all_found = True
    for folder, description in required_folders:
        folder_path = Path(folder)
        if folder_path.exists():
            print(f"✅ {description} encontrada: {folder_path}")
            
            # Lista alguns arquivos importantes
            if folder == 'images':
                favicon = folder_path / 'favicon.ico'
                if favicon.exists():
                    print(f"   📄 favicon.ico: OK")
                else:
                    print(f"   ❌ favicon.ico: NÃO ENCONTRADO")
                    all_found = False
            
            elif folder == 'planilhas':
                excel_files = list(folder_path.glob('*.xlsx'))
                if excel_files:
                    print(f"   📊 Planilhas encontradas: {len(excel_files)}")
                    for file in excel_files[:2]:  # Mostra apenas os 2 primeiros
                        print(f"      - {file.name}")
                else:
                    print(f"   ❌ Nenhuma planilha .xlsx encontrada")
                    all_found = False
            
            elif folder == 'capturas_ocr_pyautogui':
                png_files = list(folder_path.glob('*.png'))
                if png_files:
                    print(f"   🖼️ Capturas encontradas: {len(png_files)}")
                    for file in png_files[:3]:  # Mostra apenas os 3 primeiros
                        print(f"      - {file.name}")
                else:
                    print(f"   ❌ Nenhuma captura .png encontrada")
                    all_found = False
        else:
            print(f"❌ {description} não encontrada: {folder_path}")
            all_found = False
    
    return all_found

def test_interface_icon():
    """Testa se a interface consegue carregar o ícone"""
    print("\n=== Teste da Interface ===")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Esconde a janela
        
        # Simula o código da interface
        import os
        import sys
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
            ico_path = os.path.join(base_dir, 'images', 'favicon.ico')
            if not os.path.exists(ico_path):
                ico_path = os.path.join(base_dir, 'favicon.ico')
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            ico_path = os.path.join(base_dir, 'images', 'favicon.ico')
            if not os.path.exists(ico_path):
                ico_path = os.path.join(base_dir, 'favicon.ico')
        
        if os.path.exists(ico_path):
            root.iconbitmap(ico_path)
            print(f"✅ Ícone da interface carregado: {ico_path}")
            root.destroy()
            return True
        else:
            print(f"❌ Ícone da interface não encontrado: {ico_path}")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar interface: {e}")
        return False

def test_path_utils():
    """Testa as funções de utilitário de caminhos"""
    print("\n=== Teste das Funções de Caminho ===")
    
    try:
        from utils.path_utils import get_captura_path, get_planilha_path, get_image_path, get_system_path, get_desktop_path, debug_paths
        
        # Testa debug_paths
        debug_paths()
        
        # Testa get_captura_path
        captura_path = get_captura_path("autosystem_login.png")
        if captura_path and os.path.exists(captura_path):
            print(f"✅ get_captura_path: {captura_path}")
        else:
            print(f"❌ get_captura_path falhou: {captura_path}")
            return False
        
        # Testa get_planilha_path
        planilha_path = get_planilha_path("Vendas Julho.xlsx")
        if planilha_path and os.path.exists(planilha_path):
            print(f"✅ get_planilha_path: {planilha_path}")
        else:
            print(f"❌ get_planilha_path falhou: {planilha_path}")
            return False
        
        # Testa get_image_path
        image_path = get_image_path("favicon.ico")
        if image_path and os.path.exists(image_path):
            print(f"✅ get_image_path: {image_path}")
        else:
            print(f"❌ get_image_path falhou: {image_path}")
            return False
        
        # Testa get_desktop_path
        desktop_path = get_desktop_path()
        if desktop_path and os.path.exists(desktop_path):
            print(f"✅ get_desktop_path: {desktop_path}")
        else:
            print(f"❌ get_desktop_path falhou: {desktop_path}")
            return False
        
        # Testa get_system_path (apenas verifica se não gera erro)
        try:
            autosystem_path = get_system_path("autosystem")
            print(f"✅ get_system_path (autosystem): {autosystem_path}")
            
            emsys3_path = get_system_path("emsys3")
            print(f"✅ get_system_path (emsys3): {emsys3_path}")
            
            tesseract_path = get_system_path("tesseract")
            print(f"✅ get_system_path (tesseract): {tesseract_path}")
        except Exception as e:
            print(f"⚠️ get_system_path: {e} (pode ser normal se programas não estiverem instalados)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar path_utils: {e}")
        return False

def main():
    """Função principal"""
    print("=== Teste de Build do OceanicDesk ===")
    print(f"Data/Hora: {os.popen('date /t & time /t').read().strip()}")
    print(f"Pasta atual: {Path.cwd()}")
    print(f"Executável: {sys.executable}")
    print(f"Frozen: {getattr(sys, 'frozen', False)}")
    
    # Executa os testes
    env_ok = test_env_loading()
    favicon_ok = test_favicon_path()
    folders_ok = test_required_folders()
    interface_ok = test_interface_icon()
    path_utils_ok = test_path_utils()
    
    print("\n=== Resumo dos Testes ===")
    print(f"📄 .env: {'✅ OK' if env_ok else '❌ FALHOU'}")
    print(f"🎨 Favicon: {'✅ OK' if favicon_ok else '❌ FALHOU'}")
    print(f"📁 Pastas: {'✅ OK' if folders_ok else '❌ FALHOU'}")
    print(f"🖥️ Interface: {'✅ OK' if interface_ok else '❌ FALHOU'}")
    print(f"🛠️ Path Utils: {'✅ OK' if path_utils_ok else '❌ FALHOU'}")
    
    if all([env_ok, favicon_ok, folders_ok, interface_ok, path_utils_ok]):
        print("\n🎉 Todos os testes passaram! O build deve funcionar corretamente.")
        return True
    else:
        print("\n⚠️ Alguns testes falharam. Verifique os problemas acima.")
        return False

if __name__ == "__main__":
    main() 