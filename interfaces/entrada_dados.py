import tkinter as tk
from tkinter import messagebox


def coletar_litros_usuario():
    valores = {}

    def confirmar():
        try:
            valores["etanol"] = float(entry_etanol.get())
            valores["aditivada"] = float(entry_aditivada.get())
            valores["diesel"] = float(entry_diesel.get())
            valores["comum"] = float(entry_comum.get())
            janela.quit()
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números válidos.")

    janela = tk.Tk()
    janela.title("Inserir Litros do Posto")
    janela.geometry("300x300")
    janela.configure(padx=20, pady=20)

    tk.Label(janela, text="Etanol Comum (L):").pack()
    entry_etanol = tk.Entry(janela)
    entry_etanol.pack()

    tk.Label(janela, text="Gasolina Aditivada (L):").pack()
    entry_aditivada = tk.Entry(janela)
    entry_aditivada.pack()

    tk.Label(janela, text="Diesel S10 (L):").pack()
    entry_diesel = tk.Entry(janela)
    entry_diesel.pack()

    tk.Label(janela, text="Gasolina Comum (L):").pack()
    entry_comum = tk.Entry(janela)
    entry_comum.pack()

    tk.Button(janela, text="Confirmar", command=confirmar).pack(pady=15)

    janela.mainloop()

    return (
        valores.get("comum", 0),
        valores.get("aditivada", 0),
        valores.get("diesel", 0),
        valores.get("etanol", 0),
    )
