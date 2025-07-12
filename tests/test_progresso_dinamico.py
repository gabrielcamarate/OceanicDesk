import sys
import os
import time
import threading

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces.alerta_visual import mostrar_alerta_visual, atualizar_progresso, fechar_progresso

def test_progresso_simples():
    """Teste de progresso simples"""
    print("=== Teste 1: Progresso Simples ===")
    
    atualizar_progresso("Teste Simples", "Iniciando operação...", 0)
    time.sleep(1)
    
    atualizar_progresso("Teste Simples", "Processando dados...", 25)
    time.sleep(1)
    
    atualizar_progresso("Teste Simples", "Aplicando formatação...", 50)
    time.sleep(1)
    
    atualizar_progresso("Teste Simples", "Finalizando...", 75)
    time.sleep(1)
    
    atualizar_progresso("Teste Simples", "Concluído!", 100)
    time.sleep(1)
    
    fechar_progresso()
    print("✅ Progresso simples concluído")

def test_progresso_multiplas_operacoes():
    """Teste de progresso com múltiplas operações simuladas"""
    print("=== Teste 2: Múltiplas Operações ===")
    
    operacoes = [
        ("Inicializando", "Carregando configurações...", 10),
        ("Validando", "Verificando arquivos...", 20),
        ("Conectando", "Estabelecendo conexão...", 30),
        ("Processando", "Executando operações...", 50),
        ("Salvando", "Persistindo dados...", 70),
        ("Finalizando", "Limpando recursos...", 90),
        ("Concluído", "Operação finalizada!", 100)
    ]
    
    for titulo, descricao, progresso in operacoes:
        atualizar_progresso(titulo, descricao, progresso)
        time.sleep(0.8)
    
    fechar_progresso()
    print("✅ Múltiplas operações concluídas")

def test_progresso_etapas():
    """Teste simulando etapas do OceanicDesk"""
    print("=== Teste 3: Etapas OceanicDesk ===")
    
    etapas = [
        ("Etapa 1: Backup", "Criando backup da planilha...", 12),
        ("Etapa 2: Login", "Conectando ao sistema...", 25),
        ("Etapa 3: Relatório", "Gerando relatório de litros...", 37),
        ("Etapa 4: Dados", "Extraindo dados de cashback...", 50),
        ("Etapa 5: Interface", "Abrindo interface de coleta...", 62),
        ("Etapa 6: E-mail", "Preparando relatório...", 75),
        ("Etapa 7: EMSys", "Conectando ao sistema...", 87),
        ("Etapa 8: Projeção", "Processando dados de vendas...", 100)
    ]
    
    for titulo, descricao, progresso in etapas:
        atualizar_progresso(titulo, descricao, progresso)
        time.sleep(1)
    
    fechar_progresso()
    print("✅ Etapas OceanicDesk concluídas")

def test_progresso_rapido():
    """Teste de progresso muito rápido"""
    print("=== Teste 4: Progresso Rápido ===")
    
    for i in range(0, 101, 5):
        atualizar_progresso("Progresso Rápido", f"Etapa {i//5 + 1}/20", i)
        time.sleep(0.1)
    
    fechar_progresso()
    print("✅ Progresso rápido concluído")

def test_progresso_com_alertas():
    """Teste de progresso com alertas simultâneos"""
    print("=== Teste 5: Progresso + Alertas ===")
    
    atualizar_progresso("Operação Principal", "Iniciando processo...", 10)
    time.sleep(0.5)
    
    # Simula alertas que aparecem durante o progresso
    mostrar_alerta_visual("Aviso", "Arquivo temporário criado", tipo="warning")
    time.sleep(0.5)
    
    atualizar_progresso("Operação Principal", "Processando dados...", 30)
    time.sleep(0.5)
    
    mostrar_alerta_visual("Info", "Dados validados com sucesso", tipo="info")
    time.sleep(0.5)
    
    atualizar_progresso("Operação Principal", "Finalizando...", 70)
    time.sleep(0.5)
    
    mostrar_alerta_visual("Sucesso", "Operação concluída!", tipo="success")
    time.sleep(0.5)
    
    atualizar_progresso("Operação Principal", "Concluído!", 100)
    time.sleep(1)
    
    fechar_progresso()
    print("✅ Progresso com alertas concluído")

def test_progresso_threads():
    """Teste de progresso em diferentes threads"""
    print("=== Teste 6: Progresso em Threads ===")
    
    def operacao_thread(nome, duracao):
        for i in range(0, 101, 10):
            atualizar_progresso(f"Thread {nome}", f"Progresso {i}%", i)
            time.sleep(duracao)
        fechar_progresso()
    
    # Cria threads com diferentes velocidades
    threads = []
    for i in range(3):
        t = threading.Thread(target=operacao_thread, args=(f"T{i+1}", 0.2))
        threads.append(t)
        t.start()
        time.sleep(0.3)
    
    # Aguarda todas as threads
    for t in threads:
        t.join()
    
    print("✅ Progresso em threads concluído")

def test_bug_sobreposicao_corrigido():
    """Teste para verificar se o bug de sobreposição foi corrigido"""
    print("=== Teste 7: Bug Sobreposição (Corrigido) ===")
    
    # Simula o cenário problemático do COM
    print("Simulando 3 alertas de erro...")
    mostrar_alerta_visual("COM Error 1", "Falha na porta COM1", tipo="error")
    time.sleep(0.3)
    mostrar_alerta_visual("COM Error 2", "Falha na porta COM2", tipo="error")
    time.sleep(0.3)
    mostrar_alerta_visual("COM Error 3", "Falha na porta COM3", tipo="error")
    time.sleep(1)
    
    print("Simulando progresso que deve substituir os alertas...")
    atualizar_progresso("Conectando COM", "Tentando reconexão...", 25)
    time.sleep(1)
    
    atualizar_progresso("Conectando COM", "Estabelecendo comunicação...", 75)
    time.sleep(1)
    
    atualizar_progresso("Conectando COM", "Conexão estabelecida!", 100)
    time.sleep(1)
    
    fechar_progresso()
    
    print("Simulando alerta de sucesso...")
    mostrar_alerta_visual("COM Conectado", "Todas as portas funcionando!", tipo="success")
    time.sleep(2)
    
    print("✅ Bug de sobreposição testado - verifique se não há sobreposição visual")

def main():
    """Executa todos os testes de progresso dinâmico"""
    print("🧪 Iniciando Testes do Sistema de Progresso Dinâmico")
    print("=" * 60)
    
    # Lista de testes
    testes = [
        test_progresso_simples,
        test_progresso_multiplas_operacoes,
        test_progresso_etapas,
        test_progresso_rapido,
        test_progresso_com_alertas,
        test_progresso_threads,
        test_bug_sobreposicao_corrigido
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n🔄 Executando Teste {i}/{len(testes)}")
        try:
            teste()
            print(f"✅ Teste {i} concluído")
        except Exception as e:
            print(f"❌ Erro no Teste {i}: {e}")
        
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎯 Todos os testes de progresso dinâmico concluídos!")
    print("📝 Verifique se o progresso funciona corretamente e não há sobreposições")

if __name__ == "__main__":
    main() 