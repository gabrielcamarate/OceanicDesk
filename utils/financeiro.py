import pyautogui
import time
import openpyxl
from utils.duplicata_ocr import aguardar_usuario
from interfaces.alerta_visual import mostrar_alerta_visual


def preenchendo_sangria(valor, operador):
    mostrar_alerta_visual("Iniciando sangria", f"Valor: R$ {valor} | Operador: {operador}", tipo="info")
    
    print(f"[SANGRIA] Valor: {valor} | Operador: {operador}")
    
    mostrar_alerta_visual("Aguardando confirmação", "Confirme para iniciar sangria", tipo="warning")
    aguardar_usuario()
    
    mostrar_alerta_visual("Clicando no menu", "Acessando menu de sangria...", tipo="dev")
    pyautogui.click(352, 414, duration=0.5)
    
    mostrar_alerta_visual("Preenchendo dados", "Inserindo informações da sangria...", tipo="dev")
    pyautogui.click(521, 175, duration=0.5)
    pyautogui.write("1", interval=0.5)
    pyautogui.press("tab")
    pyautogui.write(valor, interval=0.5)
    pyautogui.press("tab")
    pyautogui.write(operador, interval=0.5)
    
    mostrar_alerta_visual("Confirmando sangria", "Salvando dados...", tipo="dev")
    pyautogui.click(489, 293)
    time.sleep(1.5)
    pyautogui.click(869, 263)
    
    print("Sangria adicionada com sucesso.")
    mostrar_alerta_visual("Sangria concluída", f"Valor R$ {valor} registrado com sucesso", tipo="success")
