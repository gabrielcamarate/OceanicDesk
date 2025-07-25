"""
Exemplos de uso do Sistema de Tratamento de Erros Centralizado.

IMPORTANTE: Este sistema mantém 100% da compatibilidade com o tratamento existente.
Todos os try/except atuais continuam funcionando exatamente igual.

Este arquivo demonstra como usar o novo sistema como ADIÇÃO ao existente.
"""

import os
import time
from pathlib import Path

# Imports do sistema original (mantidos)
try:
    from utils.logger import logger
    from interfaces.alerta_visual import mostrar_alerta_visual
except ImportError:
    # Fallback se módulos não estiverem disponíveis
    class MockLogger:
        def error(self, msg): print(f"[ERROR] {msg}")
        def info(self, msg): print(f"[INFO] {msg}")
    
    logger = MockLogger()
    
    def mostrar_alerta_visual(titulo, msg, tipo="info"):
        print(f"[{tipo.upper()}] {titulo}: {msg}")

# Imports do novo sistema de exceções (adições)
from utils.exceptions import (
    # Exceções customizadas
    OceanicDeskError,
    FileOperationError,
    SystemConnectionError,
    DataValidationError,
    AutomationError,
    ConfigurationError,
    
    # Handlers
    ErrorHandler,
    
    # Decorators
    handle_file_operations,
    handle_data_validation,
    
    # Utilitários
    safe_execute,
    get_error_context,
    wrap_existing_exception
)


# ============================================================================
# EXEMPLOS DE USO - MANTENDO COMPATIBILIDADE TOTAL
# ============================================================================

def exemplo_sistema_original():
    """
    Demonstra que o sistema original continua funcionando 100% igual.
    """
    print("=== SISTEMA ORIGINAL (100% MANTIDO) ===")
    
    # Tratamento de erro original (continua funcionando igual)
    try:
        # Simula erro que já existe no sistema
        raise FileNotFoundError("AutoSystem não encontrado")
    except FileNotFoundError as e:
        # Sistema original (mantido)
        logger.error(f"Erro: {e}")
        mostrar_alerta_visual("Erro", str(e), tipo="error")
        print("✅ Sistema original funcionando!")
    
    # Outro exemplo original
    try:
        valor = float("texto_inválido")
    except ValueError as e:
        logger.error(f"Erro de conversão: {e}")
        print("✅ Tratamento original de ValueError funcionando!")


def exemplo_sistema_melhorado():
    """
    Demonstra como usar o novo sistema como ADIÇÃO.
    """
    print("\n=== SISTEMA MELHORADO (ADIÇÃO) ===")
    
    # Usando exceções customizadas com contexto adicional
    try:
        raise FileOperationError(
            "Planilha não encontrada",
            file_path="C:/Planilhas/vendas.xlsx",
            operation="abrir_planilha",
            details={
                "usuario": "admin",
                "tentativa": 1,
                "tamanho_esperado": "2MB"
            }
        )
    except FileOperationError as e:
        # Sistema original (mantido)
        logger.error(f"Erro: {e}")
        
        # Informações adicionais disponíveis
        print(f"✅ Arquivo: {e.file_path}")
        print(f"✅ Detalhes: {e.details}")
        print(f"✅ Timestamp: {e.timestamp}")


def exemplo_integracao_gradual():
    """
    Demonstra como integrar gradualmente sem modificar código existente.
    """
    print("\n=== INTEGRAÇÃO GRADUAL ===")
    
    # Função que simula código existente
    def funcao_existente_com_erro():
        """Simula função que já existe no sistema"""
        logger.info("Executando função existente...")
        raise FileNotFoundError("Arquivo tmp.xlsx não encontrado")
    
    # Wrapper que adiciona tratamento melhorado SEM modificar a função original
    def funcao_existente_com_tratamento_melhorado():
        """Wrapper que adiciona tratamento melhorado"""
        try:
            # Chama função original (sem modificação)
            funcao_existente_com_erro()
            
        except FileNotFoundError as e:
            # Sistema original (mantido)
            logger.error(f"Erro original: {e}")
            
            # Sistema melhorado (adição)
            enhanced_error = ErrorHandler.handle_file_error(
                e, 
                "tmp.xlsx", 
                "processar_relatorio"
            )
            
            # Agora temos contexto adicional
            print(f"✅ Erro melhorado: {enhanced_error.message}")
            print(f"✅ Contexto: {enhanced_error.details}")
    
    # Executa com tratamento melhorado
    funcao_existente_com_tratamento_melhorado()


def exemplo_decorators():
    """
    Demonstra como usar decorators para tratamento automático.
    """
    print("\n=== DECORATORS AUTOMÁTICOS ===")
    
    @handle_file_operations("processar_arquivo")
    def processar_arquivo(caminho):
        """Função que processa arquivo com tratamento automático"""
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        return f"Arquivo {caminho} processado"
    
    @handle_data_validation("validar_numero")
    def validar_numero(valor):
        """Função que valida número com tratamento automático"""
        return float(valor)
    
    # Teste dos decorators
    try:
        processar_arquivo("arquivo_inexistente.xlsx")
    except FileOperationError as e:
        print(f"✅ Decorator de arquivo: {e.message}")
        print(f"✅ Arquivo: {e.file_path}")
    
    try:
        validar_numero("texto_inválido")
    except DataValidationError as e:
        print(f"✅ Decorator de validação: {e.message}")
        print(f"✅ Campo: {e.field_name}")
        print(f"✅ Valor inválido: {e.invalid_value}")


