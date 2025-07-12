# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env', '.'),  # Inclui o arquivo .env na raiz do executável
        ('images/favicon.ico', 'images/'),  # Inclui o favicon na pasta images
        ('images/favicon.ico', '.'),  # Inclui o favicon também na raiz do executável
        ('images/', 'images/'),  # Inclui a pasta de imagens completa
        ('config/', 'config/'),  # Inclui a pasta de configuração
        ('planilhas/', 'planilhas/'),  # Inclui a pasta de planilhas
        ('capturas_ocr_pyautogui/', 'capturas_ocr_pyautogui/'),  # Inclui as capturas de tela para OCR
    ],
    hiddenimports=[
        'dotenv',
        'openpyxl',
        'tkinter',
        'pyautogui',
        'selenium',
        'pandas',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OceanicDesk',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para aplicação GUI sem console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='images/favicon.ico',  # Ícone do aplicativo
) 