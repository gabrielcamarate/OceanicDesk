from utils.file_utils import aguardar_arquivo
from utils.duplicata_ocr import aguardar_usuario
import os
import time
from datetime import datetime, timedelta
import pyautogui
from utils.logger import logger
from tkinter import messagebox
from utils.excel_ops import extrair_valores_relatorio_combustivel_tmp, extrair_valores_relatorio_bebidas_nao_alcoolicas_tmp, relatorio_bomboniere_tmp, relatorio_cerveja_tmp, relatorio_isqueiro_tmp, relatorio_cigarro_tmp
from utils.relatorios.food import atualizar_meu_controle
from utils.extratores import salvar_planilha_emsys
from utils.file_utils import corrigir_cache_excel_com
from utils.helpers import esperar_elemento
import pygetwindow as gw

def mostrar_area_de_trabalho():
    """Minimiza todas as janelas no Windows."""
    import platform
    import ctypes
    import time

    if platform.system() == "Windows":
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win
        ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)  # D
        ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)  # D up
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Win up
        time.sleep(1)


def abrir_auto_system():
    caminho_app = r"c:\ProgramData\Microsoft\Windows\Start Menu\Programs\AutoSystem\AutoSystem - Gerencial.lnk"
    mostrar_area_de_trabalho()
    os.startfile(caminho_app)
    logger.info("Abrindo AutoSystem...")
    esperar_elemento(r"C:\Users\Usuario\Desktop\Gabriel Camarate\Projeto_posto\capturas_ocr_pyautogui\autosystem_login.png", timeout=60)


def fazer_login(usuario: str, senha: str):
    logger.info("Efetuando login...")
    pyautogui.write(usuario, interval=0.1)
    pyautogui.press("tab")
    pyautogui.write(senha, interval=0.1)
    pyautogui.press("enter")
    esperar_elemento(r"C:\Users\Usuario\Desktop\Gabriel Camarate\Projeto_posto\capturas_ocr_pyautogui\autosystem_remove_alert.png", timeout=60)
    pyautogui.moveTo(1095, 13)
    pyautogui.click()


def navegar_para_relatorio_produtividade():
    logger.info("Navegando até relatório de produtividade...")
    time.sleep(2)
    pyautogui.moveTo(782, 452)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(942, 330)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(49, 31, duration=0.5)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(156, 268, duration=1)
    time.sleep(1)
    pyautogui.moveTo(342, 656, duration=0.8)
    pyautogui.click()
    time.sleep(2)


def preencher_filtros_e_gerar():
    pyautogui.press("tab")
    pyautogui.write("1612", interval=0.1)
    for _ in range(4):
        pyautogui.press("tab")
    pyautogui.write("50", interval=0.1)
    for _ in range(5):
        pyautogui.press("tab")

    data_ontem = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    pyautogui.write(data_ontem, interval=0.1)
    pyautogui.press("tab")
    pyautogui.write(data_ontem, interval=0.1)

    pyautogui.moveTo(465, 456, duration=0.8)
    pyautogui.click()
    time.sleep(1)
    for _ in range(5):
        time.sleep(0.2)
        pyautogui.press("tab")
    pyautogui.press("space")
    for _ in range(6):
        pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(2)


def exportar_relatorio_excel():
    logger.info("Exportando relatório para Excel...")
    pyautogui.moveTo(143, 39)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(596, 451)
    pyautogui.click()
    time.sleep(6)
    pyautogui.moveTo(194, 743, duration=0.5)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.press("f12")
    time.sleep(2)
    pyautogui.hotkey("alt", "d")
    time.sleep(0.5)
    pyautogui.write(r"C:\Users\Usuario\Desktop")
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.write("tmp")
    time.sleep(0.5)
    pyautogui.press("tab", interval=0.2)
    pyautogui.press("down", presses=1, interval=0.2)
    pyautogui.press("up", presses=28, interval=0.2)
    time.sleep(0.3)
    pyautogui.press("enter", presses=2, interval=0.2)
    pyautogui.hotkey("ctrl", "w")
    time.sleep(2)
    logger.info("✅ Relatório exportado.")


