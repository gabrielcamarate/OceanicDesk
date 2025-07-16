"""
Utilitários para resolver caminhos de arquivos em desenvolvimento e quando compilado
"""

import os
import sys
from pathlib import Path
from interfaces.alerta_visual import mostrar_alerta_visual


def get_project_root():
    """
    Retorna o caminho raiz do projeto, funcionando tanto em desenvolvimento quanto quando compilado
    """
    if getattr(sys, 'frozen', False):
        # Se é um executável PyInstaller
        return Path(sys.executable).parent
    else:
        # Se é desenvolvimento, retorna a pasta raiz do projeto
        return Path(__file__).parent.parent


def find_file_in_project(filename, subfolder=None):
    """
    Procura um arquivo no projeto, funcionando tanto em desenvolvimento quanto quando compilado
    
    Args:
        filename (str): Nome do arquivo a procurar
        subfolder (str, optional): Subpasta onde procurar
    
    Returns:
        Path: Caminho completo do arquivo encontrado ou None se não encontrado
    """
    project_root = get_project_root()
    
    # Lista de possíveis locais para procurar
    search_paths = []
    
    if subfolder:
        # Procura na subpasta especificada
        search_paths.extend([
            project_root / subfolder / filename,
            project_root / filename,  # Fallback na raiz
        ])
    else:
        # Procura em locais comuns
        search_paths.extend([
            project_root / filename,
            project_root / "images" / filename,
            project_root / "capturas_ocr_pyautogui" / filename,
            project_root / "planilhas" / filename,
        ])
    
    # Procura o primeiro arquivo que existe
    for path in search_paths:
        if path.exists():
            return path
    
    # Se não encontrou, retorna None
    return None


def get_captura_path(filename):
    """
    Obtém o caminho de uma imagem de captura, funcionando tanto em desenvolvimento quanto quando compilado
    
    Args:
        filename (str): Nome do arquivo de imagem (ex: 'autosystem_login.png')
    
    Returns:
        str: Caminho completo da imagem
    """
    path = find_file_in_project(filename, "capturas_ocr_pyautogui")
    if path:
        return str(path)
    else:
        # Fallback para o caminho antigo (para compatibilidade)
        project_root = get_project_root()
        return str(project_root / "capturas_ocr_pyautogui" / filename)


def get_planilha_path(filename):
    """
    Obtém o caminho de uma planilha, funcionando tanto em desenvolvimento quanto quando compilado
    
    Args:
        filename (str): Nome do arquivo da planilha (ex: 'Vendas Julho.xlsx')
    
    Returns:
        str: Caminho completo da planilha
    """
    path = find_file_in_project(filename, "planilhas")
    if path:
        return str(path)
    else:
        # Fallback para o caminho antigo (para compatibilidade)
        project_root = get_project_root()
        return str(project_root / "planilhas" / filename)


def get_image_path(filename):
    """
    Obtém o caminho de uma imagem, funcionando tanto em desenvolvimento quanto quando compilado
    
    Args:
        filename (str): Nome do arquivo de imagem (ex: 'favicon.ico')
    
    Returns:
        str: Caminho completo da imagem
    """
    path = find_file_in_project(filename, "images")
    if path:
        return str(path)
    else:
        # Fallback para o caminho antigo (para compatibilidade)
        project_root = get_project_root()
        return str(project_root / "images" / filename)


def get_system_path(program_name):
    """
    Obtém o caminho de um programa do sistema, com fallbacks para diferentes instalações
    
    Args:
        program_name (str): Nome do programa ('autosystem', 'emsys3', 'tesseract')
    
    Returns:
        str: Caminho completo do programa
    """
    if program_name.lower() == "autosystem":
        # Caminhos possíveis para o AutoSystem
        possible_paths = [
            r"c:\ProgramData\Microsoft\Windows\Start Menu\Programs\AutoSystem\AutoSystem - Gerencial.lnk",
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AutoSystem\AutoSystem - Gerencial.lnk",
            r"C:\Program Files\AutoSystem\AutoSystem.exe",
            r"C:\Program Files (x86)\AutoSystem\AutoSystem.exe",
        ]
        
    elif program_name.lower() == "emsys3":
        # Caminhos possíveis para o EMSys3
        possible_paths = [
            r"c:\Rezende\EMSys3\EMSys3.exe",
            r"C:\Rezende\EMSys3\EMSys3.exe",
            r"C:\Program Files\Rezende\EMSys3\EMSys3.exe",
            r"C:\Program Files (x86)\Rezende\EMSys3\EMSys3.exe",
        ]
        
    elif program_name.lower() == "tesseract":
        # Caminhos possíveis para o Tesseract
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\Usuario\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
        ]
        
    else:
        mostrar_alerta_visual("Programa não reconhecido", f"'{program_name}' não suportado", tipo="error")
        raise ValueError(f"Programa '{program_name}' não reconhecido")
    
    # Procura o primeiro caminho que existe
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Se não encontrou, mostra aviso e retorna o primeiro caminho como fallback
    mostrar_alerta_visual(f"{program_name} não encontrado", f"Usando fallback: {possible_paths[0]}", tipo="warning")
    return possible_paths[0]


def get_desktop_path():
    """
    Obtém o caminho da área de trabalho do usuário
    
    Returns:
        str: Caminho completo da área de trabalho
    """
    return os.path.join(os.path.expanduser("~"), "Desktop")


def debug_paths():
    """
    Função de debug para mostrar onde os arquivos estão sendo procurados
    """
    mostrar_alerta_visual("Debug de Caminhos", "Verificando estrutura do projeto...", tipo="info")
    
    print("=== Debug de Caminhos ===")
    print(f"Projeto raiz: {get_project_root()}")
    print(f"Frozen: {getattr(sys, 'frozen', False)}")
    print(f"Desktop: {get_desktop_path()}")
    
    # Testa alguns arquivos importantes
    test_files = [
        ("capturas_ocr_pyautogui", "autosystem_login.png"),
        ("capturas_ocr_pyautogui", "emsys_login.png"),
        ("images", "favicon.ico"),
        ("planilhas", "Vendas Julho.xlsx"),
    ]
    
    arquivos_encontrados = 0
    for folder, filename in test_files:
        path = find_file_in_project(filename, folder)
        if path:
            print(f"✅ {folder}/{filename}: {path}")
            arquivos_encontrados += 1
        else:
            print(f"❌ {folder}/{filename}: NÃO ENCONTRADO")
    
    # Testa caminhos de sistema
    system_programs = ["autosystem", "emsys3", "tesseract"]
    programas_encontrados = 0
    for program in system_programs:
        try:
            path = get_system_path(program)
            if os.path.exists(path):
                print(f"✅ {program}: {path}")
                programas_encontrados += 1
            else:
                print(f"⚠️ {program}: {path} (não encontrado)")
        except Exception as e:
            print(f"❌ {program}: {e}")
    
    print("========================")
    
    mostrar_alerta_visual("Debug concluído", f"{arquivos_encontrados} arquivos e {programas_encontrados} programas encontrados", tipo="success") 