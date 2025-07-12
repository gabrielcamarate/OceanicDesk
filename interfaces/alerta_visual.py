import tkinter as tk
import threading
import time
from tkinter import ttk

ICONS = {
    'success': '\u2714',  # ✔
    'error': '\u26A0',    # ⚠
    'info': '\u2139',     # ℹ
    'dev': '\u2699',      # ⚙
    'warning': '\u26A0',  # ⚠
    'progress': '\u21BB', # ↻
}

COLORS = {
    'success': '#1e2b1e',
    'error': '#2b1e1e',
    'info': '#1e2230',
    'dev': '#23232b',
    'warning': '#2b2b1e',
    'progress': '#1e2b2b',
}

BORDER_COLORS = {
    'success': '#4ade80',
    'error': '#f87171',
    'info': '#60a5fa',
    'dev': '#a78bfa',
    'warning': '#fbbf24',
    'progress': '#06b6d4',
}

TEXT_COLORS = {
    'success': '#d1fae5',
    'error': '#fee2e2',
    'info': '#dbeafe',
    'dev': '#ddd6fe',
    'warning': '#fef3c7',
    'progress': '#cffafe',
}

# Controle de posicionamento para múltiplos alertas
alert_positions = []
max_alerts = 3
active_alerts = 0
alert_lock = threading.Lock()

def mostrar_alerta_visual(titulo, descricao, tipo='info', tempo=3000, opacidade=0.92, posicao=None):
    """
    Exibe um alerta visual moderno e elegante.
    
    Args:
        titulo: Título do alerta
        descricao: Descrição detalhada
        tipo: success, error, info, dev, warning, progress
        tempo: Tempo de exibição em ms
        opacidade: Opacidade da janela (0.0 a 1.0)
        posicao: Posição específica (None para automático)
    """
    def _show():
        global active_alerts
        
        with alert_lock:
            if active_alerts >= max_alerts:
                return  # Limita alertas simultâneos
            active_alerts += 1
        
        try:
            root = tk.Toplevel()
            root.overrideredirect(True)
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.0)
            root.configure(bg=COLORS.get(tipo, '#23232b'))
            
            # Calcula posição - CANTO INFERIOR DIREITO
            root.update_idletasks()
            largura = 380
            altura = 70
            
            if posicao is None:
                # Posicionamento no canto inferior direito
                x = root.winfo_screenwidth() - largura - 20
                y = root.winfo_screenheight() - altura - 20 - (len(alert_positions) * (altura + 10))
                
                # Limita o número de alertas simultâneos
                if len(alert_positions) >= max_alerts:
                    y = root.winfo_screenheight() - altura - 20 - ((len(alert_positions) % max_alerts) * (altura + 10))
                
                alert_positions.append((x, y))
            else:
                x, y = posicao
                
            root.geometry(f'{largura}x{altura}+{x}+{y}')
            
            # Frame principal
            frame = tk.Frame(root, bg=COLORS.get(tipo, '#23232b'), bd=0, highlightthickness=0)
            frame.pack(fill='both', expand=True)
            
            # Borda colorida à esquerda
            borda = tk.Frame(frame, bg=BORDER_COLORS.get(tipo, '#60a5fa'), width=6)
            borda.pack(side='left', fill='y')
            
            # Conteúdo
            conteudo = tk.Frame(frame, bg=COLORS.get(tipo, '#23232b'))
            conteudo.pack(side='left', fill='both', expand=True, padx=12, pady=10)
            
            # Ícone
            icone = tk.Label(conteudo, text=ICONS.get(tipo, '\u2139'), font=('Segoe UI', 18), 
                            bg=COLORS.get(tipo, '#23232b'), fg=BORDER_COLORS.get(tipo, '#60a5fa'))
            icone.grid(row=0, column=0, rowspan=2, sticky='n', padx=(0, 10))
            
            # Título
            label_titulo = tk.Label(conteudo, text=titulo, font=('Segoe UI Semibold', 11), 
                                   bg=COLORS.get(tipo, '#23232b'), fg=TEXT_COLORS.get(tipo, '#dbeafe'))
            label_titulo.grid(row=0, column=1, sticky='w')
            
            # Descrição
            label_desc = tk.Label(conteudo, text=descricao, font=('Segoe UI', 10), 
                                 bg=COLORS.get(tipo, '#23232b'), fg='#b3b3b3')
            label_desc.grid(row=1, column=1, sticky='w')
            
            # Efeito fade in
            for i in range(1, 11):
                root.attributes('-alpha', i * opacidade / 10)
                root.update()
                time.sleep(0.02)  # Reduzido para ser mais rápido
            
            # Timer para fade out
            def fade_out():
                for i in range(10, -1, -1):
                    root.attributes('-alpha', i * opacidade / 10)
                    root.update()
                    time.sleep(0.025)  # Reduzido para ser mais rápido
                
                # Remove da lista de posições
                if posicao is None and (x, y) in alert_positions:
                    alert_positions.remove((x, y))
                
                with alert_lock:
                    global active_alerts
                    active_alerts = max(0, active_alerts - 1)
                
                root.destroy()
            
            root.after(tempo, fade_out)
            
            # Mantém a janela em primeiro plano (otimizado)
            def manter_topmost():
                try:
                    for _ in range(20):  # Limita o tempo de execução
                        root.attributes('-topmost', True)
                        time.sleep(0.5)
                except:
                    pass
            
            threading.Thread(target=manter_topmost, daemon=True).start()
            root.mainloop()
            
        except Exception as e:
            with alert_lock:
                active_alerts = max(0, active_alerts - 1)
    
    # Usa thread apenas se necessário
    if threading.current_thread() is threading.main_thread():
        threading.Thread(target=_show, daemon=True).start()
    else:
        _show()