def auto_system_login(usuario: str, senha: str):
    abrir_auto_system()
    fazer_login(usuario, senha)
    navegar_para_relatorio_produtividade()
    preencher_filtros_e_gerar()
    exportar_relatorio_excel()


def abrir_relatorio_vendas_detalhado():
    logger.info("Abrindo relatório de vendas detalhado...")
    pyautogui.click(109, 28)
    time.sleep(1)
    pyautogui.moveTo(250, 267, duration=0.5)
    time.sleep(1)
    pyautogui.moveTo(560, 108, duration=0.5)
    time.sleep(1)
    pyautogui.moveTo(771, 268, duration=0.5)
    time.sleep(1)
    pyautogui.click()


def aplicar_filtros_vendas_detalhado():
    logger.info("Aplicando filtros...")
    pyautogui.click(1069, 212)
    time.sleep(1)
    pyautogui.click(888, 427)
    time.sleep(1)
    pyautogui.click(467, 350)
    time.sleep(1)
    pyautogui.click(644, 535)
    time.sleep(1)
    pyautogui.click(497, 374)
    time.sleep(0.5)
    pyautogui.press("backspace", presses=8, interval=0.2)
    data_ontem = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    pyautogui.write(data_ontem, interval=0.1)
    pyautogui.click(521, 471, duration=0.5)
    pyautogui.click(541, 531, duration=0.5)
    pyautogui.click(631, 530, duration=0.5)
    time.sleep(0.5)


def gerar_e_exportar_vendas_detalhado():
    logger.info("Gerando e exportando relatório...")
    pyautogui.click(396, 678)
    time.sleep(4)
    pyautogui.click(144, 38)
    time.sleep(0.5)
    pyautogui.click(593, 450)
    time.sleep(3)
    pyautogui.moveTo(194, 743, duration=0.5)
    time.sleep(1)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.press("f12")
    time.sleep(2)
    pyautogui.hotkey("alt", "d")
    time.sleep(0.5)
    pyautogui.write(r"C:\Users\Usuario\Desktop")
    pyautogui.press("enter")
    time.sleep(1.5)
    pyautogui.write("tmp")
    time.sleep(0.5)
    pyautogui.press("tab", interval=0.2)
    pyautogui.press("down", presses=1, interval=0.2)
    pyautogui.press("up", presses=28, interval=0.2)
    time.sleep(0.3)
    pyautogui.press("enter", presses=2, interval=0.2)
    pyautogui.hotkey("ctrl", "w")
    time.sleep(5)
    logger.info("✅ Relatório detalhado exportado.")


def auto_system_relatorio_litro_e_desconto():
    abrir_relatorio_vendas_detalhado()
    aplicar_filtros_vendas_detalhado()
    gerar_e_exportar_vendas_detalhado()


def abrir_emsys3():
    logger.info("Abrindo EMSys3...")
    mostrar_area_de_trabalho()
    os.startfile(r"c:\Rezende\EMSys3\EMSys3.exe")
    esperar_elemento(r"C:\Users\Usuario\Desktop\Gabriel Camarate\Projeto_posto\capturas_ocr_pyautogui\emsys_login.png", timeout=60)


def login_emsys3():
    pyautogui.press("down", presses=8, interval=0.2)
    pyautogui.press("enter")
    time.sleep(6.5)
    pyautogui.press("tab", presses=2, interval=0.2)
    pyautogui.write("NILTON.BARBOSA")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("123")
    pyautogui.press("enter")
    esperar_elemento(r"C:\Users\Usuario\Desktop\Gabriel Camarate\Projeto_posto\capturas_ocr_pyautogui\emsys_alert.png", timeout=60)


def acessar_relatorio_pix():
    pyautogui.click(1094, 134)
    time.sleep(1)
    pyautogui.click(155, 38)
    time.sleep(1)
    pyautogui.moveTo(529, 105, duration=0.4)
    pyautogui.click()
    time.sleep(0.8)
    pyautogui.moveTo(669, 142)
    pyautogui.click()
    time.sleep(2.5)
    pyautogui.click(901, 512)
    time.sleep(4.5)
    pyautogui.click(765, 482)
    time.sleep(6)


