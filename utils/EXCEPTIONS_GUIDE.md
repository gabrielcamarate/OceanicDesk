# Sistema de Tratamento de Erros Centralizado - OceanicDesk

## ✅ COMPATIBILIDADE TOTAL GARANTIDA

**IMPORTANTE**: O sistema original continua funcionando 100% igual. Nada foi quebrado ou modificado.

## 📋 Resumo da Implementação

### Sistema Original (Mantido)
- ✅ `try/except` padrão - Funciona exatamente igual
- ✅ `raise Exception()` - Funciona exatamente igual  
- ✅ `FileNotFoundError`, `ValueError`, etc. - Funcionam exatamente igual
- ✅ `logger.error()` - Funciona exatamente igual
- ✅ `messagebox.showerror()` - Funciona exatamente igual

### Sistema Centralizado (Adicionado)
- 🆕 **Exceções Customizadas** - Contexto estruturado para diferentes tipos de erro
- 🆕 **Handlers Centralizados** - Tratamento consistente e automático
- 🆕 **Integração com Logging** - Logs estruturados automáticos
- 🆕 **Decorators** - Tratamento automático sem modificar código
- 🆕 **Utilitários** - Execução segura e extração de contexto

## 🚀 Exceções Customizadas Disponíveis

### 1. **FileOperationError**
Para erros relacionados a arquivos (Excel, backup, etc.)
```python
from utils.exceptions import FileOperationError

raise FileOperationError(
    "Planilha não encontrada",
    file_path="C:/Planilhas/vendas.xlsx",
    operation="abrir_planilha",
    details={
        "usuario": "admin",
        "tamanho_esperado": "2MB"
    }
)
```

### 2. **SystemConnectionError**
Para erros de conexão com sistemas externos (AutoSystem, EMSys)
```python
from utils.exceptions import SystemConnectionError

raise SystemConnectionError(
    "Falha na conexão com AutoSystem",
    system_name="AutoSystem",
    operation="login",
    details={
        "host": "localhost",
        "timeout": 30
    }
)
```

### 3. **DataValidationError**
Para erros de validação de dados
```python
from utils.exceptions import DataValidationError

raise DataValidationError(
    "Valor deve ser numérico",
    field_name="litros_combustivel",
    invalid_value="texto",
    operation="validar_entrada"
)
```

### 4. **AutomationError**
Para erros durante automação (pyautogui, OCR)
```python
from utils.exceptions import AutomationError

raise AutomationError(
    "Elemento não encontrado na tela",
    automation_step="click_login_button",
    operation="autosystem_login"
)
```

### 5. **ConfigurationError**
Para erros de configuração (.env, caminhos)
```python
from utils.exceptions import ConfigurationError

raise ConfigurationError(
    "Variável CAMINHO_PLANILHA não definida",
    config_key="CAMINHO_PLANILHA",
    operation="carregar_configuracao"
)
```

## 🔧 Handlers Centralizados

### ErrorHandler.handle_file_error()
Converte erros de arquivo padrão em FileOperationError
```python
from utils.exceptions import ErrorHandler

try:
    open("arquivo_inexistente.txt")
except FileNotFoundError as e:
    enhanced_error = ErrorHandler.handle_file_error(
        e, "arquivo_inexistente.txt", "abrir_arquivo"
    )
    # Agora temos contexto estruturado
    print(enhanced_error.details)
```

### ErrorHandler.handle_validation_error()
Converte erros de validação em DataValidationError
```python
try:
    float("texto_inválido")
except ValueError as e:
    enhanced_error = ErrorHandler.handle_validation_error(
        e, "valor_numerico", "texto_inválido", "validar_entrada"
    )
```

## 🎯 Decorators para Tratamento Automático

### @handle_file_operations
Tratamento automático de erros de arquivo
```python
from utils.exceptions import handle_file_operations

@handle_file_operations("processar_planilha")
def processar_planilha(caminho):
    # Se houver FileNotFoundError, será automaticamente
    # convertido em FileOperationError com contexto
    with open(caminho) as f:
        return f.read()
```

### @handle_data_validation
Tratamento automático de erros de validação
```python
from utils.exceptions import handle_data_validation

@handle_data_validation("converter_numero")
def converter_numero(valor):
    # Se houver ValueError, será automaticamente
    # convertido em DataValidationError com contexto
    return float(valor)
```

## 🛡️ Execução Segura

