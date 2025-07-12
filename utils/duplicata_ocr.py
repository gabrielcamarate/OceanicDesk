import cv2
import numpy as np
import pytesseract
import re
import time
from tkinter import messagebox, Tk
import os
import shutil
from pathlib import Path
from utils.path_utils import get_project_root, get_system_path
from utils.alerta_visual import mostrar_alerta_visual, mostrar_alerta_progresso

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
    mostrar_alerta_visual("Aguardando confirmação", "Aguardando interação do usuário...", tipo="warning")
    
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Aguardando Confirmação", "Clique em 'OK' para continuar.")
    root.destroy()
    
    mostrar_alerta_visual("Confirmação recebida", "Usuário confirmou continuar", tipo="success")


def preencher_cartoes_com_duplicatas(resultados):
    mostrar_alerta_visual("Iniciando preenchimento", "Processando cartões com duplicatas", tipo="info")
    
    # Expande Duplicatas
    mostrar_alerta_visual("Expandindo duplicatas", "Acessando seção de duplicatas...", tipo="dev")
    time.sleep(5)
    pyautogui.click(327, 207)
    time.sleep(1)

    # Entra em Cartões de Crédito
    mostrar_alerta_visual("Acessando cartões", "Navegando para cartões de crédito...", tipo="dev")
    pyautogui.click(417, 254)
    time.sleep(3)

    aguardar_usuario()

    from interfaces.valores_fechamento import calcular_expressao

    # Contador para progresso
    total_bandeiras = len([b for b in resultados.keys() if b in codigos_bandeiras])
    bandeiras_processadas = 0

    for bandeira, info in resultados.items():
        if bandeira not in codigos_bandeiras:
            mostrar_alerta_visual("Bandeira ignorada", f"{bandeira} não suportada", tipo="warning")
            continue

        valor = str(info["valor"]).replace(".", ",")
        if not valor or calcular_expressao(valor) == 0:
            mostrar_alerta_visual("Valor ignorado", f"{bandeira}: valor vazio ou zero", tipo="warning")
            continue  # ignora valores vazios ou nulos

        mostrar_alerta_visual(f"Processando {bandeira}", f"Valor: R$ {valor}", tipo="info")
        
        codigo_bandeira = str(codigos_bandeiras[bandeira])
        
        # Incluir duplicata
        mostrar_alerta_visual("Incluindo duplicata", "Preenchendo campos iniciais...", tipo="dev")
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
        mostrar_alerta_visual("Capturando cupom", "Realizando captura de tela...", tipo="dev")
        x1, y1, x2, y2 = 328, 296, 398, 312
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        # Salvar a imagem para conferência
        screenshot_path = (
            PASTA_CAPTURAS / f"screenshot_cupom_{bandeira.replace(' ', '_')}.png"
        )
        screenshot.save(screenshot_path)
        mostrar_alerta_visual("Captura salva", f"Arquivo: {screenshot_path.name}", tipo="dev")

        # Extração com pytesseract
        mostrar_alerta_visual("Processando OCR", "Extraindo texto da imagem...", tipo="dev")
        cupom = pytesseract.image_to_string(screenshot, config="--psm 7").strip()
        cupom = re.sub(r"\D", "", cupom)  # remove tudo que não for número

        if not cupom:
            mostrar_alerta_visual("Erro OCR", f"Cupom não reconhecido para {bandeira}", tipo="error")
            print(f"[ERRO] Cupom não reconhecido via OCR para {bandeira}.")
            continue

        mostrar_alerta_visual("Cupom extraído", f"{bandeira}: {cupom}", tipo="dev")
        print(f"[OCR] Cupom reconhecido para {bandeira}: {cupom}")

        # Preenchimento dos dados
        mostrar_alerta_visual("Preenchendo dados", "Inserindo cupom e valores...", tipo="dev")
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

        bandeiras_processadas += 1
        progresso = int((bandeiras_processadas / total_bandeiras) * 100)
        mostrar_alerta_progresso("Processando bandeiras", f"Progresso: {progresso}%", progresso)

    mostrar_alerta_visual("Preenchimento finalizado", f"{bandeiras_processadas} bandeiras processadas", tipo="success")


def limpar_capturas_ocr():
    mostrar_alerta_visual("Limpando capturas", "Removendo arquivos temporários...", tipo="info")
    
    if PASTA_CAPTURAS.exists():
        arquivos_removidos = 0
        for arquivo in PASTA_CAPTURAS.glob("*.png"):
            try:
                arquivo.unlink()
                arquivos_removidos += 1
            except Exception as e:
                mostrar_alerta_visual("Erro ao remover", f"Falha: {arquivo.name}", tipo="error")
                print(f"[ERRO] Falha ao excluir {arquivo}: {e}")
        
        mostrar_alerta_visual("Limpeza concluída", f"{arquivos_removidos} arquivos removidos", tipo="success")
    else:
        mostrar_alerta_visual("Pasta não encontrada", "Nenhum arquivo para remover", tipo="warning")
