import tkinter as tk
import time
from controllers.app_controller import AppController
from interfaces.alerta_visual import mostrar_alerta_visual
from utils.logger import inicializar_logger


def main():
    # Alerta de inicialização do sistema (único no início)
    mostrar_alerta_visual("OceanicDesk Iniciando", "Carregando sistema...", tipo="info", tempo=2500)
    
    # Pequeno delay para evitar sobrecarga
    time.sleep(0.5)
    
    # Inicializar sistema de logs
    inicializar_logger()
    
    root = tk.Tk()
    app = AppController(root)
    
    # Delay antes do alerta de sistema pronto
    time.sleep(1.0)
    
    # Alerta de sistema pronto
    mostrar_alerta_visual("Sistema Pronto", "OceanicDesk carregado com sucesso!", tipo="success", tempo=3000)
    
    root.mainloop()


if __name__ == "__main__":
    main()
