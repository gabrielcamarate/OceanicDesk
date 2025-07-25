"""
Sistema de Validação de Entrada Robusta - OceanicDesk

IMPORTANTE: Este sistema mantém 100% da compatibilidade com as validações existentes.
Todas as validações e conversões atuais continuam funcionando exatamente igual.

Este módulo adiciona:
1. Validadores robustos para diferentes tipos de dados
2. Conversores seguros com fallback
3. Validações específicas para o domínio do posto de combustível
4. Integração com sistema de logging e tratamento de erros
"""

import re
import os
from pathlib import Path
from typing import Any, Union, Optional, List, Dict, Callable
from decimal import Decimal, InvalidOperation
from datetime import datetime, date

# Import do sistema de exceções (se disponível)
try:
    from utils.exceptions import DataValidationError, ConfigurationError
    EXCEPTIONS_AVAILABLE = True
except ImportError:
    EXCEPTIONS_AVAILABLE = False

# Import do sistema de logging (se disponível)
try:
    from utils.logger import log_operacao, log_erro, logger
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False

# ============================================================================
# VALIDADORES BÁSICOS (ADIÇÃO AO SISTEMA EXISTENTE)
# ============================================================================

class BaseValidator:
    """
    Classe base para todos os validadores.
    Mantém compatibilidade total com validações existentes.
    """
    
    def __init__(self, field_name: str = "unknown_field", operation: str = "validation"):
        self.field_name = field_name
        self.operation = operation
    
    def validate(self, value: Any) -> Any:
        """Método base de validação - deve ser sobrescrito"""
        return value
    
    def _log_validation(self, value: Any, result: Any, status: str = "SUCCESS"):
        """Log da validação se sistema de logging estiver disponível"""
        if LOGGING_AVAILABLE:
            log_operacao(f"validate_{self.field_name}", status, {
                "validator": self.__class__.__name__,
                "input_value": str(value)[:100],
                "input_type": type(value).__name__,
                "output_value": str(result)[:100] if result is not None else None,
                "output_type": type(result).__name__ if result is not None else None
            })
    
    def _raise_validation_error(self, message: str, value: Any):
        """Levanta erro de validação com contexto estruturado"""
        if EXCEPTIONS_AVAILABLE:
            raise DataValidationError(
                message,
                field_name=self.field_name,
                invalid_value=value,
                operation=self.operation
            )
        else:
            # Fallback para ValueError padrão
            raise ValueError(f"{self.field_name}: {message}")


