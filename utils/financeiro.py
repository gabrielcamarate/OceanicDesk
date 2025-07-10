import pyautogui
import time
from utils.duplicata_ocr import aguardar_usuario


def preenchendo_sangria(valor, operador):
    print(f"[SANGRIA] Valor: {valor} | Operador: {operador}")
    aguardar_usuario()
    pyautogui.click(352, 414, duration=0.5)
    pyautogui.click(521, 175, duration=0.5)
    pyautogui.write("1", interval=0.5)
    pyautogui.press("tab")
    pyautogui.write(valor, interval=0.5)
    pyautogui.press("tab")
    pyautogui.write(operador, interval=0.5)
    pyautogui.click(489, 293)
    time.sleep(1.5)
    pyautogui.click(869, 263)
    print("Sangria adicionada com sucesso.")
