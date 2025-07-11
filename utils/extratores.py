import os
import time
import pyautogui
import win32com.client as win32
from pathlib import Path
from dotenv import load_dotenv

from utils.logger import logger
from utils.file_utils import aguardar_arquivo, corrigir_cache_excel_com
from utils.excel_ops import buscar_valor_total_geral

def salvar_planilha_emsys():
    from openpyxl import load_workbook
    from openpyxl.cell import MergedCell
    import win32com.client as win32
    
    time.sleep(4)
    pyautogui.click(48, 42)
    time.sleep(1)
    pyautogui.press("down", presses=3, interval=0.2)
    pyautogui.press("tab")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(3.5)
    pyautogui.write("tmp", interval=0.2)
    pyautogui.press("enter")
    time.sleep(10)

    corrigir_cache_excel_com()
    time.sleep(5)

    desktop_tmp = os.path.join(os.path.expanduser("~"), "Desktop", "tmp.xlsx")
    aguardar_arquivo(desktop_tmp)
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    wb = excel.Workbooks.Open(desktop_tmp)
    time.sleep(10)
    wb.Save()
    wb.Close(SaveChanges=True)
    excel.Quit()
    logger.info("🔄 Arquivo tmp.xlsx aberto e salvo via Excel COM.")

def extrair_food_tmp(chacal=False):
    """
    Extrai valor do tmp.xlsx e insere fórmula de projeção em Meu Controle na célula G39.
    A fórmula será: =valor/dia_fim*30
    """
    load_dotenv()

    # Caminhos
    caminho_tmp = Path.home() / "Desktop" / "tmp.xlsx"
    caminho_meu_controle = os.getenv("CAMINHO_MEU_CONTROLE")
    if not caminho_meu_controle:
        raise EnvironmentError("CAMINHO_MEU_CONTROLE não definido no .env.")

    # Extrair valor da planilha temporária
    valor = buscar_valor_total_geral(caminho_tmp, chacal=chacal)

    try:
        if isinstance(valor, str):
            valor = float(valor.replace(".", "").replace(",", "."))
    except ValueError:
        raise ValueError(f"Não foi possível converter o valor '{valor}' para float.")

    os.remove(caminho_tmp)
    print(f"[Limpeza] Arquivo temporário removido: {caminho_tmp}")
    # Formatar valor com vírgula decimal (para Excel em português)
    valor_str = f"{valor:.2f}"  # mantém ponto decimal (ex: "9991.68")
    
    return valor_str