import tkinter as tk
import time
from controllers.app_controller import AppController
from utils.alerta_visual import mostrar_alerta_visual
from utils.logger import inicializar_logger


def main():
    # Criar janela principal oculta para os alertas
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    root.attributes('-alpha', 0.0)  # Torna completamente transparente
    root.attributes('-topmost', False)  # Não fica sempre no topo
    
    # Alerta de inicialização do sistema (único no início)
    mostrar_alerta_visual("OceanicDesk Iniciando", "Carregando sistema...", tipo="info", tempo=2500)
    
    # Pequeno delay para evitar sobrecarga
    time.sleep(0.5)
    
    # Inicializar sistema de logs
    inicializar_logger()
    
    # Criar janela da aplicação principal
    app = AppController(root)
    
    # Delay antes do alerta de sistema pronto
    time.sleep(1.0)
    
    # Alerta de sistema pronto
    mostrar_alerta_visual("Sistema Pronto", "OceanicDesk carregado com sucesso!", tipo="success", tempo=3000)
    
    # Iniciar loop principal
    root.mainloop()


if __name__ == "__main__":
    main()