def mostrar_alerta_progresso(titulo, descricao, progresso=0):
    """
    Exibe um alerta de progresso com barra de progresso.
    """
    def _show():
        global active_alerts
        
        with alert_lock:
            if active_alerts >= max_alerts:
                return
            active_alerts += 1
        
        try:
            root = tk.Toplevel()
            root.overrideredirect(True)
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.0)
            root.configure(bg=COLORS['progress'])
            
            # Posicionamento no canto inferior direito
            root.update_idletasks()
            largura = 380
            altura = 90
            x = root.winfo_screenwidth() - largura - 20
            y = root.winfo_screenheight() - altura - 20
            
            root.geometry(f'{largura}x{altura}+{x}+{y}')
            
            # Frame principal
            frame = tk.Frame(root, bg=COLORS['progress'], bd=0, highlightthickness=0)
            frame.pack(fill='both', expand=True)
            
            # Borda colorida
            borda = tk.Frame(frame, bg=BORDER_COLORS['progress'], width=6)
            borda.pack(side='left', fill='y')
            
            # Conteúdo
            conteudo = tk.Frame(frame, bg=COLORS['progress'])
            conteudo.pack(side='left', fill='both', expand=True, padx=12, pady=10)
            
            # Ícone
            icone = tk.Label(conteudo, text=ICONS['progress'], font=('Segoe UI', 18), 
                            bg=COLORS['progress'], fg=BORDER_COLORS['progress'])
            icone.grid(row=0, column=0, rowspan=3, sticky='n', padx=(0, 10))
            
            # Título
            label_titulo = tk.Label(conteudo, text=titulo, font=('Segoe UI Semibold', 11), 
                                   bg=COLORS['progress'], fg=TEXT_COLORS['progress'])
            label_titulo.grid(row=0, column=1, sticky='w')
            
            # Descrição
            label_desc = tk.Label(conteudo, text=descricao, font=('Segoe UI', 10), 
                                 bg=COLORS['progress'], fg='#b3b3b3')
            label_desc.grid(row=1, column=1, sticky='w')
            
            # Barra de progresso
            progress_bar = ttk.Progressbar(conteudo, length=200, mode='determinate')
            progress_bar.grid(row=2, column=1, sticky='w', pady=(5, 0))
            progress_bar['value'] = progresso
            
            # Fade in
            for i in range(1, 11):
                root.attributes('-alpha', i * 0.92 / 10)
                root.update()
                time.sleep(0.02)
            
            # Mantém em primeiro plano (otimizado)
            def manter_topmost():
                try:
                    for _ in range(20):
                        root.attributes('-topmost', True)
                        time.sleep(0.5)
                except:
                    pass
            
            threading.Thread(target=manter_topmost, daemon=True).start()
            root.mainloop()
            
        except Exception as e:
            with alert_lock:
                active_alerts = max(0, active_alerts - 1)
    
    if threading.current_thread() is threading.main_thread():
        threading.Thread(target=_show, daemon=True).start()
    else:
        _show() 