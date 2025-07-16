import tkinter as tk
import time
from controllers.app_controller import AppController
from interfaces.alerta_visual import mostrar_alerta_visual
from utils.logger import inicializar_logger


def main():
    inicializar_logger()
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
