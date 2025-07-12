import os
import time
import pyautogui
import win32com.client as win32
from pathlib import Path
from dotenv import load_dotenv

from utils.logger import logger
from utils.file_utils import aguardar_arquivo, corrigir_cache_excel_com
from utils.excel_ops import buscar_valor_total_geral
from utils.alerta_visual import mostrar_alerta_visual


def salvar_planilha_emsys():
    from openpyxl import load_workbook
    from openpyxl.cell import MergedCell
    import win32com.client as win32
    
    mostrar_alerta_visual("Salvando planilha EMSys", "Iniciando processo de salvamento...", tipo="info")
    
    time.sleep(4)
    mostrar_alerta_visual("Acessando menu", "Clicando no menu de arquivo...", tipo="dev")
    pyautogui.click(48, 42)
    time.sleep(1)
    pyautogui.press("down", presses=3, interval=0.2)
    pyautogui.press("tab")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(3.5)
    
    mostrar_alerta_visual("Definindo nome", "Salvando como tmp.xlsx...", tipo="dev")
    pyautogui.write("tmp", interval=0.2)
    pyautogui.press("enter")
    time.sleep(10)

    mostrar_alerta_visual("Corrigindo cache", "Regenerando cache do Excel...", tipo="dev")
    corrigir_cache_excel_com()
    time.sleep(5)

    desktop_tmp = os.path.join(os.path.expanduser("~"), "Desktop", "tmp.xlsx")
    mostrar_alerta_visual("Aguardando arquivo", "Verificando tmp.xlsx...", tipo="info")
    aguardar_arquivo(desktop_tmp)
    
    mostrar_alerta_visual("Abrindo Excel", "Carregando arquivo via COM...", tipo="dev")
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    wb = excel.Workbooks.Open(desktop_tmp)
    time.sleep(10)
    wb.Save()
    wb.Close(SaveChanges=True)
    excel.Quit()
    
    logger.info("🔄 Arquivo tmp.xlsx aberto e salvo via Excel COM.")
    mostrar_alerta_visual("Planilha salva", "tmp.xlsx processado com sucesso", tipo="success")


def extrair_food_tmp(chacal=False):
    """
    Extrai valor do tmp.xlsx e insere fórmula de projeção em Meu Controle na célula G39.
    A fórmula será: =valor/dia_fim*30
    """
    mostrar_alerta_visual("Extraindo dados Food", "Processando tmp.xlsx...", tipo="info")
    
    load_dotenv()

    # Caminhos
    caminho_tmp = Path.home() / "Desktop" / "tmp.xlsx"
    caminho_meu_controle = os.getenv("CAMINHO_MEU_CONTROLE")
    
    if not caminho_meu_controle:
        mostrar_alerta_visual("Erro de Configuração", "CAMINHO_MEU_CONTROLE não definido", tipo="error")
        raise EnvironmentError("CAMINHO_MEU_CONTROLE não definido no .env.")

    mostrar_alerta_visual("Validando arquivo", f"Verificando: {caminho_tmp.name}", tipo="dev")
    
    if not caminho_tmp.exists():
        mostrar_alerta_visual("Arquivo não encontrado", "tmp.xlsx não existe no Desktop", tipo="error")
        raise FileNotFoundError(f"Arquivo {caminho_tmp} não encontrado.")

    # Extrair valor da planilha temporária
    mostrar_alerta_visual("Buscando valor", "Extraindo total geral...", tipo="dev")
    valor = buscar_valor_total_geral(caminho_tmp, chacal=chacal)

    try:
        if isinstance(valor, str):
            valor = float(valor.replace(".", "").replace(",", "."))
        mostrar_alerta_visual("Valor extraído", f"Total: R$ {valor:,.2f}", tipo="dev")
    except ValueError:
        mostrar_alerta_visual("Erro de conversão", f"Valor inválido: {valor}", tipo="error")
        raise ValueError(f"Não foi possível converter o valor '{valor}' para float.")

    mostrar_alerta_visual("Removendo arquivo", "Deletando tmp.xlsx...", tipo="dev")
    os.remove(caminho_tmp)
    print(f"[Limpeza] Arquivo temporário removido: {caminho_tmp}")
    
    # Formatar valor com vírgula decimal (para Excel em português)
    valor_str = f"{valor:.2f}"  # mantém ponto decimal (ex: "9991.68")
    
    mostrar_alerta_visual("Extração concluída", f"Valor processado: {valor_str}", tipo="success")
    return valor_str