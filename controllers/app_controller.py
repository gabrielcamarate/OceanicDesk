from interfaces.janela_principal import JanelaPrincipal
from utils.etapas import (
    etapa1_backup_e_precos,
    etapa2_minimercado,
    etapa3_litros_descontos,
    etapa4_cashback_pix,
    etapa5_insercao_litros,
    etapa6_envio_email,
    etapa7_fechamento_caixa,
    etapa8_projecao_de_vendas
)
from utils.alerta_visual import mostrar_alerta_visual
import time


class AppController:
    def __init__(self, root):
        self.view = JanelaPrincipal(root, self)

    def log(self, mensagem):
        self.view.log_mensagem(mensagem)

    def etapa1(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 1", "Backup e Preços...", tipo="info")
        self.log("Executando Etapa 1: Backup e Preços...")
        try:
            etapa1_backup_e_precos()
            mostrar_alerta_visual("Etapa 1 concluída", "Backup e Preços finalizados com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa2(completo=True)
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 1", str(e), tipo="error")
            self.log(f"Erro na Etapa 1: {e}")

    def etapa2(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 2", "Mini-Mercado...", tipo="info")
        self.log("Executando Etapa 2: Mini-Mercado...")
        try:
            etapa2_minimercado()
            mostrar_alerta_visual("Etapa 2 concluída", "Mini-Mercado finalizado com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa3(completo=True)
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 2", str(e), tipo="error")
            self.log(f"Erro na Etapa 2: {e}")

    def etapa3(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 3", "Litros e Descontos...", tipo="info")
        self.log("Executando Etapa 3: Litros e Descontos...")
        try:
            etapa3_litros_descontos()
            mostrar_alerta_visual("Etapa 3 concluída", "Litros e Descontos finalizados com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa4(completo=True)
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 3", str(e), tipo="error")
            self.log(f"Erro na Etapa 3: {e}")

    def etapa4(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 4", "Cashback e Pix...", tipo="info")
        self.log("Executando Etapa 4: Cashback e Pix...")
        try:
            etapa4_cashback_pix()
            mostrar_alerta_visual("Etapa 4 concluída", "Cashback e Pix finalizados com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa5(completo=True)
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 4", str(e), tipo="error")
            self.log(f"Erro na Etapa 4: {e}")

    def etapa5(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 5", "Inserção Manual de Litros...", tipo="info")
        self.log("Executando Etapa 5: Inserção Manual de Litros...")
        try:
            etapa5_insercao_litros()
            mostrar_alerta_visual("Etapa 5 concluída", "Inserção Manual de Litros finalizada com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa6(completo=True)
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 5", str(e), tipo="error")
            self.log(f"Erro na Etapa 5: {e}")

    def etapa6(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 6", "Envio de Relatório por E-mail...", tipo="info")
        self.log("Executando Etapa 6: Envio de Relatório por E-mail...")
        try:
            etapa6_envio_email()
            mostrar_alerta_visual("Etapa 6 concluída", "Relatório enviado com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa7(completo=True)
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 6", str(e), tipo="error")
            self.log(f"Erro na Etapa 6: {e}")

    def etapa7(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 7", "Fechamento de Caixa (EMSys)...", tipo="info")
        self.log("Executando Etapa 7: Fechamento de Caixa (EMSys)...")
        try:
            etapa7_fechamento_caixa()
            mostrar_alerta_visual("Etapa 7 concluída", "Fechamento de Caixa finalizado com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa8(completo=True)
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 7", str(e), tipo="error")
            self.log(f"Erro na Etapa 7: {e}")

    def etapa8(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 8", "Projeção de vendas...", tipo="info")
        self.log("Executando Etapa 8: Projeção de vendas...")
        try:
            etapa8_projecao_de_vendas()
            mostrar_alerta_visual("Etapa 8 concluída", "Projeção de vendas finalizada com sucesso!", tipo="success")
        except Exception as e:
            mostrar_alerta_visual("Erro na Etapa 8", str(e), tipo="error")
            self.log(f"Erro na Etapa 8: {e}")

    def executar_todas(self):
        self.etapa1()
        self.etapa2()
        self.etapa3()
        self.etapa4()
        self.etapa5()
        self.etapa6()
        self.etapa7()
        self.etapa8()
