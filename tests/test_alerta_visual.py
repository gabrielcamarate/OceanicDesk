import sys
import os
import time
import threading
import tkinter as tk

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.alerta_visual import mostrar_alerta_visual, mostrar_alerta_progresso


def test_alertas_basicos():
    """Teste básico de todos os tipos de alerta"""
    print("=== Teste 1: Alertas Básicos ===")
    
    mostrar_alerta_visual("Sucesso!", "Seu backup foi realizado com sucesso.", tipo="success")
    time.sleep(2)
    mostrar_alerta_visual("Erro!", "Falha ao conectar ao banco de dados.", tipo="error")
    time.sleep(2)
    mostrar_alerta_visual("Informação", "Processando relatório mensal...", tipo="info")
    time.sleep(2)
    mostrar_alerta_visual("Log de desenvolvedor", "Variável X = 42", tipo="dev")
    time.sleep(2)
    mostrar_alerta_visual("Aviso", "Atenção: dados incompletos detectados.", tipo="warning")
    time.sleep(2)

def test_alertas_simultaneos():
    """Teste de múltiplos alertas simultâneos (simula bug do COM)"""
    print("=== Teste 2: Alertas Simultâneos (Bug COM) ===")
    
    # Simula os 3 alertas que aparecem no COM
    mostrar_alerta_visual("Erro de Conexão", "Falha na comunicação com o sistema", tipo="error")
    time.sleep(0.5)
    mostrar_alerta_visual("Tentando Reconectar", "Nova tentativa de conexão...", tipo="warning")
    time.sleep(0.5)
    mostrar_alerta_visual("Processando", "Aguardando resposta do servidor", tipo="info")
    time.sleep(2)
    
    # Simula o alerta de sucesso que sobrepõe (BUG VISUAL)
    mostrar_alerta_visual("Conexão Estabelecida", "Comunicação restaurada com sucesso!", tipo="success")
    time.sleep(3)

def test_alertas_progresso():
    """Teste de alertas de progresso"""
    print("=== Teste 3: Alertas de Progresso ===")
    
    mostrar_alerta_progresso("Processando Dados", "Etapa 1 de 5", 20)
    time.sleep(1.5)
    mostrar_alerta_progresso("Atualizando Sistema", "Etapa 2 de 5", 40)
    time.sleep(1.5)
    mostrar_alerta_progresso("Sincronizando", "Etapa 3 de 5", 60)
    time.sleep(1.5)
    mostrar_alerta_progresso("Finalizando", "Etapa 4 de 5", 80)
    time.sleep(1.5)
    mostrar_alerta_progresso("Concluído", "Etapa 5 de 5", 100)
    time.sleep(2)

def test_alertas_rapidos():
    """Teste de alertas muito rápidos (simula sobrecarga)"""
    print("=== Teste 4: Alertas Rápidos (Sobrecarga) ===")
    
    for i in range(5):
        mostrar_alerta_visual(f"Alerta {i+1}", f"Teste rápido número {i+1}", tipo="info")
        time.sleep(0.2)
    
    time.sleep(3)

def test_posicionamento():
    """Teste de posicionamento no canto inferior direito"""
    print("=== Teste 5: Posicionamento ===")
    
    # Testa posicionamento automático
    mostrar_alerta_visual("Posição 1", "Canto inferior direito", tipo="info")
    time.sleep(1)
    mostrar_alerta_visual("Posição 2", "Empilhado acima", tipo="warning")
    time.sleep(1)
    mostrar_alerta_visual("Posição 3", "Terceiro nível", tipo="error")
    time.sleep(2)
    
    # Testa posicionamento específico
    mostrar_alerta_visual("Posição Fixa", "Posição específica", tipo="success", posicao=(100, 100))
    time.sleep(2)

def test_threads():
    """Teste de alertas em diferentes threads"""
    print("=== Teste 6: Alertas em Threads ===")
    
    def alerta_thread(nome):
        mostrar_alerta_visual(f"Thread {nome}", f"Alerta da thread {nome}", tipo="dev")
    
    # Cria múltiplas threads
    threads = []
    for i in range(3):
        t = threading.Thread(target=alerta_thread, args=(f"T{i+1}",))
        threads.append(t)
        t.start()
        time.sleep(0.3)
    
    # Aguarda todas as threads
    for t in threads:
        t.join()
    
    time.sleep(2)

def test_bug_sobreposicao():
    """Teste específico para simular o bug de sobreposição visual"""
    print("=== Teste 7: Bug de Sobreposição (Simulação) ===")
    
    # Simula exatamente o cenário do COM
    print("Simulando 3 alertas de erro do COM...")
    mostrar_alerta_visual("COM Error 1", "Falha na porta COM1", tipo="error")
    time.sleep(0.3)
    mostrar_alerta_visual("COM Error 2", "Falha na porta COM2", tipo="error")
    time.sleep(0.3)
    mostrar_alerta_visual("COM Error 3", "Falha na porta COM3", tipo="error")
    time.sleep(2)
    
    print("Simulando alerta de sucesso que sobrepõe...")
    mostrar_alerta_visual("COM Conectado", "Todas as portas COM funcionando!", tipo="success")
    time.sleep(3)
    
    print("BUG VISUAL: O alerta verde está sobrepondo o primeiro alerta vermelho!")

def main():
    """Executa todos os testes em sequência"""
    print("🧪 Iniciando Testes do Sistema de Alertas Visuais")
    print("=" * 50)
    
    # Lista de testes
    testes = [
        test_alertas_basicos,
        test_alertas_simultaneos,
        test_alertas_progresso,
        test_alertas_rapidos,
        test_posicionamento,
        test_threads,
        test_bug_sobreposicao
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n🔄 Executando Teste {i}/{len(testes)}")
        try:
            teste()
            print(f"✅ Teste {i} concluído")
        except Exception as e:
            print(f"❌ Erro no Teste {i}: {e}")
        
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎯 Todos os testes concluídos!")
    print("📝 Verifique os alertas visuais e identifique possíveis bugs")

if __name__ == "__main__":
    main() 