"""
Sistema de Tratamento de Erros Centralizado - OceanicDesk

IMPORTANTE: Este sistema mantém 100% da compatibilidade com o tratamento de erros existente.
Todas as exceções e try/except atuais continuam funcionando exatamente igual.

Este módulo adiciona:
1. Exceções customizadas para diferentes tipos de erro
2. Handlers centralizados para tratamento consistente
3. Integração com o sistema de logging estruturado
4. Utilitários para melhor debugging e recuperação de erros
"""

import traceback
import sys
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from pathlib import Path

# Import do sistema de logging (se disponível)
try:
    from utils.logger import log_erro, logger
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False

# ============================================================================
# EXCEÇÕES CUSTOMIZADAS DO OCEANICDESK
# ============================================================================

class OceanicDeskError(Exception):
    """
    Exceção base para todos os erros específicos do OceanicDesk.
    Mantém compatibilidade total com Exception padrão.
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None, 
                 operation: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.operation = operation
        self.timestamp = datetime.now().isoformat()
        
        # Log automático se sistema de logging estiver disponível
        if LOGGING_AVAILABLE and operation:
            log_erro(operation, self, self.details)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a exceção para dicionário para logging estruturado"""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "operation": self.operation,
            "timestamp": self.timestamp,
            "traceback": traceback.format_exc()
        }


class FileOperationError(OceanicDeskError):
    """Erros relacionados a operações de arquivo (Excel, backup, etc.)"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, 
                 operation: str = "file_operation", **kwargs):
        details = kwargs.get('details', {})
        if file_path:
            details['file_path'] = str(file_path)
            details['file_exists'] = Path(file_path).exists() if file_path else False
        
        super().__init__(message, details, operation)
        self.file_path = file_path


class SystemConnectionError(OceanicDeskError):
    """Erros de conexão com sistemas externos (AutoSystem, EMSys, etc.)"""
    
    def __init__(self, message: str, system_name: Optional[str] = None,
                 operation: str = "system_connection", **kwargs):
        details = kwargs.get('details', {})
        if system_name:
            details['system_name'] = system_name
        
        super().__init__(message, details, operation)
        self.system_name = system_name


class DataValidationError(OceanicDeskError):
    """Erros de validação de dados (valores inválidos, formatos incorretos, etc.)"""
    
    def __init__(self, message: str, field_name: Optional[str] = None,
                 invalid_value: Any = None, operation: str = "data_validation", **kwargs):
        details = kwargs.get('details', {})
        if field_name:
            details['field_name'] = field_name
        if invalid_value is not None:
            details['invalid_value'] = str(invalid_value)
            details['value_type'] = type(invalid_value).__name__
        
        super().__init__(message, details, operation)
        self.field_name = field_name
        self.invalid_value = invalid_value


class AutomationError(OceanicDeskError):
    """Erros durante automação (pyautogui, OCR, etc.)"""
    
    def __init__(self, message: str, automation_step: Optional[str] = None,
                 operation: str = "automation", **kwargs):
        details = kwargs.get('details', {})
        if automation_step:
            details['automation_step'] = automation_step
        
        super().__init__(message, details, operation)
        self.automation_step = automation_step


class ConfigurationError(OceanicDeskError):
    """Erros de configuração (.env, caminhos, etc.)"""
    
    def __init__(self, message: str, config_key: Optional[str] = None,
                 operation: str = "configuration", **kwargs):
        details = kwargs.get('details', {})
        if config_key:
            details['config_key'] = config_key
        
        super().__init__(message, details, operation)
        self.config_key = config_key


# ============================================================================
# HANDLERS DE ERRO CENTRALIZADOS
# ============================================================================

class ErrorHandler:
    """
    Handler centralizado para tratamento de erros.
    Complementa o sistema existente sem substituí-lo.
    """
    
    @staticmethod
    def handle_file_error(error: Exception, file_path: str, operation: str = "file_operation") -> FileOperationError:
        """
        Converte erros de arquivo padrão em FileOperationError com contexto adicional.
        """
        if isinstance(error, FileNotFoundError):
            return FileOperationError(
                f"Arquivo não encontrado: {file_path}",
                file_path=file_path,
                operation=operation,
                details={
                    "original_error": str(error),
                    "error_type": type(error).__name__
                }
            )
        elif isinstance(error, PermissionError):
            return FileOperationError(
                f"Permissão negada para arquivo: {file_path}",
                file_path=file_path,
                operation=operation,
                details={
                    "original_error": str(error),
                    "error_type": type(error).__name__,
                    "suggestion": "Verifique se o arquivo não está aberto em outro programa"
                }
            )
        else:
            return FileOperationError(
                f"Erro ao processar arquivo {file_path}: {error}",
                file_path=file_path,
                operation=operation,
                details={
                    "original_error": str(error),
                    "error_type": type(error).__name__
                }
            )
    
    @staticmethod
    def handle_validation_error(error: Exception, field_name: str, value: Any, 
                              operation: str = "validation") -> DataValidationError:
        """
        Converte erros de validação padrão em DataValidationError com contexto.
        """
        if isinstance(error, ValueError):
            return DataValidationError(
                f"Valor inválido para {field_name}: {value}",
                field_name=field_name,
                invalid_value=value,
                operation=operation,
                details={
                    "original_error": str(error),
                    "error_type": type(error).__name__
                }
            )
        else:
            return DataValidationError(
                f"Erro de validação em {field_name}: {error}",
                field_name=field_name,
                invalid_value=value,
                operation=operation,
                details={
                    "original_error": str(error),
                    "error_type": type(error).__name__
                }
            )
    
    @staticmethod
    def handle_system_error(error: Exception, system_name: str, 
                          operation: str = "system_operation") -> SystemConnectionError:
        """
        Converte erros de sistema em SystemConnectionError com contexto.
        """
        return SystemConnectionError(
            f"Erro no sistema {system_name}: {error}",
            system_name=system_name,
            operation=operation,
            details={
                "original_error": str(error),
                "error_type": type(error).__name__
            }
        )


# ============================================================================
# DECORATORS PARA TRATAMENTO AUTOMÁTICO DE ERROS
# ============================================================================

def handle_file_operations(operation_name: str = "file_operation"):
    """
    Decorator que automaticamente converte erros de arquivo em FileOperationError.
    Mantém comportamento original mas adiciona contexto estruturado.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (FileNotFoundError, PermissionError, OSError) as e:
                # Tenta extrair caminho do arquivo dos argumentos
                file_path = None
                if args:
                    file_path = str(args[0]) if args[0] else None
                
                # Converte para exceção customizada
                custom_error = ErrorHandler.handle_file_error(e, file_path or "unknown", operation_name)
                
                # Re-raise como exceção customizada
                raise custom_error from e
            except Exception as e:
                # Para outros erros, mantém comportamento original
                raise
        
        return wrapper
    return decorator


