import os
import time
from datetime import datetime, timedelta
import pandas as pd
import pyautogui
from tkinter import messagebox, Tk
from utils.duplicata_ocr import (
    preencher_cartoes_com_duplicatas,
    aguardar_usuario,
    limpar_capturas_ocr,
)
from interfaces.metodos_pagamento import coletar_formas_pagamento
from interfaces.valores_fechamento import abrir_janela_valores
from utils.sistema import salvar_planilha_emsys, acessar_relatorio_subcategoria
from interfaces.alerta_visual import mostrar_alerta_visual, mostrar_alerta_progresso


def aguardar_usuario() -> None:
    """
    Exibe uma janela modal solicitando confirmação do usuário antes de continuar a automação.
    """
    mostrar_alerta_visual("Aguardando confirmação", "Aguardando interação do usuário...", tipo="warning")
    
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Aguardando Confirmação", "Clique em 'OK' para continuar.")
    root.destroy()
    
    mostrar_alerta_visual("Confirmação recebida", "Usuário confirmou continuar", tipo="success")


def extrair_valor_tmp() -> float:
    """
    Procura por um arquivo 'tmp*.xlsx' na área de trabalho, extrai o valor da linha
    com 'Total de geral' e retorna esse valor. Remove o arquivo após leitura.
    """
    mostrar_alerta_visual("Extraindo valor temporário", "Procurando arquivo tmp.xlsx...", tipo="info", tempo=1000)
    time.sleep(1.2)
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    arquivos_encontrados = []
    for nome_arquivo in os.listdir(desktop):
        if nome_arquivo.startswith("tmp") and nome_arquivo.endswith(".xlsx"):
            arquivos_encontrados.append(nome_arquivo)
    
    if not arquivos_encontrados:
        mostrar_alerta_visual("Erro: Arquivo não encontrado", "Nenhum tmp*.xlsx no Desktop", tipo="error")
        raise FileNotFoundError(
            "Nenhum arquivo 'tmp*.xlsx' encontrado na área de trabalho."
        )
    
    
    caminho_tmp = os.path.join(desktop, arquivos_encontrados[0])
    
    df = pd.read_excel(caminho_tmp)

    linha = df[df.iloc[:, 0] == "Total de geral"]
    if not linha.empty:
        valor = linha.iloc[0, 2]  # Coluna C
        print(f"[Extração] Valor encontrado: {valor}")
        mostrar_alerta_visual("Valor extraído", f"Total geral: R$ {valor:,.2f}", tipo="dev", tempo=1000)
        time.sleep(1.2)
        
        os.remove(caminho_tmp)
        print(f"[Limpeza] Arquivo temporário removido: {arquivos_encontrados[0]}")
        
        return valor
    else:
        mostrar_alerta_visual("Erro: Dados não encontrados", "Linha 'Total de geral' não existe", tipo="error")
        raise ValueError("Texto 'Total de geral' não encontrado na coluna A.")


def acessar_fechamento_caixa(data_ontem: str) -> None:
    """
    Abre o menu de fechamento de caixa no EMSys, insere a data de ontem e
    realiza os passos iniciais para preparar o ambiente.
    """
    mostrar_alerta_visual("Acessando fechamento de caixa", "Automação iniciada.", tipo="info")
    aguardar_usuario()

    # 1. Acessando fechamento de caixa
    pyautogui.click(330, 84)
    time.sleep(1)
    pyautogui.click(409, 292)
    time.sleep(10)
    
    # 2. Selecionando pista e data
    pyautogui.click(780, 172)
    pyautogui.click(640, 221, duration=0.5)
    pyautogui.click(956, 202)
    
    pyautogui.write(data_ontem)
    pyautogui.click(427, 74, duration=0.2)
    time.sleep(5)
    
    mostrar_alerta_visual("Configuração concluída", "Pista e data configuradas", tipo="success")


def automatizar_fechamento_caixa():
    from utils.duplicata_ocr import limpar_capturas_ocr, aguardar_usuario
    from interfaces.metodos_pagamento import coletar_formas_pagamento
    from interfaces.valores_fechamento import abrir_janela_valores

    
    for i in range(3):
        mostrar_alerta_visual(f"Ciclo {i+1}/3", "Iniciando novo ciclo de fechamento", tipo="info")
        print(f"[INFO] Iniciando ciclo {i+1}/3")

        # Trocar caixa e limpar espécies
        pyautogui.click(633, 76)  # muda para outro caixa
        time.sleep(2)
        
        pyautogui.click(307, 157, duration=0.5)
        pyautogui.click(384, 174, duration=0.5)
        pyautogui.click(685, 172, duration=0.5)
        pyautogui.click(630, 398)
        time.sleep(2)

        # Interface e preenchimento
        mostrar_alerta_visual("Coletando dados", "Abrindo interface de pagamentos...", tipo="info")
        respostas = coletar_formas_pagamento()
        
        mostrar_alerta_visual("Abrindo valores", "Exibindo interface de valores...", tipo="info")
        abrir_janela_valores(respostas)

        # Limpa capturas ao final do processo
        limpar_capturas_ocr()

        # Aguardar antes da próxima repetição
        if i < 2:  # Não aguarda no último ciclo
            mostrar_alerta_visual("Aguardando próximo ciclo", "Preparando para próxima iteração...", tipo="warning")
            aguardar_usuario()
    
    mostrar_alerta_visual("Automação concluída", "Todos os ciclos finalizados", tipo="success")


