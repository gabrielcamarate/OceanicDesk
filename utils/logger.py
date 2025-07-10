import logging
from datetime import datetime
from pathlib import Path

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
    logger.info(mensagem)
