import tkinter as tk
from PIL import ImageGrab
import time
import os

# Caminho de saída
CAMINHO_SAIDA = os.path.join(os.getcwd(), "capturas_ocr_pyautogui", "emsys_alert.png")

class ScreenCaptureTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.3)  # janela semi-transparente
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg='black')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.root.mainloop()

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.root.withdraw()  # esconde a janela para capturar sem ela
        time.sleep(0.2)  # pequena pausa para garantir que sumiu

        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))

        imagem = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)
        imagem.save(CAMINHO_SAIDA)
        print(f"[✅] Captura salva em: {CAMINHO_SAIDA}")

        self.root.destroy()


if __name__ == "__main__":
    print("🖱️  Clique e arraste com o mouse para selecionar a área desejada...")
    ScreenCaptureTool()
