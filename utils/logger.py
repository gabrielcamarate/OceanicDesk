import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import traceback
import sys

class StructuredLogger:
    """
    Logger estruturado para operações do sistema.
    Mantém compatibilidade total com o sistema de logging existente.
    """

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.setup_handlers()

    def setup_handlers(self):
        """Configura handlers para o logger estruturado"""
        if not self.logger.handlers:
            # Usar a mesma configuração do logger principal
            log_dir = Path(__file__).resolve().parent.parent / "logs"
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / f"structured_log_{datetime.today().date()}.log"

            # Handler para arquivo estruturado
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.INFO)

            # Formato JSON para logs estruturados
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.INFO)

    def log_operation(self, operation: str, status: str, details: Dict[str, Any] = None):
        """Log estruturado para operações"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": status,
            "details": details or {},
            "level": "INFO"
        }
        self.logger.info(json.dumps(log_data, ensure_ascii=False, indent=None))

    def log_error(self, operation: str, error: Exception, details: Dict[str, Any] = None):
        """Log estruturado para erros"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": "ERROR",
            "error": {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            },
            "details": details or {},
            "level": "ERROR"
        }
        self.logger.error(json.dumps(log_data, ensure_ascii=False, indent=None))

    def log_performance(self, operation: str, duration_ms: float, details: Dict[str, Any] = None):
        """Log estruturado para métricas de performance"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "status": "PERFORMANCE",
            "performance": {
                "duration_ms": duration_ms,
                "duration_seconds": duration_ms / 1000
            },
            "details": details or {},
            "level": "INFO"
        }
        self.logger.info(json.dumps(log_data, ensure_ascii=False, indent=None))

# ============================================================================
# SISTEMA DE LOGGING ORIGINAL - MANTIDO 100% FUNCIONAL
# ============================================================================

# Criar pasta de logs se não existir
log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"log_{datetime.today().date()}.log"

# Configuração original mantida exatamente igual
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()],
)

# Logger original mantido
logger = logging.getLogger("posto_automation")

# ============================================================================
# INSTÂNCIAS DO NOVO SISTEMA ESTRUTURADO (ADIÇÃO)
# ============================================================================

# Logger estruturado para operações principais
structured_logger = StructuredLogger("posto_automation_structured")

# Logger estruturado para performance
performance_logger = StructuredLogger("posto_performance")

# ============================================================================
# FUNÇÕES ORIGINAIS - MANTIDAS 100% IGUAIS
# ============================================================================

def registrar_log(mensagem: str):
    """Registra uma mensagem no log e mostra alerta visual para logs importantes"""
    logger.info(mensagem)

    # Mostra alerta visual apenas para mensagens importantes
    if any(palavra in mensagem.lower() for palavra in ['erro', 'error', 'falha', 'sucesso', 'concluído', 'finalizado']):
        tipo = 'error' if any(palavra in mensagem.lower() for palavra in ['erro', 'error', 'falha']) else 'success'


def inicializar_logger():
    """Inicializa o sistema de logging com alerta visual"""
    logger.info("Sistema de logging inicializado")
    # ADIÇÃO: Inicializar também o sistema estruturado
    structured_logger.log_operation("system_startup", "SUCCESS", {"component": "logger"})

# ============================================================================
# NOVAS FUNÇÕES DE CONVENIÊNCIA (ADIÇÃO)
# ============================================================================

def log_operacao(operacao: str, status: str, detalhes: Optional[Dict[str, Any]] = None):
    """
    Função de conveniência para logging estruturado de operações.
    Complementa o sistema existente sem substituí-lo.
    """
    structured_logger.log_operation(operacao, status, detalhes)

def log_erro(operacao: str, erro: Exception, detalhes: Optional[Dict[str, Any]] = None):
    """
    Função de conveniência para logging estruturado de erros.
    Complementa o sistema existente sem substituí-lo.
    """
    structured_logger.log_error(operacao, erro, detalhes)

def log_performance(operacao: str, duracao_ms: float, detalhes: Optional[Dict[str, Any]] = None):
    """
    Função de conveniência para logging de performance.
    Complementa o sistema existente sem substituí-lo.
    """
    performance_logger.log_performance(operacao, duracao_ms, detalhes)
 
