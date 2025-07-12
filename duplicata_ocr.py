import os
import pytesseract
from utils.path_utils import get_system_path

# Configura o caminho do Tesseract dinamicamente
TESSERACT_CMD = os.getenv("TESSERACT_CMD", get_system_path("tesseract"))
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD 