"""
Exemplo prático de integração do sistema de logging estruturado
sem modificar o código existente.

Este arquivo demonstra como adicionar logging estruturado a funções
existentes usando o padrão Adapter/Wrapper.
"""

import time
from functools import wraps
from typing import Callable, Any, Dict, Optional

# Imports do sistema original (mantidos)
from utils.logger import logger, registrar_log

# Imports do novo sistema estruturado (adições)
from utils.logger import log_operacao, log_erro, log_performance


def with_structured_logging(operation_name: str, details: Optional[Dict[str, Any]] = None):
    """
    Decorator que adiciona logging estruturado a qualquer função
    sem modificar seu código original.
    
    Args:
        operation_name: Nome da operação para o log
        details: Detalhes adicionais para o log
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Detalhes base
            log_details = details or {}
            log_details.update({
                "function": func.__name__,
                "module": func.__module__
            })
            
            # Log de início
            log_operacao(operation_name, "INICIADO", log_details)
            
            # Medição de performance
            start_time = time.time()
            
            try:
                # Executa a função original (sem modificação)
                result = func(*args, **kwargs)
                
                # Calcula duração
                duration_ms = (time.time() - start_time) * 1000
                
                # Log de sucesso
                success_details = log_details.copy()
                success_details.update({"duration_ms": duration_ms})
                log_operacao(operation_name, "SUCESSO", success_details)
                
                # Log de performance
                log_performance(operation_name, duration_ms, log_details)
                
                return result
                
            except Exception as e:
                # Log de erro
                error_details = log_details.copy()
                error_details.update({
                    "duration_ms": (time.time() - start_time) * 1000,
                    "args": str(args)[:200],  # Limita tamanho
                    "kwargs": str(kwargs)[:200]
                })
                log_erro(operation_name, e, error_details)
                
                # Re-raise para manter comportamento original
                raise
        
        return wrapper
    return decorator


# ============================================================================
# EXEMPLOS DE INTEGRAÇÃO COM FUNÇÕES EXISTENTES
# ============================================================================

def funcao_original_sistema():
    """
    Simula uma função que já existe no sistema.
    ESTA FUNÇÃO NÃO DEVE SER MODIFICADA.
    """
    logger.info("Executando função original do sistema...")
    time.sleep(0.1)  # Simula processamento
    logger.info("Função original concluída")
    return "resultado_original"


@with_structured_logging("funcao_original_sistema", {"component": "sistema"})
def funcao_original_sistema_com_logging():
    """
    Wrapper que adiciona logging estruturado à função original
    sem modificar seu código.
    """
    return funcao_original_sistema()


def simular_autosystem_login():
    """
    Simula a função de login do AutoSystem que já existe.
    ESTA FUNÇÃO NÃO DEVE SER MODIFICADA.
    """
    logger.info("Abrindo AutoSystem...")
    time.sleep(0.05)
    logger.info("Efetuando login...")
    time.sleep(0.05)
    logger.info("Login realizado com sucesso")
    return True


@with_structured_logging("autosystem_login", {
    "sistema": "AutoSystem",
    "component": "authentication"
})
def autosystem_login_com_logging(usuario: str, senha: str):
    """
    Wrapper que adiciona logging estruturado ao login do AutoSystem.
    """
    # Adiciona detalhes específicos da operação
    log_operacao("autosystem_login", "PREPARANDO", {
        "usuario": usuario,
        "senha_length": len(senha)
    })
    
    # Chama a função original (sem modificação)
    return simular_autosystem_login()


def simular_exportar_relatorio():
    """
    Simula a função de exportação de relatório que já existe.
    ESTA FUNÇÃO NÃO DEVE SER MODIFICADA.
    """
    logger.info("Exportando relatório para Excel...")
    time.sleep(0.1)  # Simula processamento
    logger.info("✅ Relatório exportado.")
    return "tmp.xlsx"


@with_structured_logging("exportar_relatorio_excel", {
    "component": "relatorios",
    "output_format": "xlsx"
})
def exportar_relatorio_com_logging():
    """
    Wrapper que adiciona logging estruturado à exportação de relatório.
    """
    # Log específico da operação
    log_operacao("exportar_relatorio_excel", "PREPARANDO_EXPORTACAO", {
        "destino": "Desktop/tmp.xlsx",
        "formato": "Excel"
    })
    
    # Chama a função original
    resultado = simular_exportar_relatorio()
    
    # Log adicional após sucesso
    log_operacao("exportar_relatorio_excel", "ARQUIVO_CRIADO", {
        "arquivo": resultado,
        "tamanho_estimado": "2.3MB"
    })
    
    return resultado


def simular_funcao_com_erro():
    """
    Simula uma função que pode falhar.
    ESTA FUNÇÃO NÃO DEVE SER MODIFICADA.
    """
    logger.info("Executando operação que pode falhar...")
    raise FileNotFoundError("AutoSystem não encontrado em: C:/Sistema/AutoSystem.exe")


@with_structured_logging("operacao_com_erro", {"component": "sistema"})
def funcao_com_erro_com_logging():
    """
    Wrapper que adiciona logging estruturado a função que pode falhar.
    """
    return simular_funcao_com_erro()


# ============================================================================
# CLASSE ADAPTER PARA INTEGRAÇÃO MAIS COMPLEXA
# ============================================================================

class LoggingAdapter:
    """
    Adapter que adiciona logging estruturado a qualquer classe
    sem modificar seu código original.
    """
    
    def __init__(self, original_instance, component_name: str):
        self._original = original_instance
        self._component = component_name
    
    def __getattr__(self, name):
        """
        Intercepta chamadas de métodos e adiciona logging estruturado.
        """
        attr = getattr(self._original, name)
        
        if callable(attr):
            @wraps(attr)
            def wrapper(*args, **kwargs):
                operation_name = f"{self._component}_{name}"
                
                log_operacao(operation_name, "INICIADO", {
                    "component": self._component,
                    "method": name,
                    "class": self._original.__class__.__name__
                })
                
                start_time = time.time()
                
                try:
                    result = attr(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000
                    
                    log_operacao(operation_name, "SUCESSO", {
                        "component": self._component,
                        "method": name,
                        "duration_ms": duration_ms
                    })
                    
                    log_performance(operation_name, duration_ms, {
                        "component": self._component,
                        "method": name
                    })
                    
                    return result
                    
                except Exception as e:
                    log_erro(operation_name, e, {
                        "component": self._component,
                        "method": name,
                        "duration_ms": (time.time() - start_time) * 1000
                    })
                    raise
            
            return wrapper
        
        return attr


# ============================================================================
# DEMONSTRAÇÃO DE USO
# ============================================================================

def demonstrar_integracao():
    """
    Demonstra como usar o sistema de logging estruturado
    sem modificar o código existente.
    """
    print("=== DEMONSTRAÇÃO DE INTEGRAÇÃO ===\n")
    
    # 1. Função simples com decorator
    print("1. Função com decorator:")
    resultado = funcao_original_sistema_com_logging()
    print(f"Resultado: {resultado}\n")
    
    # 2. Função com parâmetros
    print("2. Login com logging estruturado:")
    autosystem_login_com_logging("admin", "senha123")
    print()
    
    # 3. Função com logs adicionais
    print("3. Exportação com logs detalhados:")
    arquivo = exportar_relatorio_com_logging()
    print(f"Arquivo criado: {arquivo}\n")
    
    # 4. Tratamento de erro
    print("4. Tratamento de erro estruturado:")
    try:
        funcao_com_erro_com_logging()
    except Exception as e:
        print(f"Erro capturado: {e}\n")
    
    print("✅ Demonstração concluída!")
    print("✅ Sistema original: 100% preservado")
    print("✅ Sistema estruturado: Funcionando como adição")


if __name__ == "__main__":
    print("EXEMPLO DE INTEGRAÇÃO DO LOGGING ESTRUTURADO")
    print("=" * 50)
    demonstrar_integracao()