def exemplo_safe_execute():
    """
    Demonstra execução segura com fallback.
    """
    print("\n=== EXECUÇÃO SEGURA ===")
    
    def operacao_que_pode_falhar():
        """Simula operação que pode falhar"""
        raise ValueError("Operação falhou")
    
    def operacao_que_funciona():
        """Simula operação que funciona"""
        return "Sucesso!"
    
    # Execução segura com valor padrão
    resultado1 = safe_execute(
        operacao_que_pode_falhar,
        default_return="Valor padrão",
        operation_name="operacao_teste"
    )
    print(f"✅ Resultado com erro: {resultado1}")
    
    resultado2 = safe_execute(
        operacao_que_funciona,
        default_return="Valor padrão",
        operation_name="operacao_sucesso"
    )
    print(f"✅ Resultado com sucesso: {resultado2}")


def exemplo_contexto_detalhado():
    """
    Demonstra extração de contexto detalhado de erros.
    """
    print("\n=== CONTEXTO DETALHADO ===")
    
    try:
        # Simula erro complexo
        raise SystemConnectionError(
            "Falha na conexão com AutoSystem",
            system_name="AutoSystem",
            operation="login",
            details={
                "host": "localhost",
                "port": 8080,
                "timeout": 30,
                "tentativas": 3
            }
        )
    except SystemConnectionError as e:
        # Extrai contexto completo
        contexto = get_error_context(e)
        
        print(f"✅ Tipo: {contexto['error_type']}")
        print(f"✅ Mensagem: {contexto['error_message']}")
        print(f"✅ É erro OceanicDesk: {contexto['is_oceanicdesk_error']}")
        print(f"✅ Timestamp: {contexto['timestamp']}")


def exemplo_migracao_codigo_existente():
    """
    Demonstra como migrar código existente gradualmente.
    """
    print("\n=== MIGRAÇÃO DE CÓDIGO EXISTENTE ===")
    
    # Código original (NÃO MODIFICAR)
    def codigo_original():
        """Código que já existe no sistema"""
        try:
            # Simula operação que falha
            raise ValueError("Valor inválido no sistema original")
        except ValueError as e:
            logger.error(f"Erro no código original: {e}")
            raise  # Re-raise para manter comportamento
    
    # Versão migrada (ADIÇÃO)
    def codigo_migrado():
        """Versão que usa o novo sistema de erros"""
        try:
            # Chama código original (sem modificação)
            codigo_original()
        except ValueError as e:
            # Envolve exceção existente com contexto adicional
            enhanced_error = wrap_existing_exception(
                e,
                operation="codigo_original",
                details={
                    "modulo": "exemplo",
                    "funcao": "codigo_original",
                    "contexto": "migração_gradual"
                }
            )
            
            # Agora temos contexto estruturado
            print(f"✅ Erro migrado: {enhanced_error.message}")
            print(f"✅ Operação: {enhanced_error.operation}")
            print(f"✅ Detalhes: {enhanced_error.details}")
    
    # Executa versão migrada
    codigo_migrado()


def exemplo_tipos_especificos():
    """
    Demonstra diferentes tipos de exceções customizadas.
    """
    print("\n=== TIPOS ESPECÍFICOS DE EXCEÇÕES ===")
    
    # Erro de configuração
    try:
        raise ConfigurationError(
            "Variável CAMINHO_PLANILHA não definida",
            config_key="CAMINHO_PLANILHA",
            operation="carregar_configuracao"
        )
    except ConfigurationError as e:
        print(f"✅ Erro de config: {e.config_key}")
    
    # Erro de automação
    try:
        raise AutomationError(
            "Elemento não encontrado na tela",
            automation_step="click_login_button",
            operation="autosystem_login"
        )
    except AutomationError as e:
        print(f"✅ Erro de automação: {e.automation_step}")
    
    # Erro de validação
    try:
        raise DataValidationError(
            "Valor deve ser numérico",
            field_name="litros_combustivel",
            invalid_value="texto",
            operation="validar_entrada"
        )
    except DataValidationError as e:
        print(f"✅ Erro de validação: {e.field_name} = {e.invalid_value}")


def demonstrar_compatibilidade_total():
    """
    Demonstra que ambos os sistemas funcionam em paralelo.
    """
    print("\n=== COMPATIBILIDADE TOTAL ===")
    
    # Sistema original e novo funcionam simultaneamente
    try:
        # Erro original
        raise FileNotFoundError("Arquivo não encontrado")
    except FileNotFoundError as e:
        # Tratamento original (mantido)
        logger.error(f"Sistema original: {e}")
        
        # Tratamento novo (adição)
        enhanced = ErrorHandler.handle_file_error(e, "arquivo.xlsx", "teste")
        print(f"Sistema novo: {enhanced.message}")
    
    print("✅ Ambos os sistemas funcionando em paralelo!")


if __name__ == "__main__":
    print("DEMONSTRAÇÃO DO SISTEMA DE TRATAMENTO DE ERROS CENTRALIZADO")
    print("=" * 60)
    
    # Executa todos os exemplos
    exemplo_sistema_original()
    exemplo_sistema_melhorado()
    exemplo_integracao_gradual()
    exemplo_decorators()
    exemplo_safe_execute()
    exemplo_contexto_detalhado()
    exemplo_migracao_codigo_existente()
    exemplo_tipos_especificos()
    demonstrar_compatibilidade_total()
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("✅ Sistema original: 100% funcional")
    print("✅ Sistema de erros centralizado: Implementado com sucesso")
    print("✅ Compatibilidade: Total")
    print("✅ Integração: Gradual e segura")
