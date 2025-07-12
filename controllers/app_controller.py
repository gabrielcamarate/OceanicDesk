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
from interfaces.alerta_visual import mostrar_alerta_visual, atualizar_progresso, fechar_progresso
import time


class AppController:
    def __init__(self, root):
        self.view = JanelaPrincipal(root, self)

    def log(self, mensagem):
        self.view.log_mensagem(mensagem)

    def etapa1(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 1", "Backup e Preços...", tipo="info")
        self.log("Executando Etapa 1: Backup e Preços...")
        
        # Alerta de progresso para operações múltiplas
        atualizar_progresso("Etapa 1: Backup", "Criando backup da planilha...", 20)
        time.sleep(0.5)
        
        try:
            etapa1_backup_e_precos()
            
            atualizar_progresso("Etapa 1: Concluída", "Backup e preços finalizados!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 1 concluída", "Backup e Preços finalizados com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa2(completo=True)
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 1", str(e), tipo="error")
            self.log(f"Erro na Etapa 1: {e}")

    def etapa2(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 2", "Mini-Mercado...", tipo="info")
        self.log("Executando Etapa 2: Mini-Mercado...")
        
        atualizar_progresso("Etapa 2: Login", "Conectando ao sistema...", 25)
        time.sleep(0.5)
        
        try:
            etapa2_minimercado()
            
            atualizar_progresso("Etapa 2: Concluída", "Mini-mercado processado!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 2 concluída", "Mini-Mercado finalizado com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa3(completo=True)
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 2", str(e), tipo="error")
            self.log(f"Erro na Etapa 2: {e}")

    def etapa3(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 3", "Litros e Descontos...", tipo="info")
        self.log("Executando Etapa 3: Litros e Descontos...")
        
        atualizar_progresso("Etapa 3: Relatório", "Gerando relatório de litros...", 30)
        time.sleep(0.5)
        
        try:
            etapa3_litros_descontos()
            
            atualizar_progresso("Etapa 3: Concluída", "Litros e descontos processados!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 3 concluída", "Litros e Descontos finalizados com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa4(completo=True)
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 3", str(e), tipo="error")
            self.log(f"Erro na Etapa 3: {e}")

    def etapa4(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 4", "Cashback e Pix...", tipo="info")
        self.log("Executando Etapa 4: Cashback e Pix...")
        
        atualizar_progresso("Etapa 4: Dados", "Extraindo dados de cashback...", 40)
        time.sleep(0.5)
        
        try:
            etapa4_cashback_pix()
            
            atualizar_progresso("Etapa 4: Concluída", "Cashback e pix processados!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 4 concluída", "Cashback e Pix finalizados com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa5(completo=True)
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 4", str(e), tipo="error")
            self.log(f"Erro na Etapa 4: {e}")

    def etapa5(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 5", "Inserção Manual de Litros...", tipo="info")
        self.log("Executando Etapa 5: Inserção Manual de Litros...")
        
        atualizar_progresso("Etapa 5: Interface", "Abrindo interface de coleta...", 50)
        time.sleep(0.5)
        
        try:
            etapa5_insercao_litros()
            
            atualizar_progresso("Etapa 5: Concluída", "Litros inseridos com sucesso!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 5 concluída", "Inserção Manual de Litros finalizada com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa6(completo=True)
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 5", str(e), tipo="error")
            self.log(f"Erro na Etapa 5: {e}")

    def etapa6(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 6", "Envio de Relatório por E-mail...", tipo="info")
        self.log("Executando Etapa 6: Envio de Relatório por E-mail...")
        
        atualizar_progresso("Etapa 6: E-mail", "Preparando relatório...", 60)
        time.sleep(0.5)
        
        try:
            etapa6_envio_email()
            
            atualizar_progresso("Etapa 6: Concluída", "E-mail enviado com sucesso!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 6 concluída", "Relatório enviado com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa7(completo=True)
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 6", str(e), tipo="error")
            self.log(f"Erro na Etapa 6: {e}")

    def etapa7(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 7", "Fechamento de Caixa (EMSys)...", tipo="info")
        self.log("Executando Etapa 7: Fechamento de Caixa (EMSys)...")
        
        atualizar_progresso("Etapa 7: EMSys", "Conectando ao sistema...", 70)
        time.sleep(0.5)
        
        try:
            etapa7_fechamento_caixa()
            
            atualizar_progresso("Etapa 7: Concluída", "Fechamento finalizado!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 7 concluída", "Fechamento de Caixa finalizado com sucesso!", tipo="success")
            if completo:
                time.sleep(0.5)  # Delay entre etapas
                self.etapa8(completo=True)
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 7", str(e), tipo="error")
            self.log(f"Erro na Etapa 7: {e}")

    def etapa8(self, completo=False):
        mostrar_alerta_visual("Iniciando Etapa 8", "Projeção de vendas...", tipo="info")
        self.log("Executando Etapa 8: Projeção de vendas...")
        
        atualizar_progresso("Etapa 8: Projeção", "Processando dados de vendas...", 80)
        time.sleep(0.5)
        
        try:
            etapa8_projecao_de_vendas()
            
            atualizar_progresso("Etapa 8: Concluída", "Projeção finalizada!", 100)
            time.sleep(1)
            fechar_progresso()
            
            mostrar_alerta_visual("Etapa 8 concluída", "Projeção de vendas finalizada com sucesso!", tipo="success")
        except Exception as e:
            fechar_progresso()
            mostrar_alerta_visual("Erro na Etapa 8", str(e), tipo="error")
            self.log(f"Erro na Etapa 8: {e}")

    def executar_todas(self):
        """Executa todas as etapas com progresso dinâmico"""
        self.log("Iniciando execução completa de todas as etapas...")
        
        # Progresso geral
        etapas = [
            ("Etapa 1: Backup e Preços", self.etapa1),
            ("Etapa 2: Mini-Mercado", self.etapa2),
            ("Etapa 3: Litros e Descontos", self.etapa3),
            ("Etapa 4: Cashback e Pix", self.etapa4),
            ("Etapa 5: Inserção de Litros", self.etapa5),
            ("Etapa 6: Envio de E-mail", self.etapa6),
            ("Etapa 7: Fechamento de Caixa", self.etapa7),
            ("Etapa 8: Projeção de Vendas", self.etapa8)
        ]
        
        for i, (nome, etapa_func) in enumerate(etapas):
            progresso = int((i / len(etapas)) * 100)
            atualizar_progresso("Execução Completa", f"{nome} ({i+1}/{len(etapas)})", progresso)
            
            try:
                etapa_func()
                time.sleep(0.5)
            except Exception as e:
                self.log(f"Erro na {nome}: {e}")
                break
        
        fechar_progresso()
        mostrar_alerta_visual("Execução Completa", "Todas as etapas foram processadas!", tipo="success")