def gerar_relatorio_pix():
    data_ontem = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    pyautogui.write(data_ontem, interval=0.2)
    pyautogui.write(data_ontem, interval=0.2)
    pyautogui.press("down")
    time.sleep(0.8)
    pyautogui.press("tab")
    pyautogui.write("68", interval=0.1)
    pyautogui.press("tab", presses=2, interval=0.2)
    pyautogui.press("enter")
    time.sleep(2.5)
    salvar_planilha_emsys()
    pyautogui.click(1334,42)
    pyautogui.click(657,140, duration=0.5)
    

def processar_relatorio_excel_cashback_pix():
    from openpyxl import load_workbook
    from openpyxl.cell import MergedCell
    import win32com.client as win32

    corrigir_cache_excel_com()

    desktop_tmp = os.path.join(os.path.expanduser("~"), "Desktop", "tmp.xlsx")
    aguardar_arquivo(desktop_tmp)
    excel = win32.gencache.EnsureDispatch("Excel.Application") # type: ignore
    excel.Visible = True
    wb = excel.Workbooks.Open(desktop_tmp)
    time.sleep(10)
    wb.Save()
    wb.Close(SaveChanges=True)
    excel.Quit()
    logger.info("🔄 Arquivo tmp.xlsx aberto e salvo via Excel COM.")

    wb_tmp = load_workbook(desktop_tmp, data_only=True)
    ws_tmp = wb_tmp.active
    cashback_valor = None
    pagarme_valor = None
    pix_valor = None

    if ws_tmp is not None:
        for row in ws_tmp.iter_rows():
            for cell in row:
                if isinstance(cell, MergedCell):
                    continue
                if cell.value is not None:
                    valor = str(cell.value).strip().upper()
                    if valor == "CASHBACK MARKA":
                        cashback_valor = row[15].value
                    elif valor == "PAGAR.ME INSTITUICAO DE PAGAMENTO S.A":
                        pagarme_valor = row[15].value
                    elif valor == "PIX - CIELO":
                        pix_valor = row[15].value
    else:
        logger.warning("ws_tmp é None. Não foi possível iterar pelas linhas.")

    def safe_float(val):
        from decimal import Decimal
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, Decimal):
            return float(val)
        try:
            return float(str(val).replace(',', '.'))
        except Exception:
            return 0.0

    pagarme_valor = pagarme_valor or 0
    pix_valor = pix_valor or 0
    total_pix = safe_float(pagarme_valor) + safe_float(pix_valor)

    if os.path.exists(desktop_tmp):
        os.remove(desktop_tmp)
        logger.info("🗑️ tmp.xlsx deletado.")

    return cashback_valor, total_pix



def auto_system_relatorio_cashback_e_pix():
    abrir_emsys3()
    login_emsys3()
    acessar_relatorio_pix()
    gerar_relatorio_pix()
    return processar_relatorio_excel_cashback_pix()


def acessar_relatorio_subcategoria():
    # Acessar menu de vendas > relatórios > venda por subcategoria
    pyautogui.click(239, 83)
    time.sleep(2)
    pyautogui.moveTo(381, 595)
    time.sleep(2)
    pyautogui.moveTo(698, 358, duration=0.5)
    pyautogui.click()
    time.sleep(5)
    
    
def relatorio_combustiveis(hoje, dia_inicio, dia_fim, ontem, chacal=False): 
    pyautogui.press('tab')
    pyautogui.write('2')
    pyautogui.press('tab')
    pyautogui.write('7')
    pyautogui.press('tab')
    pyautogui.write('51')
    pyautogui.press('tab', presses=4)

    pyautogui.write(dia_inicio)
    time.sleep(0.5)
    pyautogui.write(dia_fim)

    # Confirmar geração do relatório
    pyautogui.moveTo(538, 440, duration=0.2)
    pyautogui.click()
    pyautogui.press('tab', presses=6)
    pyautogui.press('enter')
    
    salvar_planilha_emsys()
    pyautogui.click(1334,42)
    pyautogui.click(657,140, duration=0.5)
    extrair_valores_relatorio_combustivel_tmp(ontem, chacal=chacal)
    

