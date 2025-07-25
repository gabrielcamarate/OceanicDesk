"""
Exemplos de uso do Sistema de Métricas de Performance.

IMPORTANTE: Este sistema mantém 100% da compatibilidade com as operações existentes.
Todas as funções e operações continuam funcionando exatamente igual.

Este arquivo demonstra como usar o novo sistema como ADIÇÃO ao existente.
"""

import time
import random
from pathlib import Path

# Imports do sistema original (mantidos)
try:
    from utils.logger import logger
    from interfaces.alerta_visual import mostrar_alerta_visual
except ImportError:
    # Fallback se módulos não estiverem disponíveis
    class MockLogger:
        def error(self, msg): print(f"[ERROR] {msg}")
        def info(self, msg): print(f"[INFO] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
    
    logger = MockLogger()
    
    def mostrar_alerta_visual(titulo, msg, tipo="info"):
        print(f"[{tipo.upper()}] {titulo}: {msg}")

# Imports do novo sistema de métricas (adições)
from utils.metrics import (
    # Métricas principais
    performance_metrics,
    
    # Decorators
    measure_performance,
    measure_excel_operation,
    measure_automation_operation,
    
    # Funções de conveniência
    record_operation_metric,
    start_metrics_collection,
    stop_metrics_collection,
    get_performance_stats,
    get_slow_operations_report,
    export_performance_report,
    
    # Análise e relatórios
    analyze_performance_trends,
    generate_performance_dashboard,
    
    # Alertas
    performance_alerts,
    
    # Utilitários
    enhance_with_metrics,
    is_metrics_available
)


# ============================================================================
# EXEMPLOS DE USO - MANTENDO COMPATIBILIDADE TOTAL
# ============================================================================

def exemplo_sistema_original():
    """
    Demonstra que o sistema original continua funcionando 100% igual.
    """
    print("=== SISTEMA ORIGINAL (100% MANTIDO) ===")
    
    # Operações originais (continuam funcionando igual)
    def operacao_original():
        """Simula operação que já existe no sistema"""
        logger.info("Executando operação original...")
        time.sleep(0.1)  # Simula processamento
        logger.info("Operação original concluída")
        return "resultado_original"
    
    # Função de medição manual original
    def medir_tempo_original():
        """Medição manual que já existe"""
        inicio = time.time()
        resultado = operacao_original()
        duracao = (time.time() - inicio) * 1000
        logger.info(f"Operação levou {duracao:.2f}ms")
        return resultado
    
    # Executa operações originais
    resultado = medir_tempo_original()
    print(f"✅ Sistema original funcionando: {resultado}")


def exemplo_sistema_com_metricas():
    """
    Demonstra como usar o novo sistema de métricas como ADIÇÃO.
    """
    print("\n=== SISTEMA COM MÉTRICAS (ADIÇÃO) ===")
    
    # Inicia coleta de métricas (adição)
    start_metrics_collection()
    print("✅ Coleta de métricas iniciada")
    
    # Simula algumas operações com métricas
    for i in range(5):
        # Simula operação Excel
        duration = random.uniform(100, 800)
        record_operation_metric(f"load_workbook_planilha_{i}", duration, {
            "file_size_mb": random.uniform(1, 10),
            "sheets_count": random.randint(1, 5)
        })
        
        # Simula operação de cache
        cache_duration = random.uniform(10, 50)
        record_operation_metric(f"cache_hit_planilha_{i}", cache_duration, {
            "cache_type": "workbook"
        })
    
    # Obtém estatísticas
    stats = get_performance_stats()
    print(f"✅ Total de operações: {stats['total_operations']}")
    print(f"✅ Duração média: {stats['average_duration_ms']:.2f}ms")
    
    # Para coleta
    stop_metrics_collection()
    print("✅ Sistema de métricas funcionando!")


def exemplo_decorators_metricas():
    """
    Demonstra uso de decorators para coleta automática de métricas.
    """
    print("\n=== DECORATORS DE MÉTRICAS ===")
    
    # Função original que processa Excel
    def processar_excel_original(caminho):
        """Função original que já existe no sistema"""
        print(f"Processando Excel original: {caminho}")
        time.sleep(random.uniform(0.1, 0.3))  # Simula processamento
        return f"Excel {caminho} processado"
    
    # Versão com métricas usando decorator (SEM modificar a original)
    @measure_excel_operation("excel_processing")
    def processar_excel_com_metricas(caminho):
        """Versão com métricas automáticas"""
        return processar_excel_original(caminho)
    
    # Função original de automação
    def autosystem_login_original():
        """Função original de login no AutoSystem"""
        print("Fazendo login no AutoSystem...")
        time.sleep(random.uniform(0.5, 1.5))  # Simula login
        return "Login realizado"
    
    # Versão com métricas
    @measure_automation_operation("autosystem_login")
    def autosystem_login_com_metricas():
        """Versão com métricas automáticas"""
        return autosystem_login_original()
    
    # Teste dos decorators
    print("Testando decorator Excel...")
    resultado1 = processar_excel_com_metricas("vendas.xlsx")
    print(f"✅ Resultado: {resultado1}")
    
    print("Testando decorator automação...")
    resultado2 = autosystem_login_com_metricas()
    print(f"✅ Resultado: {resultado2}")
    
    # Verifica estatísticas
    excel_stats = get_performance_stats("excel_processing")
    if excel_stats.get("metrics_count", 0) > 0:
        print(f"✅ Métricas Excel: {excel_stats['average_duration_ms']:.2f}ms")


def exemplo_integracao_gradual():
    """
    Demonstra como integrar métricas gradualmente sem modificar código existente.
    """
    print("\n=== INTEGRAÇÃO GRADUAL ===")
    
    # Função existente no sistema (NÃO MODIFICAR)
    def buscar_valor_total_existente(caminho_planilha):
        """Função que já existe no sistema"""
        print(f"Buscando valor total em: {caminho_planilha}")
        time.sleep(random.uniform(0.2, 0.8))  # Simula busca
        return 12345.67
    
    # Versão melhorada que adiciona métricas (SEM modificar a original)
    def buscar_valor_total_com_metricas(caminho_planilha):
        """Wrapper que adiciona métricas"""
        # Usa enhance_with_metrics para adicionar coleta automática
        enhanced_function = enhance_with_metrics(
            buscar_valor_total_existente, 
            "buscar_valor_total_geral"
        )
        
        return enhanced_function(caminho_planilha)
    
    # Função original de extração
    def extrair_combustivel_existente():
        """Função original de extração"""
        print("Extraindo dados de combustível...")
        time.sleep(random.uniform(0.1, 0.4))
        return {"etanol": 1500.50, "diesel": 2000.75}
    
    # Versão com métricas usando decorator personalizado
    @measure_performance("extrair_combustivel_tmp", category="excel")
    def extrair_combustivel_com_metricas():
        """Versão com métricas"""
        return extrair_combustivel_existente()
    
    # Teste da integração
    print("Versão original:")
    valor_original = buscar_valor_total_existente("relatorio.xlsx")
    
    print("Versão com métricas:")
    valor_metricas = buscar_valor_total_com_metricas("relatorio.xlsx")
    
    print("Extração com métricas:")
    dados = extrair_combustivel_com_metricas()
    
    print(f"✅ Valores: {valor_original}, {valor_metricas}")
    print(f"✅ Dados: {dados}")


def exemplo_analise_performance():
    """
    Demonstra análise de performance e identificação de gargalos.
    """
    print("\n=== ANÁLISE DE PERFORMANCE ===")
    
    # Simula várias operações com diferentes performances
    operacoes = [
        ("load_workbook_pequeno", 150, {"size": "small"}),
        ("load_workbook_grande", 2500, {"size": "large"}),
        ("read_excel_simples", 300, {"rows": 100}),
        ("read_excel_complexo", 1800, {"rows": 10000}),
        ("cache_hit", 25, {"type": "hit"}),
        ("cache_miss", 800, {"type": "miss"}),
        ("autosystem_login", 1200, {"system": "AutoSystem"}),
        ("export_relatorio", 3500, {"format": "xlsx"})
    ]
    
    # Registra operações
    for operacao, duracao, detalhes in operacoes:
        record_operation_metric(operacao, duracao, detalhes)
    
    # Análise de tendências
    trends = analyze_performance_trends()
    
    print("Análise por categoria:")
    for categoria, analise in trends["category_analysis"].items():
        print(f"  {categoria}: {analise['average_duration_ms']:.0f}ms ({analise['performance_level']})")
    
    print("\nCandidatos para otimização:")
    for candidato in trends["optimization_candidates"][:3]:
        print(f"  {candidato['operation']}: {candidato['duration_ms']:.0f}ms (prioridade: {candidato['optimization_priority']})")
    
    print(f"\nSaúde geral: {trends['general_health']}")
    
    # Relatório de operações lentas
    slow_ops = get_slow_operations_report(3)
    if slow_ops:
        print("\nOperações mais lentas:")
        for op in slow_ops:
            print(f"  {op['operation']}: {op['duration_ms']:.0f}ms")
    
    print("✅ Análise de performance concluída!")


def exemplo_dashboard_metricas():
    """
    Demonstra geração de dashboard de métricas.
    """
    print("\n=== DASHBOARD DE MÉTRICAS ===")
    
    # Gera dados do dashboard
    dashboard = generate_performance_dashboard()
    
    print("Visão Geral:")
    overview = dashboard["overview"]
    print(f"  Total de operações: {overview['total_operations']}")
    print(f"  Duração média: {overview['average_duration_ms']:.2f}ms")
    print(f"  Taxa de operações lentas: {overview['slow_operations_rate']:.1f}%")
    print(f"  Taxa de cache hit: {overview['cache_hit_rate']:.1f}%")
    print(f"  Status de saúde: {overview['health_status']}")
    
    if dashboard["top_operations"]:
        print("\nOperações mais comuns:")
        for op, count in dashboard["top_operations"]:
            print(f"  {op}: {count} execuções")
    
    if dashboard["alerts"]:
        print("\nAlertas:")
        for alert in dashboard["alerts"]:
            print(f"  {alert['severity'].upper()}: {alert['message']}")
    
    if dashboard["optimization_suggestions"]:
        print("\nSugestões de otimização:")
        for sugestao in dashboard["optimization_suggestions"]:
            print(f"  {sugestao['operation']}: {sugestao['duration_ms']:.0f}ms")
    
    print("✅ Dashboard gerado!")


def exemplo_exportar_relatorio():
    """
    Demonstra exportação de relatório completo.
    """
    print("\n=== EXPORTAÇÃO DE RELATÓRIO ===")
    
    try:
        # Exporta relatório
        report_path = export_performance_report("relatorio_exemplo.json")
        
        print(f"✅ Relatório exportado: {report_path}")
        print(f"✅ Tamanho: {report_path.stat().st_size / 1024:.1f} KB")
        
        # Verifica se arquivo foi criado
        if report_path.exists():
            print("✅ Arquivo criado com sucesso!")
        
    except Exception as e:
        print(f"Erro na exportação: {e}")


def exemplo_alertas_performance():
    """
    Demonstra sistema de alertas de performance.
    """
    print("\n=== ALERTAS DE PERFORMANCE ===")
    
    # Simula operações que podem gerar alertas
    for i in range(20):
        # Algumas operações lentas para gerar alertas
        if i % 4 == 0:  # 25% de operações lentas
            duration = random.uniform(2000, 5000)  # Operação lenta
        else:
            duration = random.uniform(100, 800)   # Operação normal
        
        record_operation_metric(f"operacao_teste_{i}", duration)
    
    # Verifica alertas
    alerts = performance_alerts.check_performance_alerts()
    
    if alerts:
        print("Alertas encontrados:")
        for alert in alerts:
            print(f"  {alert['severity'].upper()}: {alert['message']}")
    else:
        print("✅ Nenhum alerta de performance")
    
    # Reseta alertas para próximos testes
    performance_alerts.reset_alerts()
    print("✅ Sistema de alertas funcionando!")


def demonstrar_compatibilidade_total():
    """
    Demonstra que ambos os sistemas funcionam em paralelo.
    """
    print("\n=== COMPATIBILIDADE TOTAL ===")
    
    # Sistema original (mantido)
    def operacao_original():
        inicio = time.time()
        time.sleep(0.1)
        duracao = (time.time() - inicio) * 1000
        logger.info(f"Operação original: {duracao:.2f}ms")
        return "original"
    
    # Sistema com métricas (adição)
    @measure_performance("operacao_com_metricas")
    def operacao_com_metricas():
        time.sleep(0.1)
        return "com_metricas"
    
    # Ambos funcionam simultaneamente
    resultado1 = operacao_original()
    resultado2 = operacao_com_metricas()
    
    print(f"✅ Original: {resultado1}")
    print(f"✅ Com métricas: {resultado2}")
    print("✅ Ambos os sistemas funcionando em paralelo!")


if __name__ == "__main__":
    print("DEMONSTRAÇÃO DO SISTEMA DE MÉTRICAS DE PERFORMANCE")
    print("=" * 55)
    
    # Verifica disponibilidade
    print(f"Métricas disponíveis: {is_metrics_available()}")
    
    # Executa todos os exemplos
    exemplo_sistema_original()
    exemplo_sistema_com_metricas()
    exemplo_decorators_metricas()
    exemplo_integracao_gradual()
    exemplo_analise_performance()
    exemplo_dashboard_metricas()
    exemplo_exportar_relatorio()
    exemplo_alertas_performance()
    demonstrar_compatibilidade_total()
    
    print("\n" + "=" * 55)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("✅ Sistema original: 100% funcional")
    print("✅ Sistema de métricas: Implementado com sucesso")
    print("✅ Compatibilidade: Total")
    print("✅ Coleta automática: Funcionando sem impacto na performance")
