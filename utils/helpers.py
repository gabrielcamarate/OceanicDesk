import os
import re
import pyautogui
import time
import os
from interfaces.alerta_visual import mostrar_alerta_visual


def carregar_tmp_excel():
    """
    Procura um arquivo temporário .xlsx na área de trabalho cujo nome comece com 'tmp'.
    Retorna o caminho completo do primeiro encontrado.
    """
    mostrar_alerta_visual("Buscando arquivo temporário", "Procurando tmp.xlsx na área de trabalho", tipo="info")
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop):
        mostrar_alerta_visual("Erro: Área de trabalho não encontrada", "Desktop não foi encontrado", tipo="error")
        raise FileNotFoundError("A área de trabalho não foi encontrada.")
    
    mostrar_alerta_visual("Verificando Desktop", f"Pasta: {desktop}", tipo="dev")
    
    for nome_arquivo in os.listdir(desktop):
        if nome_arquivo.startswith("tmp") and nome_arquivo.endswith(".xlsx"):
            caminho_completo = os.path.join(desktop, nome_arquivo)
            mostrar_alerta_visual("Arquivo encontrado", f"tmp.xlsx: {nome_arquivo}", tipo="success")
            return caminho_completo
    
    mostrar_alerta_visual("Arquivo não encontrado", "tmp.xlsx não existe no Desktop", tipo="error")
    raise FileNotFoundError("Arquivo tmp.xlsx não encontrado.")


def remover_tmp_excel():
    """
    Remove o arquivo temporário .xlsx encontrado na área de trabalho.
    """
    mostrar_alerta_visual("Removendo arquivo temporário", "Localizando e deletando tmp.xlsx", tipo="info")
    
    caminho = carregar_tmp_excel()
    mostrar_alerta_visual("Arquivo localizado", f"Deletando: {os.path.basename(caminho)}", tipo="dev")
    
    try:
        os.remove(caminho)
        mostrar_alerta_visual("Arquivo removido", f"tmp.xlsx deletado com sucesso", tipo="success")
        print(f"[Remoção] Arquivo temporário deletado: {caminho}")
    except Exception as e:
        mostrar_alerta_visual("Erro ao remover", f"Falha: {str(e)}", tipo="error")
        raise e


def calcular_expressao(expr):
    """
    Recebe uma string como '345.23 + 234.21 - 50' e retorna o resultado float.
    Ignora símbolos como R$ e espaços.
    Retorna 0.0 se não conseguir calcular.
    """
    mostrar_alerta_visual("Calculando expressão", f"Processando: {expr}", tipo="dev")
    
    # Limpeza da expressão
    expr_original = expr
    expr = expr.replace(",", ".")
    expr = expr.replace("R$", "").replace("r$", "").strip()
    expr = re.sub(r"[^0-9+\-.\s]", "", expr)
    
    mostrar_alerta_visual("Expressão limpa", f"Original: {expr_original} | Limpa: {expr}", tipo="dev")
    
    try:
        resultado = eval(expr)  # seguro neste contexto após limpeza
        resultado_final = round(float(resultado), 2)
        mostrar_alerta_visual("Cálculo realizado", f"Resultado: {resultado_final}", tipo="success")
        return resultado_final
    except Exception as e:
        mostrar_alerta_visual("Erro no cálculo", f"Expressão inválida: {expr}", tipo="error")
        return 0.0


def esperar_elemento(caminho_imagem, timeout=60, confidence=0.8):
    inicio = time.time()
    tentativas = 0
    
    while time.time() - inicio < timeout:
        tentativas += 1
        
        try:
            local = pyautogui.locateOnScreen(caminho_imagem, confidence=confidence)
            
            if local:
                print(local)
                return local
            else:
                if tentativas % 10 == 0:  # Mostra progresso a cada 10 tentativas
                    tempo_restante = int(timeout - (time.time() - inicio))
                    mostrar_alerta_visual("Aguardando elemento", f"Tentativa {tentativas} - Restam {tempo_restante}s", tipo="warning")
                    
        except pyautogui.ImageNotFoundException:
            # imagem não encontrada nesta tentativa, só ignora e tenta de novo
            if tentativas % 10 == 0:
                tempo_restante = int(timeout - (time.time() - inicio))
                mostrar_alerta_visual("Elemento não encontrado", f"Tentativa {tentativas} - Restam {tempo_restante}s", tipo="warning")
        
        time.sleep(1)
    
    mostrar_alerta_visual("Timeout: Elemento não encontrado", f"Arquivo: {os.path.basename(caminho_imagem)}", tipo="error")
    raise TimeoutError(f"[OCR] Elemento '{os.path.basename(caminho_imagem)}' não encontrado após {timeout} segundos.")