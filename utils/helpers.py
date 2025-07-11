import os
import re
import pyautogui
import time
import os


def carregar_tmp_excel():
    """
    Procura um arquivo temporário .xlsx na área de trabalho cujo nome comece com 'tmp'.
    Retorna o caminho completo do primeiro encontrado.
    """
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop):
        raise FileNotFoundError("A área de trabalho não foi encontrada.")
    for nome_arquivo in os.listdir(desktop):
        if nome_arquivo.startswith("tmp") and nome_arquivo.endswith(".xlsx"):
            return os.path.join(desktop, nome_arquivo)
    raise FileNotFoundError("Arquivo tmp.xlsx não encontrado.")


def remover_tmp_excel():
    """
    Remove o arquivo temporário .xlsx encontrado na área de trabalho.
    """
    caminho = carregar_tmp_excel()
    os.remove(caminho)
    print(f"[Remoção] Arquivo temporário deletado: {caminho}")


def calcular_expressao(expr):
    """
    Recebe uma string como '345.23 + 234.21 - 50' e retorna o resultado float.
    Ignora símbolos como R$ e espaços.
    Retorna 0.0 se não conseguir calcular.
    """
    expr = expr.replace(",", ".")
    expr = expr.replace("R$", "").replace("r$", "").strip()
    expr = re.sub(r"[^0-9+\-.\s]", "", expr)
    try:
        resultado = eval(expr)  # seguro neste contexto após limpeza
        return round(float(resultado), 2)
    except Exception:
        return 0.0



def esperar_elemento(caminho_imagem, timeout=60, confidence=0.9):
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            local = pyautogui.locateOnScreen(caminho_imagem, confidence=confidence)
            if local:
                return local
        except pyautogui.ImageNotFoundException:
            # imagem não encontrada nesta tentativa, só ignora e tenta de novo
            pass
        time.sleep(0.3)
    raise TimeoutError(f"[OCR] Elemento '{os.path.basename(caminho_imagem)}' não encontrado após {timeout} segundos.")