### safe_execute()
Executa função com fallback em caso de erro
```python
from utils.exceptions import safe_execute

def operacao_que_pode_falhar():
    raise ValueError("Falha")

# Execução segura com valor padrão
resultado = safe_execute(
    operacao_que_pode_falhar,
    default_return="Valor padrão",
    operation_name="operacao_teste"
)
# resultado = "Valor padrão"
```

## 🔍 Extração de Contexto

### get_error_context()
Extrai contexto detalhado de qualquer exceção
```python
from utils.exceptions import get_error_context

try:
    raise ValueError("Erro de teste")
except Exception as e:
    contexto = get_error_context(e)
    print(contexto['error_type'])     # ValueError
    print(contexto['error_message'])  # Erro de teste
    print(contexto['traceback'])      # Stack trace completo
```

## 🔄 Integração Gradual

### Opção 1: Usar em Paralelo
```python
def minha_funcao():
    try:
        # ... código ...
        pass
    except FileNotFoundError as e:
        # Sistema original (mantido)
        logger.error(f"Erro: {e}")
        
        # Sistema novo (adição)
        enhanced = ErrorHandler.handle_file_error(e, "arquivo.xlsx", "operacao")
        print(f"Contexto: {enhanced.details}")
```

### Opção 2: Wrapper (Sem Modificar Código Existente)
```python
def funcao_existente():
    """Função que já existe - NÃO MODIFICAR"""
    # ... código original ...
    raise FileNotFoundError("Erro original")

def funcao_existente_melhorada():
    """Wrapper que adiciona tratamento melhorado"""
    try:
        funcao_existente()  # Chama original
    except FileNotFoundError as e:
        enhanced = ErrorHandler.handle_file_error(e, "arquivo", "operacao")
        # Agora temos contexto estruturado
        raise enhanced from e
```

### Opção 3: Migração com wrap_existing_exception()
```python
from utils.exceptions import wrap_existing_exception

try:
    # Código original que pode falhar
    raise ValueError("Erro original")
except ValueError as e:
    # Envolve exceção existente com contexto
    enhanced = wrap_existing_exception(
        e,
        operation="operacao_original",
        details={"contexto": "migração"}
    )
    # Agora temos logging estruturado automático
```

## 📊 Benefícios do Sistema Centralizado

1. **Contexto Estruturado**: Cada erro tem informações detalhadas
2. **Logging Automático**: Integração com sistema de logging estruturado
3. **Debugging Avançado**: Stack traces e contexto para análise
4. **Tratamento Consistente**: Padrões uniformes em todo o sistema
5. **Compatibilidade Total**: Sistema original preservado 100%

## ⚠️ Regras de Uso

1. **NUNCA** remover ou modificar try/except existentes
2. **SEMPRE** usar o sistema centralizado como ADIÇÃO
3. **TESTAR** cada implementação antes de usar em produção
4. **MANTER** backward compatibility em todas as mudanças

## 🎯 Exemplos Práticos

### Migrar Código de Arquivo
```python
# ANTES (mantido funcionando)
try:
    with open("planilha.xlsx") as f:
        data = f.read()
except FileNotFoundError as e:
    logger.error(f"Arquivo não encontrado: {e}")
    raise

# DEPOIS (adição)
try:
    with open("planilha.xlsx") as f:
        data = f.read()
except FileNotFoundError as e:
    # Sistema original (mantido)
    logger.error(f"Arquivo não encontrado: {e}")
    
    # Sistema novo (adição)
    enhanced = FileOperationError(
        "Planilha não encontrada",
        file_path="planilha.xlsx",
        operation="carregar_planilha"
    )
    raise enhanced from e
```

### Migrar Validação de Dados
```python
# ANTES (mantido funcionando)
try:
    valor = float(entrada_usuario)
except ValueError as e:
    logger.error(f"Valor inválido: {e}")
    raise

# DEPOIS (adição)
try:
    valor = float(entrada_usuario)
except ValueError as e:
    # Sistema original (mantido)
    logger.error(f"Valor inválido: {e}")
    
    # Sistema novo (adição)
    enhanced = DataValidationError(
        "Valor deve ser numérico",
        field_name="entrada_usuario",
        invalid_value=entrada_usuario,
        operation="validar_entrada"
    )
    raise enhanced from e
```

---

**Status**: ✅ IMPLEMENTADO E TESTADO
**Compatibilidade**: ✅ 100% MANTIDA
**Sistema Original**: ✅ FUNCIONANDO PERFEITAMENTE
**Próximo**: Sistema de Validação de Entrada Robusta
