import os
import shutil
from pathlib import Path
from interfaces.alerta_visual import mostrar_alerta_visual


def criar_backup_planilha(caminho_arquivo):
    caminho_arquivo = Path(caminho_arquivo)
    
    # Validação do arquivo original
    if not caminho_arquivo.exists():
        mostrar_alerta_visual("Erro: Arquivo não encontrado", f"Planilha não existe: {caminho_arquivo}", tipo="error")
        raise FileNotFoundError(f"Arquivo original não encontrado: {caminho_arquivo}")
    
    # Criando nome do backup
    backup_path = caminho_arquivo.with_name(
        caminho_arquivo.name.replace(".xlsx", " - BACKUP.xlsx")
    )
    
    if not backup_path.exists():
        try:
            shutil.copy(caminho_arquivo, backup_path)
            print(f"[Backup] Criado em: {backup_path}")
        except Exception as e:
            mostrar_alerta_visual("Erro ao criar backup", f"Erro: {str(e)}", tipo="error")
            raise e
    else:
        ...
    # Verificação final
    if backup_path.exists():
        tamanho_original = caminho_arquivo.stat().st_size
        tamanho_backup = backup_path.stat().st_size
    else:
        mostrar_alerta_visual("Erro: Backup não criado", "Arquivo de backup não encontrado", tipo="error")
        raise FileNotFoundError("Backup não foi criado corretamente")
