from config import (
    CAMINHO_PLANILHA,
    NOME_ABA,
    DATA_HOJE,
    DATA_ONTEM,
    LOGIN_SISTEMA,
    SENHA_SISTEMA,
)
from openpyxl import load_workbook
from tkinter import messagebox
import os

from utils.arquivos import criar_backup_planilha
from utils.excel_ops import (
    copiar_intervalo_k5_r14,
    formatar_coluna_o_em_vermelho,
    inserir_valor_planilha,
    inserir_litro_e_desconto_planilha,
    inserir_cashback_e_pix_planilha,
    inserir_litros_planilha,
    atualizando_planilhas_projecao
)
from utils.sistema import (
    auto_system_login,
    auto_system_relatorio_litro_e_desconto,
    auto_system_relatorio_cashback_e_pix,
    acessar_relatorio_subcategoria,
    relatorio_combustiveis,
    relatorio_bebida_nao_alcoolica,
    relatorio_bomboniere,
    relatorio_cerveja,
    relatorio_food,
    relatorio_isqueiros,
    relatorio_cigarro,
    posto_chacaltaya
)
from utils.email import enviar_relatorio
from interfaces.entrada_dados import coletar_litros_usuario
from interfaces.metodos_pagamento import coletar_formas_pagamento
from interfaces.valores_fechamento import abrir_janela_valores
from utils.automacao import extrair_valor_tmp, acessar_fechamento_caixa
from utils.automacao import acessar_fechamento_caixa, automatizar_fechamento_caixa
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

# Global modificável se planilha for definida externamente
CAMINHO_PLANILHA_DINAMICO = None


def etapa1_backup_e_precos():
    if not CAMINHO_PLANILHA and not CAMINHO_PLANILHA_DINAMICO:
        raise EnvironmentError("CAMINHO_PLANILHA não definido no .env e nenhum caminho dinâmico selecionado.")
    caminho = CAMINHO_PLANILHA_DINAMICO or CAMINHO_PLANILHA
    assert caminho is not None, "Caminho da planilha não pode ser None."
    criar_backup_planilha(caminho)
    wb = load_workbook(caminho)
    copiar_intervalo_k5_r14(wb, DATA_HOJE)
    formatar_coluna_o_em_vermelho(wb, DATA_HOJE)
    wb.save(caminho)


def etapa2_minimercado():
    if not LOGIN_SISTEMA or not SENHA_SISTEMA:
        raise EnvironmentError("LOGIN_SISTEMA ou SENHA_SISTEMA não definido no .env.")
    caminho = CAMINHO_PLANILHA_DINAMICO or CAMINHO_PLANILHA
    assert caminho is not None, "Caminho da planilha não pode ser None."
    auto_system_login(LOGIN_SISTEMA, SENHA_SISTEMA)
    valor = extrair_valor_tmp()
    wb = load_workbook(caminho)
    inserir_valor_planilha(wb, valor, DATA_HOJE)
    wb.save(caminho)
    messagebox.showinfo("Etapa 2", "Relatório mini-mercado salvo na planilha.")
    

def etapa3_litros_descontos():
    auto_system_relatorio_litro_e_desconto()
    inserir_litro_e_desconto_planilha(
        CAMINHO_PLANILHA_DINAMICO or CAMINHO_PLANILHA, NOME_ABA
    )
    os.system("taskkill /f /im AutoSystem.exe")
    messagebox.showinfo("Etapa 3", "Litros e descontos inseridos com sucesso.")


def etapa4_cashback_pix():
    cashback, pix_total = auto_system_relatorio_cashback_e_pix()
    inserir_cashback_e_pix_planilha(
        CAMINHO_PLANILHA_DINAMICO or CAMINHO_PLANILHA, NOME_ABA, cashback, pix_total
    )


def etapa5_insercao_litros():
    litros = coletar_litros_usuario()
    inserir_litros_planilha(
        CAMINHO_PLANILHA_DINAMICO or CAMINHO_PLANILHA, NOME_ABA, *litros
    )


def etapa6_envio_email():
    enviar_relatorio(
        CAMINHO_PLANILHA_DINAMICO or CAMINHO_PLANILHA, DATA_ONTEM
    )
    messagebox.showinfo("Etapa 6", "Relatório enviado por e-mail!")


def etapa7_fechamento_caixa():
    acessar_fechamento_caixa(DATA_ONTEM)
    automatizar_fechamento_caixa()


def etapa8_projecao_de_vendas() -> None:
    """
    Executa a Etapa 8, que inclui:
    - Atualização de planilhas projeção
    - Atualização completa de relatórios do Meu Controle
    """
    hoje = datetime.now()
    dia_inicio = hoje.replace(day=1).strftime("%d/%m/%Y")
    dia_fim = (hoje - timedelta(days=1)).strftime("%d/%m/%Y")
    ontem = hoje - timedelta(days=1)
    ontem = ontem.day
    
    
    # atualizando_planilhas_projecao()
    # acessar_relatorio_subcategoria()
    # relatorio_combustiveis(hoje, dia_inicio, dia_fim, ontem)
    # relatorio_bebida_nao_alcoolica(ontem)
    # relatorio_bomboniere(ontem)
    # relatorio_cerveja(ontem)
    # relatorio_food(ontem)
    # relatorio_cigarro(ontem)
    # relatorio_isqueiros(ontem)
    posto_chacaltaya()
    messagebox.showinfo("Etapa 8", "Relatórios atualizados com sucesso!")