def relatorio_bebida_nao_alcoolica(ontem, chacal=False):
    time.sleep(2)
    pyautogui.press("tab", presses=4)
    pyautogui.write("1")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("0")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("4")
    pyautogui.press("tab", presses=13)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    salvar_planilha_emsys()
    pyautogui.click(1334,42)
    pyautogui.click(657,140, duration=0.5)    
    extrair_valores_relatorio_bebidas_nao_alcoolicas_tmp(ontem, chacal=chacal)
    

def relatorio_bomboniere(ontem, chacal=False):
    time.sleep(2)
    pyautogui.press("tab", presses=4)
    pyautogui.write("1")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("0")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("3")
    pyautogui.press("tab", presses=13)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    salvar_planilha_emsys()
    pyautogui.click(1334,42)
    pyautogui.click(657,140, duration=0.5)    
    relatorio_bomboniere_tmp(ontem, chacal=chacal)


def relatorio_cerveja(ontem, chacal=False):
    time.sleep(2)
    pyautogui.press("tab", presses=4)
    pyautogui.write("1")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("0")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("62")
    pyautogui.press("tab", presses=13)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    salvar_planilha_emsys()
    pyautogui.click(1334,42)
    pyautogui.click(657,140, duration=0.5)    
    relatorio_cerveja_tmp(ontem, chacal=chacal)


def relatorio_cigarro(ontem, chacal=False):
    time.sleep(2)
    pyautogui.press("tab", presses=4)
    pyautogui.write("1")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("0")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("1")
    pyautogui.press("tab", presses=13)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    salvar_planilha_emsys()
    pyautogui.click(1334,42)
    pyautogui.click(657,140, duration=0.5)    
    relatorio_cigarro_tmp(ontem, chacal=chacal)

  
def relatorio_food(ontem, chacal=False):
    atualizar_meu_controle(dia_fim=ontem, chacal=chacal)


def relatorio_isqueiros(ontem, chacal=False):
    time.sleep(2)
    pyautogui.press("tab", presses=4)
    pyautogui.write("1")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("0")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("0")
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write("538")
    pyautogui.press("tab", presses=12)
    time.sleep(0.5)
    pyautogui.press("enter")
    
    salvar_planilha_emsys()
    pyautogui.click(1334,42)
    pyautogui.click(829,146, duration=0.5)    
    relatorio_isqueiro_tmp(ontem, chacal=chacal)
    
    
def posto_chacaltaya():
    hoje = datetime.now()
    dia_inicio = hoje.replace(day=1).strftime("%d/%m/%Y")
    dia_fim = (hoje - timedelta(days=1)).strftime("%d/%m/%Y")
    ontem = hoje - timedelta(days=1)
    ontem = ontem.day
    
    pyautogui.click(83,44)    
    pyautogui.click(29,81, duration=0.2) 
    time.sleep(8)
    pyautogui.click(29,81, duration=0.2) 
    time.sleep(6)
    pyautogui.press("tab")
    pyautogui.write("ELIANE.MARIA")
    pyautogui.press("tab")
    pyautogui.write("220508")
    pyautogui.press("enter")
    time.sleep(30)
    pyautogui.click(155,38)
    time.sleep(15)
    acessar_relatorio_subcategoria()
    relatorio_combustiveis(hoje, dia_inicio, dia_fim, ontem, chacal=True)
    relatorio_bebida_nao_alcoolica(ontem, chacal=True)
    relatorio_bomboniere(ontem, chacal=True)
    relatorio_cerveja(ontem, chacal=True)
    relatorio_food(ontem, chacal=True)
    relatorio_cigarro(ontem, chacal=True)
    relatorio_isqueiros(ontem, chacal=True)