def handle_data_validation(operation_name: str = "validation"):
    """
    Decorator que automaticamente converte erros de validação em DataValidationError.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                # Tenta extrair informações dos argumentos
                field_name = func.__name__
                value = args[0] if args else None
                
                # Converte para exceção customizada
                custom_error = ErrorHandler.handle_validation_error(e, field_name, value, operation_name)
                
                # Re-raise como exceção customizada
                raise custom_error from e
            except Exception as e:
                # Para outros erros, mantém comportamento original
                raise
        
        return wrapper
    return decorator


# ============================================================================
# UTILITÁRIOS PARA COMPATIBILIDADE
# ============================================================================

def safe_execute(func: Callable, *args, default_return=None, 
                operation_name: str = "safe_execution", **kwargs):
    """
    Executa uma função de forma segura, capturando e logando erros.
    Retorna valor padrão em caso de erro.
    Complementa o sistema existente sem substituí-lo.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        # Log do erro se sistema de logging estiver disponível
        if LOGGING_AVAILABLE:
            log_erro(operation_name, e, {
                "function": func.__name__,
                "args": str(args)[:200],
                "kwargs": str(kwargs)[:200]
            })
        
        # Log tradicional como fallback
        if LOGGING_AVAILABLE:
            logger.error(f"Erro em {operation_name}: {e}")
        else:
            print(f"[ERRO] {operation_name}: {e}")
        
        return default_return


def get_error_context(error: Exception) -> Dict[str, Any]:
    """
    Extrai contexto detalhado de qualquer exceção para debugging.
    """
    return {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": traceback.format_exc(),
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "is_oceanicdesk_error": isinstance(error, OceanicDeskError)
    }


# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA PARA MIGRAÇÃO GRADUAL
# ============================================================================

def wrap_existing_exception(error: Exception, operation: str,
                          details: Optional[Dict[str, Any]] = None) -> OceanicDeskError:
    """
    Envolve uma exceção existente em OceanicDeskError para adicionar contexto.
    Útil para migração gradual sem quebrar código existente.
    """
    return OceanicDeskError(
        str(error),
        details=details,
        operation=operation
    )


# ============================================================================
# COMPATIBILIDADE COM SISTEMA EXISTENTE
# ============================================================================

# Aliases para manter compatibilidade com padrões existentes
FileError = FileOperationError
ValidationError = DataValidationError
SystemError = SystemConnectionError

# Função para verificar se uma exceção é do OceanicDesk
def is_oceanicdesk_error(error: Exception) -> bool:
    """Verifica se uma exceção é do tipo OceanicDesk"""
    return isinstance(error, OceanicDeskError)

# Função para extrair detalhes de qualquer exceção
def extract_error_details(error: Exception) -> Dict[str, Any]:
    """Extrai detalhes de qualquer exceção, customizada ou não"""
    if isinstance(error, OceanicDeskError):
        return error.to_dict()
    else:
        return get_error_context(error)
