import tkinter as tk
from controllers.app_controller import AppController
from utils.alerta_visual import mostrar_alerta_visual
from utils.logger import inicializar_logger


def main():
    # Alerta de inicialização do sistema
    mostrar_alerta_visual("OceanicDesk Iniciando", "Carregando sistema...", tipo="info", tempo=2000)
    
    # Inicializar sistema de logs
    inicializar_logger()
    
    root = tk.Tk()
    app = AppController(root)
    
    # Alerta de sistema pronto
    mostrar_alerta_visual("Sistema Pronto", "OceanicDesk carregado com sucesso!", tipo="success", tempo=3000)
    
    root.mainloop()


if __name__ == "__main__":
    main()
