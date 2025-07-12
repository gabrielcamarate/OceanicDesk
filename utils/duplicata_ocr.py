import pyautogui
import pytesseract
import re
import time
from tkinter import messagebox, Tk
import os
import shutil
from pathlib import Path
from utils.path_utils import get_project_root, get_system_path

PASTA_CAPTURAS = get_project_root() / "capturas_ocr"
PASTA_CAPTURAS.mkdir(exist_ok=True)

# Configura o caminho do Tesseract dinamicamente
pytesseract.pytesseract.tesseract_cmd = get_system_path("tesseract")

codigos_bandeiras = {
    "GOOCARD": 11,
    "PRIME": 11757,
    "PREPAGO MASTER": 23859,
    "PREPAGO VISA": 23861,
    "PREPAGO ELO": 23863,
    "MASTERCARD DEB": 836,
    "MASTERCARD CRED": 821,
    "PLUXE": 823,
    "VR": 1867,
    "VISA CRED": 2,
    "VISA DEB": 3,
    "ALELO": 868,
    "AMEX": 8800,
    "ELO CRED": 464,
    "ELO DEB": 465,
    "FITCARD": 11757,
    "PIX": 17224,
    "NEO": 11758,
    "WIZEL": 2485,
    "AGILE": 1248,
    "LINK": 11756
}


def aguardar_usuario():
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Aguardando Confirmação", "Clique em 'OK' para continuar.")
    root.destroy()


def preencher_cartoes_com_duplicatas(resultados):
    # Expande Duplicatas
    time.sleep(5)
    pyautogui.click(327, 207)
    time.sleep(1)

    # Entra em Cartões de Crédito
    pyautogui.click(417, 254)
    time.sleep(3)

    aguardar_usuario()

    from interfaces.valores_fechamento import calcular_expressao

    for bandeira, info in resultados.items():
        if bandeira not in codigos_bandeiras:
            continue

        valor = str(info["valor"]).replace(".", ",")
        if not valor or calcular_expressao(valor) == 0:
            continue  # ignora valores vazios ou nulos

        codigo_bandeira = str(codigos_bandeiras[bandeira])
        # Incluir duplicata
        pyautogui.click(525, 175)
        pyautogui.write("1")
        pyautogui.press("tab")
        pyautogui.write("1")
        pyautogui.press("tab")
        pyautogui.write("1")
        pyautogui.press("tab")
        pyautogui.write("1")
        pyautogui.press("tab")
        pyautogui.click(651, 382)  # campo cupom fiscal
        time.sleep(4)
        # Captura da área onde aparece o cupom fiscal
        x1, y1, x2, y2 = 328, 296, 398, 312
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        # Salvar a imagem para conferência

        screenshot_path = (
            PASTA_CAPTURAS / f"screenshot_cupom_{bandeira.replace(' ', '_')}.png"
        )
        screenshot.save(screenshot_path)

        # Extração com pytesseract
        cupom = pytesseract.image_to_string(screenshot, config="--psm 7").strip()
        cupom = re.sub(r"\D", "", cupom)  # remove tudo que não for número

        if not cupom:
            print(f"[ERRO] Cupom não reconhecido via OCR para {bandeira}.")
            continue

        print(f"[OCR] Cupom reconhecido para {bandeira}: {cupom}")

        pyautogui.click(536, 301)  # selecionar cupom
        pyautogui.click(871, 510)  # confirmar
        time.sleep(2)

        pyautogui.click(633, 414)  # clicar em sim
        time.sleep(2)

        pyautogui.click(598, 223)  # clicar duplicata
        pyautogui.press("backspace")
        pyautogui.write(cupom)

        pyautogui.press("tab", presses=4)
        pyautogui.write(codigo_bandeira)
        pyautogui.press("tab", presses=3)
        pyautogui.write(valor)

        pyautogui.click(453, 179)  # confirmar
        time.sleep(3)


def limpar_capturas_ocr():
    if PASTA_CAPTURAS.exists():
        for arquivo in PASTA_CAPTURAS.glob("*.png"):
            try:
                arquivo.unlink()
            except Exception as e:
                print(f"[ERRO] Falha ao excluir {arquivo}: {e}")
