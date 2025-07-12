import time
import pyautogui
import os
from openpyxl import load_workbook
from dotenv import load_dotenv
from utils.excel_ops import LETRA_PLANILHA

# Esses dois abaixo você precisa garantir que existem em outro módulo
from utils.extratores import salvar_planilha_emsys, extrair_food_tmp
from interfaces.alerta_visual import mostrar_alerta_visual, mostrar_alerta_progresso


def extrair_valores_e_somar(chacal=False):
    mostrar_alerta_visual("Iniciando extração Food", f"Modo: {'Chacaltaya' if chacal else 'Oceanic'}", tipo="info")
    
    if chacal:
        codigos = [60, 11, 23, 64, 54, 14]
    else:
        codigos = [60, 23, 64, 54, 65, 14]
    
    mostrar_alerta_visual("Códigos configurados", f"Total: {len(codigos)} códigos", tipo="dev")
    resultados = []

    for i, codigo in enumerate(codigos):
        progresso = int((i / len(codigos)) * 100)
        mostrar_alerta_progresso(f"Processando código {codigo}", f"Progresso: {progresso}%", progresso)
        
        mostrar_alerta_visual(f"Processando código {codigo}", f"Item {i+1} de {len(codigos)}", tipo="info")
        
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

        mostrar_alerta_visual("Salvando planilha", f"Código {codigo} - Salvando dados...", tipo="dev")
        salvar_planilha_emsys()
        pyautogui.click(1334,42)
        pyautogui.click(657,140, duration=0.5)

        mostrar_alerta_visual("Extraindo valor", f"Código {codigo} - Processando tmp.xlsx...", tipo="dev")
        valor_str = extrair_food_tmp(chacal=True)  # Ex: "123,45"
        valor_float = float(valor_str.replace(",", "."))
        resultados.append(valor_float)
        
        mostrar_alerta_visual("Valor extraído", f"Código {codigo}: R$ {valor_float:,.2f}", tipo="dev")

    total = sum(resultados)
    total_str = str(round(total, 2)).replace(".", ",")  # Ex: "435,90"
    print(total_str)
    
    mostrar_alerta_visual("Soma concluída", f"Total: R$ {total:,.2f}", tipo="success")

    return total_str

def atualizar_meu_controle(dia_fim, chacal=False):
    mostrar_alerta_visual("Atualizando Meu Controle", f"Dia fim: {dia_fim} | Modo: {'Chacaltaya' if chacal else 'Oceanic'}", tipo="info")
    
    load_dotenv()

    # Extrair e somar valores
    mostrar_alerta_visual("Extraindo valores", "Iniciando processo de extração...", tipo="info")
    valor = extrair_valores_e_somar(chacal=chacal)
    
    try:
        if isinstance(valor, str):
            valor = float(valor.replace(".", "").replace(",", "."))
        mostrar_alerta_visual("Valor processado", f"Total: R$ {valor:,.2f}", tipo="dev")
    except ValueError:
        mostrar_alerta_visual("Erro de conversão", f"Valor inválido: {valor}", tipo="error")
        raise ValueError(f"Não foi possível converter o valor '{valor}' para float.")

    # Formatar valor com vírgula decimal (para Excel em português)
    valor_str = f"{valor:.2f}"  # mantém ponto decimal (ex: "9991.68")

    # Caminho da planilha do controle
    caminho_meu_controle = os.getenv("CAMINHO_MEU_CONTROLE")
    if not caminho_meu_controle:
        mostrar_alerta_visual("Erro de Configuração", "CAMINHO_MEU_CONTROLE não definido", tipo="error")
        raise EnvironmentError("CAMINHO_MEU_CONTROLE não definido no .env.")

    mostrar_alerta_visual("Carregando planilha", f"Arquivo: {os.path.basename(caminho_meu_controle)}", tipo="dev")
    
    # Abrir a planilha
    wb_controle = load_workbook(caminho_meu_controle)
    ws_controle = wb_controle.active

    # Criar a fórmula com base no total e dia_fim
    formula = f"={valor_str}/{dia_fim}*30"
    mostrar_alerta_visual("Fórmula criada", f"Fórmula: {formula}", tipo="dev")

    # Atualizar a célula G42
    if chacal:
        celula = f"{LETRA_PLANILHA}20"
    else:
        celula = f"{LETRA_PLANILHA}42"
    
    mostrar_alerta_visual("Atualizando célula", f"Célula: {celula}", tipo="dev")
    ws_controle[celula] = formula

    # Salvar alterações
    mostrar_alerta_visual("Salvando alterações", "Persistindo modificações...", tipo="info")
    wb_controle.save(caminho_meu_controle)
    
    mostrar_alerta_visual("Meu Controle atualizado", f"Fórmula inserida em {celula}", tipo="success")