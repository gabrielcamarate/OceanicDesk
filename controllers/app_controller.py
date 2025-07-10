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


class AppController:
    def __init__(self, root):
        self.view = JanelaPrincipal(root, self)

    def log(self, mensagem):
        self.view.log_mensagem(mensagem)

    def etapa1(self, completo=False):
        self.log("Executando Etapa 1: Backup e Preços...")
        etapa1_backup_e_precos()
        if completo:
            self.etapa2(completo=True)  

    def etapa2(self, completo=False):
        self.log("Executando Etapa 2: Mini-Mercado...")
        etapa2_minimercado()
        if completo:
            self.etapa3(completo=True)  

    def etapa3(self, completo=False):
        self.log("Executando Etapa 3: Litros e Descontos...")
        etapa3_litros_descontos()
        if completo:
            self.etapa4(completo=True)  

    def etapa4(self, completo=False):
        self.log("Executando Etapa 4: Cashback e Pix...")
        etapa4_cashback_pix()
        if completo:
            self.etapa5(completo=True)  

    def etapa5(self, completo=False):
        self.log("Executando Etapa 5: Inserção Manual de Litros...")
        etapa5_insercao_litros()
        if completo:
            self.etapa6(completo=True)  

    def etapa6(self, completo=False):
        self.log("Executando Etapa 6: Envio de Relatório por E-mail...")
        etapa6_envio_email()
        if completo:
            self.etapa7(completo=True)  

    def etapa7(self, completo=False):
        self.log("Executando Etapa 7: Fechamento de Caixa (EMSys)...")
        etapa7_fechamento_caixa()
        if completo:
            self.etapa8(completo=True)  

    def etapa8(self, completo=False):
        self.log("Executando Etapa 8: Projeção de vendas...")
        etapa8_projecao_de_vendas()
        
    def executar_todas(self):
        self.etapa1()
        self.etapa2()
        self.etapa3()
        self.etapa4()
        self.etapa5()
        self.etapa6()
        self.etapa7()
        self.etapa8()