class NumericValidator(BaseValidator):
    """
    Validador para valores numéricos.
    Complementa as conversões float() existentes com validação robusta.
    """
    
    def __init__(self, field_name: str = "numeric_field", 
                 min_value: Optional[float] = None,
                 max_value: Optional[float] = None,
                 allow_negative: bool = True,
                 decimal_places: Optional[int] = None):
        super().__init__(field_name, "numeric_validation")
        self.min_value = min_value
        self.max_value = max_value
        self.allow_negative = allow_negative
        self.decimal_places = decimal_places
    
    def validate(self, value: Any) -> float:
        """
        Valida e converte valor para float.
        Mantém compatibilidade com conversões existentes.
        """
        original_value = value
        
        try:
            # Conversão robusta (compatível com sistema existente)
            if isinstance(value, (int, float)):
                result = float(value)
            elif isinstance(value, Decimal):
                result = float(value)
            elif isinstance(value, str):
                # Limpeza compatível com sistema existente
                # Primeiro remove espaços e caracteres especiais, mantendo pontos e vírgulas
                cleaned = re.sub(r'[^\d\-\+\.,]', '', value.strip())

                # Se tem vírgula, assume formato brasileiro (vírgula = decimal)
                if ',' in cleaned:
                    # Se tem ponto E vírgula, assume ponto = separador de milhares
                    if '.' in cleaned and ',' in cleaned:
                        # Ex: "1.500,50" -> "1500.50"
                        cleaned = cleaned.replace('.', '').replace(',', '.')
                    else:
                        # Ex: "1500,50" -> "1500.50"
                        cleaned = cleaned.replace(',', '.')
                # Se só tem ponto, pode ser decimal ou separador de milhares
                elif '.' in cleaned:
                    # Se tem mais de um ponto ou ponto não está nas últimas 3 posições, é separador de milhares
                    dot_count = cleaned.count('.')
                    last_dot_pos = cleaned.rfind('.')
                    if dot_count > 1 or (len(cleaned) - last_dot_pos - 1) > 3:
                        # Ex: "1.500.000" ou "1.5000" -> "1500000" ou "15000"
                        cleaned = cleaned.replace('.', '')
                    # Senão, mantém como decimal

                result = float(cleaned) if cleaned else 0.0
            else:
                raise ValueError(f"Tipo não suportado: {type(value)}")
            
            # Validações adicionais
            if not self.allow_negative and result < 0:
                self._raise_validation_error(
                    f"Valor não pode ser negativo: {result}",
                    original_value
                )
            
            if self.min_value is not None and result < self.min_value:
                self._raise_validation_error(
                    f"Valor deve ser maior ou igual a {self.min_value}: {result}",
                    original_value
                )
            
            if self.max_value is not None and result > self.max_value:
                self._raise_validation_error(
                    f"Valor deve ser menor ou igual a {self.max_value}: {result}",
                    original_value
                )
            
            # Arredondamento se especificado
            if self.decimal_places is not None:
                result = round(result, self.decimal_places)
            
            self._log_validation(original_value, result)
            return result
            
        except (ValueError, InvalidOperation) as e:
            self._log_validation(original_value, None, "ERROR")
            self._raise_validation_error(
                f"Não foi possível converter para número: {original_value}",
                original_value
            )


class FilePathValidator(BaseValidator):
    """
    Validador para caminhos de arquivo.
    Complementa as verificações os.path.exists() existentes.
    """
    
    def __init__(self, field_name: str = "file_path",
                 must_exist: bool = True,
                 allowed_extensions: Optional[List[str]] = None,
                 create_if_missing: bool = False):
        super().__init__(field_name, "file_validation")
        self.must_exist = must_exist
        self.allowed_extensions = allowed_extensions or []
        self.create_if_missing = create_if_missing
    
    def validate(self, value: Any) -> Path:
        """
        Valida caminho de arquivo.
        Mantém compatibilidade com verificações existentes.
        """
        original_value = value
        
        try:
            # Conversão para Path
            if isinstance(value, str):
                path = Path(value)
            elif isinstance(value, Path):
                path = value
            else:
                self._raise_validation_error(
                    f"Caminho deve ser string ou Path: {type(value)}",
                    original_value
                )
            
            # Validação de existência
            if self.must_exist and not path.exists():
                if self.create_if_missing:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.touch()
                else:
                    self._raise_validation_error(
                        f"Arquivo não encontrado: {path}",
                        original_value
                    )
            
            # Validação de extensão
            if self.allowed_extensions and path.suffix.lower() not in self.allowed_extensions:
                self._raise_validation_error(
                    f"Extensão não permitida. Permitidas: {self.allowed_extensions}. Encontrada: {path.suffix}",
                    original_value
                )
            
            self._log_validation(original_value, str(path))
            return path
            
        except Exception as e:
            self._log_validation(original_value, None, "ERROR")
            if not isinstance(e, (DataValidationError, ValueError)):
                self._raise_validation_error(
                    f"Erro ao validar caminho: {e}",
                    original_value
                )
            raise


