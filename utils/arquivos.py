import os
import shutil
from pathlib import Path
from interfaces.alerta_visual import mostrar_alerta_visual


def criar_backup_planilha(caminho_arquivo):
    mostrar_alerta_visual("Iniciando backup", f"Arquivo: {os.path.basename(caminho_arquivo)}", tipo="info")
    
    caminho_arquivo = Path(caminho_arquivo)
    
    # Validação do arquivo original
    if not caminho_arquivo.exists():
        mostrar_alerta_visual("Erro: Arquivo não encontrado", f"Planilha não existe: {caminho_arquivo}", tipo="error")
        raise FileNotFoundError(f"Arquivo original não encontrado: {caminho_arquivo}")
    
    mostrar_alerta_visual("Arquivo validado", f"Origem: {caminho_arquivo.name}", tipo="dev")
    
    # Criando nome do backup
    backup_path = caminho_arquivo.with_name(
        caminho_arquivo.name.replace(".xlsx", " - BACKUP.xlsx")
    )
    
    mostrar_alerta_visual("Nome do backup", f"Destino: {backup_path.name}", tipo="dev")
    
    if not backup_path.exists():
        mostrar_alerta_visual("Criando backup", "Copiando arquivo...", tipo="info")
        
        try:
            shutil.copy(caminho_arquivo, backup_path)
            mostrar_alerta_visual("Backup criado", f"Arquivo: {backup_path.name}", tipo="success")
            print(f"[Backup] Criado em: {backup_path}")
        except Exception as e:
            mostrar_alerta_visual("Erro ao criar backup", f"Erro: {str(e)}", tipo="error")
            raise e
    else:
        mostrar_alerta_visual("Backup já existe", f"Arquivo: {backup_path.name}", tipo="warning")
        print(f"[Backup] Já existe: {backup_path}")
    
    # Verificação final
    if backup_path.exists():
        tamanho_original = caminho_arquivo.stat().st_size
        tamanho_backup = backup_path.stat().st_size
        
        if tamanho_original == tamanho_backup:
            mostrar_alerta_visual("Backup verificado", f"Tamanho: {tamanho_backup:,} bytes", tipo="success")
        else:
            mostrar_alerta_visual("Aviso: Tamanhos diferentes", f"Original: {tamanho_original:,} | Backup: {tamanho_backup:,}", tipo="warning")
    else:
        mostrar_alerta_visual("Erro: Backup não criado", "Arquivo de backup não encontrado", tipo="error")
        raise FileNotFoundError("Backup não foi criado corretamente")
