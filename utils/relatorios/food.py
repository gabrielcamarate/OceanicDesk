import time
import pyautogui
import os
from openpyxl import load_workbook
from dotenv import load_dotenv
from utils.excel_ops import LETRA_PLANILHA

# Esses dois abaixo você precisa garantir que existem em outro módulo
from utils.extratores import salvar_planilha_emsys, extrair_food_tmp


def extrair_valores_e_somar(chacal=False):
    if chacal:
        codigos = [60, 11, 23, 64, 54, 14]
    else:
        codigos = [60, 23, 64, 54, 65, 14]
    resultados = []

    for codigo in codigos:
        time.sleep(2)
        pyautogui.press("tab", presses=4)
        pyautogui.write("1")
        pyautogui.press("tab")
        time.sleep(0.5)
        pyautogui.write("0")
        pyautogui.press("tab")
        time.sleep(0.5)

        pyautogui.write(str(codigo))
        pyautogui.press("tab", presses=13)
        time.sleep(0.5)
        pyautogui.press("enter")

        salvar_planilha_emsys()
        pyautogui.click(1334,42)
        pyautogui.click(657,140, duration=0.5)

        valor_str = extrair_food_tmp(chacal=True)  # Ex: "123,45"
        valor_float = float(valor_str.replace(",", "."))
        resultados.append(valor_float)

    total = sum(resultados)
    total_str = str(round(total, 2)).replace(".", ",")  # Ex: "435,90"
    print(total_str)

    return total_str

def atualizar_meu_controle(dia_fim, chacal=False):
    load_dotenv()

    # Extrair e somar valores
    valor = extrair_valores_e_somar(chacal=chacal)
    
    try:
        if isinstance(valor, str):
            valor = float(valor.replace(".", "").replace(",", "."))
    except ValueError:
        raise ValueError(f"Não foi possível converter o valor '{valor}' para float.")

    # Formatar valor com vírgula decimal (para Excel em português)
    valor_str = f"{valor:.2f}"  # mantém ponto decimal (ex: "9991.68")

    # Caminho da planilha do controle
    caminho_meu_controle = os.getenv("CAMINHO_MEU_CONTROLE")

    # Abrir a planilha
    wb_controle = load_workbook(caminho_meu_controle)
    ws_controle = wb_controle.active

    # Criar a fórmula com base no total e dia_fim
    formula = f"={valor_str}/{dia_fim}*30"

    # Atualizar a célula G42
    if chacal:
        ws_controle[f"{LETRA_PLANILHA}20"] = formula
    else:
        ws_controle[f"{LETRA_PLANILHA}42"] = formula

    # Salvar alterações
    wb_controle.save(caminho_meu_controle)