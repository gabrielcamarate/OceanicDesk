import pyautogui
import time
import webbrowser
from pywinauto.application import Application
from pywinauto import timings



def enviar_relatorio(caminho_arquivo, data_ontem, chacal=False):
    webmail_url = "https://webmail-seguro.com.br/rededuque.com.br/?_task=login"
    webbrowser.open(webmail_url)
    time.sleep(4)
    pyautogui.hotkey("ctrl", "a", interval=1)
    pyautogui.press("backspace", interval=1)

    pyautogui.write("postojardimoceanico@admrededuque.com.br")
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.write("Duque60@")
    pyautogui.alert("🚧 Resolva o CAPTCHA manualmente e clique em OK para continuar.")
    pyautogui.press("tab", presses=3, interval=0.2)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.click(96, 231)
    time.sleep(1)
    pyautogui.write("wagner.fernandes@rededuque.com.br")
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    if chacal:
        pyautogui.write("PROJEÇÃO DE JUNHO/25")
    else:
        pyautogui.write("Vendas Oceanico")
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.press("delete", presses=22)
    if chacal:
        pyautogui.write(
            f"Bom dia,\n\nSegue em anexo planilhas de projeção atualizada até o dia {data_ontem}.\n\nAtenciosamente,\nGabriel Camarate."
        )
    else:
        pyautogui.write(
            f"Bom dia,\n\nSegue planilhas de vendas da pista dia {data_ontem}.\n\nAtenciosamente,\nGabriel Camarate."
        )
    time.sleep(1)
    pyautogui.click(418, 162)
    time.sleep(1.5)
    pyautogui.click(500, 360)
    time.sleep(4)
    if chacal:
        pyautogui.alert("🚧 Selecione os arquivos e clique em OK para continuar.")
    else:
        pyautogui.write(str(caminho_arquivo))
    time.sleep(3)
    pyautogui.click(504, 534)
    time.sleep(2)
    pyautogui.click(254, 164)
    time.sleep(6)
    pyautogui.hotkey("alt", "f4")
