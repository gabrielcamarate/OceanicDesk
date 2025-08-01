import tkinter as tk
import time
from controllers.app_controller import AppController
from interfaces.alerta_visual import mostrar_alerta_visual
from utils.logger import inicializar_logger
from utils.dynamic_config import auto_update_config

def main():
    print("Iniciando OceanicDesk...")
    print("=" * 50)

    # SISTEMA AUTOMÁTICO DE CONFIGURAÇÃO DINÂMICA
    print("🔧 Verificando configurações automáticas...")
    update_result = auto_update_config()

    # Mostra informações detalhadas das atualizações
    if update_result.get('error'):
        print(f"⚠️ Erro na configuração automática: {update_result['error']}")
        mostrar_alerta_visual("Erro de Configuração", update_result['error'], tipo="warning")
    else:
        print(f"📅 Dia atual: {update_result['current_day']}")

        if update_result['dates_updated']:
            date_info = update_result.get('date_range', {})
            print(f"📅 DATAS ATUALIZADAS AUTOMATICAMENTE!")
            print(f"   Período: {date_info.get('dia_inicio')} até {date_info.get('dia_fim')}")
            print(f"   Motivo: {date_info.get('description', 'Atualização automática')}")
            mostrar_alerta_visual("Datas Atualizadas",
                                f"Período: {date_info.get('dia_inicio')} até {date_info.get('dia_fim')}",
                                tipo="success")

        if update_result['paths_updated']:
            month_info = update_result.get('month_info', {})
            print(f"📁 CAMINHOS ATUALIZADOS AUTOMATICAMENTE!")
            print(f"   Novo mês: {month_info.get('nome_cap', 'N/A')} de {month_info.get('ano', 'N/A')}")
            print(f"   Todos os 6 caminhos mensais foram atualizados")
            mostrar_alerta_visual("Caminhos Atualizados",
                                f"Novo mês: {month_info.get('nome_cap')} de {month_info.get('ano')}",
                                tipo="success")

        if not update_result['dates_updated'] and not update_result['paths_updated']:
            print("✅ Configurações já estão atualizadas")

    print("=" * 50)
    print("🚀 Iniciando interface principal...")

    # Inicializa sistema normalmente
    inicializar_logger()
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
