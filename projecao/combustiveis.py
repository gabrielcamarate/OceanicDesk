import pandas as pd
import openpyxl
import xlwings as xw
from datetime import datetime, timedelta
from pathlib import Path


def atualizar_combustiveis(caminho_vendas: str, caminho_destino: str) -> None:
    caminho_vendas = Path(caminho_vendas)
    caminho_destino = Path(caminho_destino)
    data_ontem = datetime.today() - timedelta(days=1)
    nome_aba = f"Dia {data_ontem.day:02d}"
    linha_destino = data_ontem.day + 4

    df_vendas = pd.read_excel(caminho_vendas, sheet_name=nome_aba, engine="openpyxl")

    gas_c = round(df_vendas.iloc[19, 3])
    gas_a = round(df_vendas.iloc[20, 3])
    etanol_c = round(df_vendas.iloc[23, 3])
    diesel_s10 = round(df_vendas.iloc[26, 3])

    wb_controle = openpyxl.load_workbook(caminho_destino)
    aba = wb_controle.active

    aba[f"D{linha_destino}"] = gas_c
    aba[f"E{linha_destino}"] = gas_a
    aba[f"F{linha_destino}"] = etanol_c
    aba[f"G{linha_destino}"] = diesel_s10

    wb_controle.save(caminho_destino)
    print(f"Arquivo modificado salvo como {caminho_destino}")


def atualizar_dados_projecao_combustiveis(
    caminho_vendas: str, caminho_projecao: str
) -> None:
    caminho_vendas = Path(caminho_vendas)
    caminho_projecao = Path(caminho_projecao)
    from win32com.client import gencache

    excel = gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    wb = excel.Workbooks.Open(caminho_vendas)
    wb.RefreshAll()
    excel.CalculateUntilAsyncQueriesDone()
    wb.Save()
    wb.Close()
    excel.Quit()

    data_ontem = datetime.today() - timedelta(days=1)
    nome_aba = f"Dia {data_ontem.day:02d}"
    linha_destino = data_ontem.day + 1

    df_vendas = pd.read_excel(caminho_vendas, sheet_name=nome_aba, engine="openpyxl")

    litros = 0 if pd.isna(df_vendas.iloc[29, 3]) else df_vendas.iloc[29, 3]
    lucro = 0 if pd.isna(df_vendas.iloc[29, 4]) else df_vendas.iloc[29, 4]
    minimercado = 0 if pd.isna(df_vendas.iloc[31, 3]) else round(df_vendas.iloc[31, 3])
    margem = 0 if pd.isna(df_vendas.iloc[15, 6]) else df_vendas.iloc[15, 6]
    
    
    # Adiciona os dados na planilha cópia e exporta os mesmos para a planilha meu controle 
    with xw.App(visible=True) as app:
        app.display_alerts = False  # Desativa alertas como o de vínculos
        app.screen_updating = False

        try:
            wb_proj = app.books.open(caminho_projecao, update_links=False)
        except Exception as e:
            print(f"[ERRO] Não foi possível abrir o arquivo: {e}")
            raise
        aba = wb_proj.sheets["VENDAS GERAL"]
       
        # Atribuição segura dos valores
        aba.range(f"M{linha_destino}").value = litros
        aba.range(f"N{linha_destino}").value = lucro
        aba.range(f"O{linha_destino}").value = minimercado
        aba.range(f"P{linha_destino}").value = margem
        wb_proj.save()
        wb_proj.close()
        
