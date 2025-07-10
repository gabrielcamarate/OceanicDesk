import unittest
import os
from utils.arquivos import criar_backup_planilha


class TestArquivos(unittest.TestCase):
    def test_criar_backup(self):
        caminho = "tests/base_teste.xlsx"
        criar_backup_planilha(caminho)
        backups = [
            f
            for f in os.listdir("backups")
            if f.startswith("backup_") and f.endswith(".xlsx")
        ]
        self.assertTrue(any("base_teste" not in f for f in backups))


if __name__ == "__main__":
    unittest.main()
