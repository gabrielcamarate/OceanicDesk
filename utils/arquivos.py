import os
import shutil


def criar_backup_planilha(caminho_arquivo):
    backup_path = caminho_arquivo.with_name(
        caminho_arquivo.name.replace(".xlsx", " - BACKUP.xlsx")
    )
    if not backup_path.exists():
        shutil.copy(caminho_arquivo, backup_path)
        print(f"[Backup] Criado em: {backup_path}")
    else:
        print(f"[Backup] Já existe: {backup_path}")