class CombustivelValidator(BaseValidator):
    """
    Validador específico para dados de combustível.
    Validações específicas do domínio do posto.
    """
    
    TIPOS_COMBUSTIVEL = ["etanol", "aditivada", "diesel", "comum"]
    
    def __init__(self, field_name: str = "combustivel"):
        super().__init__(field_name, "combustivel_validation")
    
    def validate_tipo(self, tipo: str) -> str:
        """Valida tipo de combustível"""
        tipo_lower = tipo.lower().strip()
        
        if tipo_lower not in self.TIPOS_COMBUSTIVEL:
            self._raise_validation_error(
                f"Tipo de combustível inválido. Permitidos: {self.TIPOS_COMBUSTIVEL}. Recebido: {tipo}",
                tipo
            )
        
        self._log_validation(tipo, tipo_lower)
        return tipo_lower
    
    def validate_litros(self, litros: Any) -> float:
        """Valida quantidade de litros"""
        validator = NumericValidator(
            field_name=f"{self.field_name}_litros",
            min_value=0.0,
            max_value=50000.0,  # Limite razoável para tanque de posto
            allow_negative=False,
            decimal_places=2
        )
        return validator.validate(litros)
    
    def validate_preco(self, preco: Any) -> float:
        """Valida preço do combustível"""
        validator = NumericValidator(
            field_name=f"{self.field_name}_preco",
            min_value=0.01,
            max_value=20.0,  # Limite razoável para preço por litro
            allow_negative=False,
            decimal_places=3
        )
        return validator.validate(preco)


class ConfigValidator(BaseValidator):
    """
    Validador para configurações do sistema (.env, etc.).
    Complementa as verificações de configuração existentes.
    """
    
    def __init__(self, field_name: str = "config"):
        super().__init__(field_name, "config_validation")
    
    def validate_env_var(self, var_name: str, required: bool = True) -> Optional[str]:
        """Valida variável de ambiente"""
        value = os.getenv(var_name)
        
        if required and not value:
            if EXCEPTIONS_AVAILABLE:
                raise ConfigurationError(
                    f"Variável de ambiente obrigatória não definida: {var_name}",
                    config_key=var_name,
                    operation="env_validation"
                )
            else:
                raise ValueError(f"Variável de ambiente obrigatória não definida: {var_name}")
        
        self._log_validation(var_name, value or "None")
        return value
    
    def validate_planilha_path(self, path: Any) -> Path:
        """Valida caminho de planilha Excel"""
        validator = FilePathValidator(
            field_name="planilha_path",
            must_exist=True,
            allowed_extensions=[".xlsx", ".xls"]
        )
        return validator.validate(path)


# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA (COMPATÍVEIS COM SISTEMA EXISTENTE)
# ============================================================================

def safe_float(value: Any, default: float = 0.0, field_name: str = "numeric_value") -> float:
    """
    Conversão segura para float com fallback.
    Complementa as conversões float() existentes no sistema.
    """
    try:
        validator = NumericValidator(field_name=field_name)
        return validator.validate(value)
    except Exception:
        if LOGGING_AVAILABLE:
            logger.warning(f"Conversão float falhou para {value}, usando padrão {default}")
        return default


def safe_int(value: Any, default: int = 0, field_name: str = "integer_value") -> int:
    """
    Conversão segura para int com fallback.
    """
    try:
        float_val = safe_float(value, default, field_name)
        return int(float_val)
    except Exception:
        if LOGGING_AVAILABLE:
            logger.warning(f"Conversão int falhou para {value}, usando padrão {default}")
        return default


def validate_file_exists(file_path: Any, field_name: str = "file_path") -> Path:
    """
    Validação robusta de existência de arquivo.
    Complementa as verificações os.path.exists() existentes.
    """
    validator = FilePathValidator(field_name=field_name, must_exist=True)
    return validator.validate(file_path)


def validate_excel_file(file_path: Any, field_name: str = "excel_file") -> Path:
    """
    Validação específica para arquivos Excel.
    """
    validator = FilePathValidator(
        field_name=field_name,
        must_exist=True,
        allowed_extensions=[".xlsx", ".xls"]
    )
    return validator.validate(file_path)


