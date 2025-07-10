from datetime import datetime, timedelta
import win32com.client as win32


def obter_data_ontem_formatada():
    data_ontem = datetime.today() - timedelta(days=1)
    dia_str = f"{data_ontem.day:02d}"
    dia_int = data_ontem.day
    return dia_str, dia_int


def atualizar_conexoes_excel(caminho_arquivo: str) -> None:
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    try:
        wb = excel.Workbooks.Open(caminho_arquivo)
        wb.RefreshAll()
        excel.CalculateUntilAsyncQueriesDone()
        wb.Save()
        wb.Close()
    finally:
        excel.Quit()
