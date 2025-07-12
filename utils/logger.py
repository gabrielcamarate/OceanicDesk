import logging
from datetime import datetime
from pathlib import Path
from interfaces.alerta_visual import mostrar_alerta_visual

# Criar pasta de logs se não existir
log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"log_{datetime.today().date()}.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()],
)

logger = logging.getLogger("posto_automation")


def registrar_log(mensagem: str):
    """Registra uma mensagem no log e mostra alerta visual para logs importantes"""
    logger.info(mensagem)
    
    # Mostra alerta visual apenas para mensagens importantes
    if any(palavra in mensagem.lower() for palavra in ['erro', 'error', 'falha', 'sucesso', 'concluído', 'finalizado']):
        tipo = 'error' if any(palavra in mensagem.lower() for palavra in ['erro', 'error', 'falha']) else 'success'
        mostrar_alerta_visual("Log registrado", mensagem[:50] + "..." if len(mensagem) > 50 else mensagem, tipo=tipo)


def inicializar_logger():
    """Inicializa o sistema de logging com alerta visual"""
    mostrar_alerta_visual("Sistema de logs", f"Log file: {log_file.name}", tipo="dev")
    logger.info("Sistema de logging inicializado")
    mostrar_alerta_visual("Logger ativo", "Sistema de logs pronto", tipo="success")