def validate_combustivel_data(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Validação completa de dados de combustível.
    Mantém compatibilidade com estrutura existente.
    """
    validator = CombustivelValidator()
    validated_data = {}
    
    for tipo in CombustivelValidator.TIPOS_COMBUSTIVEL:
        if tipo in data:
            # Valida tipo
            validated_tipo = validator.validate_tipo(tipo)
            
            # Valida litros
            validated_litros = validator.validate_litros(data[tipo])
            
            validated_data[validated_tipo] = validated_litros
    
    return validated_data


# ============================================================================
# DECORATORS PARA VALIDAÇÃO AUTOMÁTICA
# ============================================================================

def validate_numeric_input(field_name: str = "input", **validator_kwargs):
    """
    Decorator para validação automática de entrada numérica.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Aplica validação no primeiro argumento se for numérico
            if args:
                validator = NumericValidator(field_name=field_name, **validator_kwargs)
                validated_args = list(args)
                try:
                    validated_args[0] = validator.validate(args[0])
                except Exception:
                    # Se validação falhar, mantém comportamento original
                    pass
                args = tuple(validated_args)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_file_input(field_name: str = "file_input", **validator_kwargs):
    """
    Decorator para validação automática de entrada de arquivo.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Aplica validação no primeiro argumento se for caminho
            if args:
                validator = FilePathValidator(field_name=field_name, **validator_kwargs)
                validated_args = list(args)
                try:
                    validated_args[0] = validator.validate(args[0])
                except Exception:
                    # Se validação falhar, mantém comportamento original
                    pass
                args = tuple(validated_args)

            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# VALIDADORES ESPECÍFICOS DO OCEANICDESK
# ============================================================================

class OceanicDeskValidator:
    """
    Validador principal para dados específicos do OceanicDesk.
    Centraliza todas as validações do domínio do posto.
    """

    @staticmethod
    def validate_usuario_sistema(usuario: str) -> str:
        """Valida usuário do sistema"""
        if not usuario or not isinstance(usuario, str):
            raise ValueError("Usuário deve ser uma string não vazia")

        usuario = usuario.strip()
        if len(usuario) < 3:
            raise ValueError("Usuário deve ter pelo menos 3 caracteres")

        return usuario

    @staticmethod
    def validate_senha_sistema(senha: str) -> str:
        """Valida senha do sistema"""
        if not senha or not isinstance(senha, str):
            raise ValueError("Senha deve ser uma string não vazia")

        if len(senha) < 3:
            raise ValueError("Senha deve ter pelo menos 4 caracteres")

        return senha

    @staticmethod
    def validate_data_relatorio(data: Any) -> date:
        """Valida data para relatórios"""
        if isinstance(data, date):
            return data
        elif isinstance(data, datetime):
            return data.date()
        elif isinstance(data, str):
            try:
                # Tenta formatos comuns
                for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]:
                    try:
                        return datetime.strptime(data, fmt).date()
                    except ValueError:
                        continue
                raise ValueError(f"Formato de data não reconhecido: {data}")
            except Exception:
                raise ValueError(f"Não foi possível converter data: {data}")
        else:
            raise ValueError(f"Tipo de data inválido: {type(data)}")

    @staticmethod
    def validate_valor_monetario(valor: Any, campo: str = "valor") -> float:
        """Valida valores monetários"""
        validator = NumericValidator(
            field_name=campo,
            min_value=0.0,
            allow_negative=False,
            decimal_places=2
        )
        return validator.validate(valor)

    @staticmethod
    def validate_percentual(valor: Any, campo: str = "percentual") -> float:
        """Valida valores percentuais (0-100)"""
        validator = NumericValidator(
            field_name=campo,
            min_value=0.0,
            max_value=100.0,
            allow_negative=False,
            decimal_places=2
        )
        return validator.validate(valor)


# ============================================================================
# SISTEMA DE VALIDAÇÃO EM LOTE
# ============================================================================

class BatchValidator:
    """
    Sistema para validação em lote de múltiplos campos.
    Útil para validar formulários e estruturas de dados complexas.
    """

    def __init__(self):
        self.validators = {}
        self.errors = {}
        self.validated_data = {}

    def add_validator(self, field_name: str, validator: BaseValidator):
        """Adiciona validador para um campo"""
        self.validators[field_name] = validator

    def add_numeric_validator(self, field_name: str, **kwargs):
        """Adiciona validador numérico"""
        self.validators[field_name] = NumericValidator(field_name=field_name, **kwargs)

    def add_file_validator(self, field_name: str, **kwargs):
        """Adiciona validador de arquivo"""
        self.validators[field_name] = FilePathValidator(field_name=field_name, **kwargs)

    def validate_all(self, data: Dict[str, Any], stop_on_first_error: bool = False) -> bool:
        """
        Valida todos os campos.
        Retorna True se todos passaram, False caso contrário.
        """
        self.errors.clear()
        self.validated_data.clear()

        for field_name, value in data.items():
            if field_name in self.validators:
                try:
                    validated_value = self.validators[field_name].validate(value)
                    self.validated_data[field_name] = validated_value
                except Exception as e:
                    self.errors[field_name] = str(e)
                    if stop_on_first_error:
                        break
            else:
                # Campo sem validador - passa direto
                self.validated_data[field_name] = value

        return len(self.errors) == 0

    def get_errors(self) -> Dict[str, str]:
        """Retorna erros de validação"""
        return self.errors.copy()

    def get_validated_data(self) -> Dict[str, Any]:
        """Retorna dados validados"""
        return self.validated_data.copy()

    def get_error_summary(self) -> str:
        """Retorna resumo dos erros"""
        if not self.errors:
            return "Nenhum erro de validação"

        summary = f"Encontrados {len(self.errors)} erro(s) de validação:\n"
        for field, error in self.errors.items():
            summary += f"- {field}: {error}\n"

        return summary.strip()


# ============================================================================
# FUNÇÕES DE MIGRAÇÃO GRADUAL
# ============================================================================

def enhance_existing_validation(original_func: Callable, validator: BaseValidator):
    """
    Melhora uma função de validação existente sem modificá-la.
    Útil para migração gradual.
    """
    def enhanced_wrapper(*args, **kwargs):
        # Tenta validação melhorada primeiro
        if args:
            try:
                validated_value = validator.validate(args[0])
                args = (validated_value,) + args[1:]
            except Exception:
                # Se falhar, usa função original
                pass

        # Chama função original
        return original_func(*args, **kwargs)

    return enhanced_wrapper


def create_validation_wrapper(field_name: str, validation_type: str = "numeric", **kwargs):
    """
    Cria wrapper de validação para funções existentes.
    """
    if validation_type == "numeric":
        validator = NumericValidator(field_name=field_name, **kwargs)
    elif validation_type == "file":
        validator = FilePathValidator(field_name=field_name, **kwargs)
    elif validation_type == "combustivel":
        validator = CombustivelValidator(field_name=field_name)
    else:
        validator = BaseValidator(field_name=field_name)

    def wrapper(func: Callable) -> Callable:
        return enhance_existing_validation(func, validator)

    return wrapper


# ============================================================================
# COMPATIBILIDADE COM SISTEMA EXISTENTE
# ============================================================================

# Aliases para manter compatibilidade
validate_float = safe_float
validate_int = safe_int
validate_path = validate_file_exists

# Função para verificar se validação está disponível
def is_validation_available() -> bool:
    """Verifica se sistema de validação está disponível"""
    return True

# Função para obter validador por tipo
def get_validator(validation_type: str, field_name: str = "field", **kwargs) -> BaseValidator:
    """Retorna validador baseado no tipo"""
    validators_map = {
        "numeric": NumericValidator,
        "file": FilePathValidator,
        "combustivel": CombustivelValidator,
        "config": ConfigValidator
    }

    validator_class = validators_map.get(validation_type, BaseValidator)
    return validator_class(field_name=field_name, **kwargs)
