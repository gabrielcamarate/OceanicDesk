import pandas as pd
import openpyxl
import calendar
from datetime import datetime
from pathlib import Path

LETRA_PLANILHA = "H"

def atualizar_projecao_vendas(
    caminho_arquivo_chacaltaya: str,
    caminho_arquivo_vendas: str,
    caminho_arquivo_destino: str,
    nome_aba_vendas: str = "Abril",
    nome_aba_chacaltaya: str = "Julho",
) -> None:
    caminho_arquivo_chacaltaya = Path(caminho_arquivo_chacaltaya)
    caminho_arquivo_vendas = Path(caminho_arquivo_vendas)
    caminho_arquivo_destino = Path(caminho_arquivo_destino)

    df_chacaltaya = pd.read_excel(
        caminho_arquivo_chacaltaya, sheet_name=nome_aba_chacaltaya, engine="openpyxl"
    )
    df_oceanico = pd.read_excel(
        caminho_arquivo_vendas, sheet_name=None, engine="openpyxl"
    )

    # # Descobre o número de dias do mês atual
    # hoje = datetime.today()
    # dias_do_mes = calendar.monthrange(hoje.year, hoje.month)[1]

    proj_loja_chacaltaya = df_chacaltaya.iloc[37, 2]
    proj_acai_chacaltaya = df_chacaltaya.iloc[37, 15]
    proj_loja_oceanico = df_oceanico[nome_aba_vendas].iloc[36, 2]
    proj_acai_oceanico = df_oceanico[nome_aba_vendas].iloc[36, 15]

    wb_destino = openpyxl.load_workbook(caminho_arquivo_destino)
    aba_destino = wb_destino.active

    aba_destino[f"{LETRA_PLANILHA}3"] = proj_loja_chacaltaya
    aba_destino[f"{LETRA_PLANILHA}7"] = proj_acai_chacaltaya
    aba_destino[f"{LETRA_PLANILHA}26"] = proj_loja_oceanico
    aba_destino[f"{LETRA_PLANILHA}30"] = proj_acai_oceanico

    wb_destino.save(caminho_arquivo_destino)
    print(f"Arquivo modificado salvo como: {caminho_arquivo_destino}")
