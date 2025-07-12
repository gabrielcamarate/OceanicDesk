import os
import time
import win32com.client
import win32com.client.gencache
import shutil
from datetime import datetime
from interfaces.alerta_visual import mostrar_alerta_visual


def aguardar_arquivo(caminho_arquivo, timeout=30, intervalo=0.5):
    """Aguarda até que um arquivo exista, dentro de um limite de tempo.

    Args:
        caminho_arquivo (str): Caminho completo do arquivo a verificar.
        timeout (int): Tempo máximo de espera em segundos. Default: 30.
        intervalo (float): Intervalo entre verificações. Default: 0.5s.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado dentro do tempo limite.
    """
    mostrar_alerta_visual("Aguardando arquivo", f"Verificando: {os.path.basename(caminho_arquivo)}", tipo="info")
    
    tempo_esperado = 0
    while not os.path.exists(caminho_arquivo) and tempo_esperado < timeout:
        time.sleep(intervalo)
        tempo_esperado += intervalo
        
        # Mostra progresso a cada 5 segundos
        if tempo_esperado % 5 == 0:
            mostrar_alerta_visual("Aguardando arquivo", f"Tempo: {tempo_esperado}s / {timeout}s", tipo="warning")

    if not os.path.exists(caminho_arquivo):
        mostrar_alerta_visual("Erro: Arquivo não encontrado", f"Timeout após {timeout} segundos", tipo="error")
        raise FileNotFoundError(
            f"Arquivo {caminho_arquivo} não encontrado após {timeout} segundos."
        )
    
    mostrar_alerta_visual("Arquivo encontrado", f"Arquivo disponível: {os.path.basename(caminho_arquivo)}", tipo="success")

def corrigir_cache_excel_com():
    """
    Limpa e regenera o cache COM do Excel, caso esteja corrompido.
    """
    mostrar_alerta_visual("Corrigindo cache Excel", "Iniciando processo de limpeza...", tipo="info")
    
    try:
        # Caminho do cache gerado pelo pywin32
        cache_dir = win32com.client.gencache.GetGeneratePath()
        mostrar_alerta_visual("Verificando cache", f"Diretório: {cache_dir}", tipo="dev")
        
        if os.path.exists(cache_dir):
            mostrar_alerta_visual("Removendo cache", "Limpando cache corrompido...", tipo="dev")
            shutil.rmtree(cache_dir, ignore_errors=True)
            print(f"[COM CACHE] Cache COM removido: {cache_dir}")
        else:
            mostrar_alerta_visual("Cache não encontrado", "Diretório não existe", tipo="warning")

        # Força recriação do cache para o Excel
        mostrar_alerta_visual("Regenerando cache", "Criando novo cache do Excel...", tipo="dev")
        win32com.client.gencache.EnsureDispatch("Excel.Application")
        print("[COM CACHE] Cache do Excel COM regenerado com sucesso.")
        mostrar_alerta_visual("Cache corrigido", "Processo finalizado com sucesso", tipo="success")

    except Exception as e:
        mostrar_alerta_visual("Erro ao corrigir cache", f"Falha: {str(e)}", tipo="error")
        print(f"[ERRO] Falha ao corrigir cache COM do Excel: {e}")
        raise e