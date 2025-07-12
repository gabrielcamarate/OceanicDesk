#!/usr/bin/env python3
"""
Script de build para compilar o OceanicDesk em executável
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

def get_version():
    """Lê a versão do arquivo VERSION"""
    try:
        with open('VERSION', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "1.0.0"

def clean_build():
    """Limpa arquivos de build anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removendo {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Remove arquivos .spec antigos
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'OceanicDesk.spec':
            print(f"Removendo {spec_file}...")
            spec_file.unlink()

def check_requirements():
    """Verifica se o PyInstaller está instalado"""
    try:
        import PyInstaller
        print("PyInstaller encontrado!")
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)

def build_exe():
    """Compila o executável"""
    version = get_version()
    exe_name = f"OceanicDesk_v{version}.exe"
    
    print(f"Compilando OceanicDesk v{version}...")
    
    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--icon=images/favicon.ico',
        '--name=OceanicDesk',
        '--add-data=.env;.',
        '--add-data=images/favicon.ico;.',
        '--add-data=images;images',
        '--add-data=config;config',
        '--add-data=planilhas;planilhas',
        '--add-data=capturas_ocr_pyautogui;capturas_ocr_pyautogui',
        'run.py'
    ]
    
    print(f"Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=True)
    
    if result.returncode == 0:
        print("Build concluído com sucesso!")
        
        # Renomeia o executável com a versão
        dist_dir = Path('dist')
        if dist_dir.exists():
            exe_files = list(dist_dir.glob('OceanicDesk.exe'))
            if exe_files:
                old_path = exe_files[0]
                new_path = dist_dir / exe_name
                old_path.rename(new_path)
                print(f"Executável criado: {new_path}")
                
                # Copia o .env para a pasta dist
                if os.path.exists('.env'):
                    shutil.copy2('.env', dist_dir / '.env')
                    print("Arquivo .env copiado para dist/")
                
                # Copia o favicon para a raiz do dist (para garantir que a interface encontre)
                favicon_src = Path('images/favicon.ico')
                if favicon_src.exists():
                    shutil.copy2(favicon_src, dist_dir / 'favicon.ico')
                    print("Favicon copiado para raiz do dist/")
                
                # Copia as pastas necessárias para dist
                folders_to_copy = ['images', 'planilhas', 'capturas_ocr_pyautogui']
                for folder in folders_to_copy:
                    if os.path.exists(folder):
                        folder_dist = dist_dir / folder
                        if folder_dist.exists():
                            shutil.rmtree(folder_dist)
                        shutil.copytree(folder, folder_dist)
                        print(f"Pasta {folder}/ copiada para dist/")
        
        return True
    else:
        print("Erro durante o build!")
        return False

def main():
    """Função principal"""
    print("=== Build do OceanicDesk ===")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Verifica se estamos na pasta correta
    if not os.path.exists('run.py'):
        print("Erro: run.py não encontrado. Execute este script na pasta raiz do projeto.")
        return False
    
    # Verifica se o .env existe
    if not os.path.exists('.env'):
        print("Aviso: Arquivo .env não encontrado na raiz do projeto.")
        print("Certifique-se de que o arquivo .env existe antes de fazer o build.")
    
    # Limpa builds anteriores
    clean_build()
    
    # Verifica dependências
    check_requirements()
    
    # Faz o build
    success = build_exe()
    
    if success:
        print("\n=== Build concluído com sucesso! ===")
        print("O executável está na pasta 'dist/'")
        print("Lembre-se de copiar o arquivo .env para a mesma pasta do executável!")
    else:
        print("\n=== Erro no build ===")
    
    return success

if __name__ == "__main__":
    main() 