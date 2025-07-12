import pyautogui
import time
import webbrowser
from pywinauto.application import Application
from pywinauto import timings
from config import EMAIL_REMETENTE, SENHA_EMAIL, EMAIL_DESTINATARIO
import os
from interfaces.alerta_visual import mostrar_alerta_visual


def enviar_relatorio(caminho_arquivo, data_ontem, chacal=False):
    mostrar_alerta_visual("Iniciando envio de e-mail", "Preparando relatório...", tipo="info")
    
    # Checagem elegante das variáveis de email
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    if not EMAIL_REMETENTE or not SENHA_EMAIL or not destinatario:
        mostrar_alerta_visual("Erro de Configuração", "Credenciais de e-mail não definidas", tipo="error")
        raise EnvironmentError(
            "EMAIL_REMETENTE, SENHA_EMAIL ou EMAIL_DESTINATARIO ausente no .env. Preencha corretamente."
        )
    
    mostrar_alerta_visual("Credenciais validadas", f"Destinatário: {destinatario}", tipo="dev")
    
    webmail_url = "https://webmail-seguro.com.br/rededuque.com.br/?_task=login"
    mostrar_alerta_visual("Abrindo webmail", "Carregando página de login...", tipo="info")
    
    webbrowser.open(webmail_url)
    time.sleep(4)
    
    mostrar_alerta_visual("Preenchendo login", "Inserindo credenciais...", tipo="dev")
    pyautogui.hotkey("ctrl", "a", interval=1)
    pyautogui.press("backspace", interval=1)

    pyautogui.write(EMAIL_REMETENTE)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.write(SENHA_EMAIL)
    
    mostrar_alerta_visual("Aguardando CAPTCHA", "Resolva o CAPTCHA manualmente", tipo="warning")
    pyautogui.alert("🚧 Resolva o CAPTCHA manualmente e clique em OK para continuar.")
    
    mostrar_alerta_visual("CAPTCHA resolvido", "Continuando login...", tipo="success")
    pyautogui.press("tab", presses=3, interval=0.2)
    pyautogui.press("enter")
    time.sleep(2)
    
    mostrar_alerta_visual("Acessando e-mail", "Navegando para nova mensagem...", tipo="info")
    pyautogui.click(96, 231)
    time.sleep(1)
    
    mostrar_alerta_visual("Preenchendo destinatário", f"Para: {destinatario}", tipo="dev")
    pyautogui.write(destinatario)
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    
    if chacal:
        assunto = "PROJEÇÃO DE JUNHO/25"
    else:
        assunto = "Vendas Oceanico"
    
    mostrar_alerta_visual("Preenchendo assunto", f"Assunto: {assunto}", tipo="dev")
    pyautogui.write(assunto)
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.press("delete", presses=22)
    
    if chacal:
        mensagem = f"Bom dia,\n\nSegue em anexo planilhas de projeção atualizada até o dia {data_ontem}.\n\nAtenciosamente,\nGabriel Camarate."
    else:
        mensagem = f"Bom dia,\n\nSegue planilhas de vendas da pista dia {data_ontem}.\n\nAtenciosamente,\nGabriel Camarate."
    
    mostrar_alerta_visual("Preenchendo mensagem", "Inserindo texto do e-mail...", tipo="dev")
    pyautogui.write(mensagem)
    time.sleep(1)
    
    mostrar_alerta_visual("Anexando arquivo", "Selecionando arquivo para anexo...", tipo="info")
    pyautogui.click(418, 162)
    time.sleep(1.5)
    pyautogui.click(500, 360)
    time.sleep(4)
    
    if chacal:
        mostrar_alerta_visual("Aguardando seleção", "Selecione os arquivos manualmente", tipo="warning")
        pyautogui.alert("🚧 Selecione os arquivos e clique em OK para continuar.")
    else:
        mostrar_alerta_visual("Inserindo caminho", f"Arquivo: {os.path.basename(caminho_arquivo)}", tipo="dev")
        pyautogui.write(str(caminho_arquivo))
    
    time.sleep(3)
    pyautogui.click(504, 534)
    time.sleep(2)
    
    mostrar_alerta_visual("Enviando e-mail", "Finalizando envio...", tipo="info")
    pyautogui.click(254, 164)
    time.sleep(6)
    pyautogui.hotkey("alt", "f4")
    
    mostrar_alerta_visual("E-mail enviado", "Relatório enviado com sucesso!", tipo="success")
