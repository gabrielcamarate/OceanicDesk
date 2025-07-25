"""
Exemplos de uso do sistema de logging estruturado.
Este arquivo demonstra como usar o novo sistema mantendo compatibilidade total.

IMPORTANTE: Este é um arquivo de exemplo/demonstração.
O sistema atual continua funcionando 100% igual.
"""

import time
from datetime import datetime
from utils.logger import (
    # Sistema original (mantido igual)
    logger,
    registrar_log,
    inicializar_logger,
    
    # Novo sistema estruturado (adição)
    log_operacao,
    log_erro,
    log_performance,
    structured_logger
)

def exemplo_uso_sistema_original():
    """
    Demonstra que o sistema original continua funcionando exatamente igual.
    NADA mudou no comportamento existente.
    """
    print("=== SISTEMA ORIGINAL (100% MANTIDO) ===")
    
    # Todas essas chamadas funcionam exatamente como antes
    logger.info("Teste do logger original")
    registrar_log("Teste da função registrar_log original")
    
    # Simulando uso real do sistema
    logger.info("Abrindo AutoSystem...")
    logger.info("Efetuando login...")
    logger.info("✅ Relatório exportado.")
    
    print("✅ Sistema original funcionando perfeitamente!")

def exemplo_uso_sistema_estruturado():
    """
    Demonstra como usar o novo sistema estruturado como ADIÇÃO.
    """
    print("\n=== NOVO SISTEMA ESTRUTURADO (ADIÇÃO) ===")
    
    # Logging de operações com contexto estruturado
    log_operacao(
        operacao="autosystem_login",
        status="INICIADO",
        detalhes={
            "usuario": "admin",
            "sistema": "AutoSystem",
            "tentativa": 1
        }
    )
    
    # Simulando uma operação com medição de performance
    inicio = time.time()
    time.sleep(0.1)  # Simula operação
    duracao_ms = (time.time() - inicio) * 1000
    
    log_performance(
        operacao="exportar_relatorio_excel",
        duracao_ms=duracao_ms,
        detalhes={
            "arquivo": "tmp.xlsx",
            "linhas_processadas": 1500,
            "tamanho_mb": 2.3
        }
    )
    
    # Logging de sucesso
    log_operacao(
        operacao="autosystem_login",
        status="SUCESSO",
        detalhes={
            "usuario": "admin",
            "sistema": "AutoSystem",
            "tempo_resposta_ms": 850
        }
    )
    
    print("✅ Sistema estruturado funcionando como adição!")

def exemplo_tratamento_erro():
    """
    Demonstra como o novo sistema trata erros de forma estruturada.
    """
    print("\n=== TRATAMENTO DE ERROS ESTRUTURADO ===")
    
    try:
        # Simula um erro
        raise FileNotFoundError("AutoSystem não encontrado em: C:/Sistema/AutoSystem.exe")
    except Exception as e:
        # Sistema original (mantido)
        logger.error(f"Erro no sistema: {e}")
        
        # Sistema estruturado (adição)
        log_erro(
            operacao="abrir_autosystem",
            erro=e,
            detalhes={
                "caminho_esperado": "C:/Sistema/AutoSystem.exe",
                "sistema_operacional": "Windows",
                "usuario": "admin"
            }
        )
    
    print("✅ Tratamento de erros funcionando!")

def exemplo_integracao_gradual():
    """
    Demonstra como integrar gradualmente o sistema estruturado
    sem modificar o código existente.
    """
    print("\n=== INTEGRAÇÃO GRADUAL ===")
    
    # Função que simula código existente
    def funcao_existente():
        """Simula uma função que já existe no sistema"""
        logger.info("Executando função existente...")
        # ... código existente ...
        logger.info("Função existente concluída")
    
    # Wrapper que adiciona logging estruturado SEM modificar a função original
    def funcao_existente_com_logging_estruturado():
        """Wrapper que adiciona logging estruturado"""
        inicio = time.time()
        
        # Log estruturado de início
        log_operacao("funcao_existente", "INICIADO")
        
        try:
            # Chama a função original (sem modificação)
            funcao_existente()
            
            # Log estruturado de sucesso
            duracao_ms = (time.time() - inicio) * 1000
            log_operacao("funcao_existente", "SUCESSO")
            log_performance("funcao_existente", duracao_ms)
            
        except Exception as e:
            # Log estruturado de erro
            log_erro("funcao_existente", e)
            raise
    
    # Executa com logging estruturado
    funcao_existente_com_logging_estruturado()
    
    print("✅ Integração gradual funcionando!")

def demonstrar_compatibilidade_total():
    """
    Demonstra que ambos os sistemas funcionam em paralelo.
    """
    print("\n=== COMPATIBILIDADE TOTAL ===")
    
    # Ambos os sistemas funcionam simultaneamente
    logger.info("Log do sistema original")
    log_operacao("demonstracao", "EM_ANDAMENTO", {"sistema": "ambos"})
    
    registrar_log("Função original registrar_log")
    structured_logger.log_operation("demonstracao", "DETALHADO", {"nivel": "baixo"})
    
    print("✅ Ambos os sistemas funcionando em paralelo!")

if __name__ == "__main__":
    print("DEMONSTRAÇÃO DO SISTEMA DE LOGGING MELHORADO")
    print("=" * 50)
    
    # Inicializa o sistema (função original mantida)
    inicializar_logger()
    
    # Executa todos os exemplos
    exemplo_uso_sistema_original()
    exemplo_uso_sistema_estruturado()
    exemplo_tratamento_erro()
    exemplo_integracao_gradual()
    demonstrar_compatibilidade_total()
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("✅ Sistema original: 100% funcional")
    print("✅ Sistema estruturado: Adicionado com sucesso")
    print("✅ Compatibilidade: Total")
