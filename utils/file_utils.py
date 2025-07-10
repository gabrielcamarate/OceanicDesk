import os
import time
import win32com.client
import win32com.client.gencache
import shutil


def aguardar_arquivo(caminho_arquivo, timeout=30, intervalo=0.5):
    """Aguarda até que um arquivo exista, dentro de um limite de tempo.

    Args:
        caminho_arquivo (str): Caminho completo do arquivo a verificar.
        timeout (int): Tempo máximo de espera em segundos. Default: 30.
        intervalo (float): Intervalo entre verificações. Default: 0.5s.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado dentro do tempo limite.
    """
    tempo_esperado = 0
    while not os.path.exists(caminho_arquivo) and tempo_esperado < timeout:
        time.sleep(intervalo)
        tempo_esperado += intervalo

    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(
            f"Arquivo {caminho_arquivo} não encontrado após {timeout} segundos."
        )

def corrigir_cache_excel_com():
    """
    Limpa e regenera o cache COM do Excel, caso esteja corrompido.
    """
    try:
        # Caminho do cache gerado pelo pywin32
        cache_dir = win32com.client.gencache.GetGeneratePath()
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir, ignore_errors=True)
            print(f"[COM CACHE] Cache COM removido: {cache_dir}")

        # Força recriação do cache para o Excel
        win32com.client.gencache.EnsureDispatch("Excel.Application")
        print("[COM CACHE] Cache do Excel COM regenerado com sucesso.")

    except Exception as e:
        print(f"[ERRO] Falha ao corrigir cache COM do Excel: {e}")