# Sistema de Validação de Entrada Robusta - OceanicDesk

## ✅ COMPATIBILIDADE TOTAL GARANTIDA

**IMPORTANTE**: O sistema original continua funcionando 100% igual. Nada foi quebrado ou modificado.

## 📋 Resumo da Implementação

### Sistema Original (Mantido)
- ✅ `float()`, `int()` - Funcionam exatamente igual
- ✅ `os.path.exists()` - Funciona exatamente igual  
- ✅ Validações manuais com `try/except` - Funcionam exatamente igual
- ✅ `messagebox.showerror()` - Funciona exatamente igual
- ✅ Conversões de string para número - Funcionam exatamente igual

### Sistema de Validação (Adicionado)
- 🆕 **Validadores Robustos** - Validação estruturada com contexto detalhado
- 🆕 **Conversões Seguras** - Funções com fallback automático
- 🆕 **Validações Específicas** - Para domínio do posto de combustível
- 🆕 **Validação em Lote** - Para múltiplos campos simultaneamente
- 🆕 **Decorators** - Validação automática sem modificar código

## 🚀 Validadores Disponíveis

### 1. **NumericValidator**
Validação robusta de valores numéricos
```python
from utils.validators import NumericValidator

validator = NumericValidator(
    field_name="litros_combustivel",
    min_value=0.0,
    max_value=50000.0,
    allow_negative=False,
    decimal_places=2
)

# Aceita vários formatos
resultado1 = validator.validate("123,45")    # Formato brasileiro
resultado2 = validator.validate(123.45)      # Número direto
resultado3 = validator.validate("123.456")   # Será arredondado para 123.46
```

### 2. **FilePathValidator**
Validação robusta de caminhos de arquivo
```python
from utils.validators import FilePathValidator

validator = FilePathValidator(
    field_name="planilha_excel",
    must_exist=True,
    allowed_extensions=[".xlsx", ".xls"],
    create_if_missing=False
)

path = validator.validate("C:/Planilhas/vendas.xlsx")
```

### 3. **CombustivelValidator**
Validação específica para dados de combustível
```python
from utils.validators import CombustivelValidator

validator = CombustivelValidator("combustivel_data")

# Validação de tipo
tipo = validator.validate_tipo("etanol")  # Aceita: etanol, diesel, comum, aditivada

# Validação de litros
litros = validator.validate_litros("1500.50")  # Min: 0, Max: 50000

# Validação de preço
preco = validator.validate_preco("5.789")  # Min: 0.01, Max: 20.0
```

### 4. **ConfigValidator**
Validação de configurações do sistema
```python
from utils.validators import ConfigValidator

validator = ConfigValidator("config_sistema")

# Validação de variável de ambiente
caminho = validator.validate_env_var("CAMINHO_PLANILHA", required=True)

# Validação de caminho de planilha
planilha = validator.validate_planilha_path("C:/Planilhas/vendas.xlsx")
```

### 5. **OceanicDeskValidator**
Validações específicas do domínio do posto
```python
from utils.validators import OceanicDeskValidator

# Validação de usuário do sistema
usuario = OceanicDeskValidator.validate_usuario_sistema("admin")

# Validação de data para relatórios
data = OceanicDeskValidator.validate_data_relatorio("2025-07-25")

# Validação de valor monetário
valor = OceanicDeskValidator.validate_valor_monetario("1234,56")

# Validação de percentual (0-100)
percentual = OceanicDeskValidator.validate_percentual("15.5")
```

## 🛡️ Funções de Conveniência

### Conversões Seguras com Fallback
```python
from utils.validators import safe_float, safe_int

# Conversão segura para float
valor1 = safe_float("123,45", default=0.0)        # 123.45
valor2 = safe_float("texto_inválido", default=0.0) # 0.0

# Conversão segura para int
numero1 = safe_int("123.99", default=0)            # 123
numero2 = safe_int("texto_inválido", default=0)    # 0
```

### Validações Específicas
```python
from utils.validators import (
    validate_file_exists,
    validate_excel_file,
    validate_combustivel_data
)

# Validação de existência de arquivo
path = validate_file_exists("C:/arquivo.txt")

# Validação específica para Excel
excel_path = validate_excel_file("C:/planilha.xlsx")

# Validação completa de dados de combustível
dados = {
    "etanol": "1500.50",
    "diesel": "2000.75",
    "comum": "1800.25"
}
dados_validados = validate_combustivel_data(dados)
```

## 🎯 Decorators para Validação Automática

### @validate_numeric_input
Validação automática de entrada numérica
```python
from utils.validators import validate_numeric_input

@validate_numeric_input("valor_entrada", min_value=0.0, decimal_places=2)
def processar_valor(valor):
    # Valor já validado e convertido automaticamente
    return f"Valor processado: {valor}"

resultado = processar_valor("123,456")  # Será validado e arredondado
```

### @validate_file_input
Validação automática de entrada de arquivo
```python
from utils.validators import validate_file_input

@validate_file_input("arquivo_entrada", must_exist=True, allowed_extensions=[".xlsx"])
def processar_planilha(caminho):
    # Caminho já validado automaticamente
    return f"Planilha processada: {caminho}"

resultado = processar_planilha("vendas.xlsx")
```

## 📊 Sistema de Validação em Lote

### BatchValidator
Validação de múltiplos campos simultaneamente
```python
from utils.validators import BatchValidator

# Configura validador em lote
batch = BatchValidator()

# Adiciona validadores para diferentes campos
batch.add_numeric_validator("etanol", min_value=0.0, decimal_places=2)
batch.add_numeric_validator("diesel", min_value=0.0, decimal_places=2)
batch.add_file_validator("planilha", must_exist=True, allowed_extensions=[".xlsx"])

# Dados para validar
dados = {
    "etanol": "1500.50",
    "diesel": "2000.75",
    "planilha": "vendas.xlsx"
}

# Executa validação
if batch.validate_all(dados):
    print("✅ Todos os campos válidos!")
    dados_validados = batch.get_validated_data()
else:
    print("❌ Erros encontrados:")
    print(batch.get_error_summary())
```

## 🔄 Integração Gradual

### Opção 1: Usar em Paralelo
```python
def minha_funcao(valor_str):
    try:
        # Sistema original (mantido)
        valor_original = float(valor_str.replace(",", "."))
        
        # Sistema novo (adição)
        valor_validado = safe_float(valor_str, default=0.0)
        
        # Usar o que preferir
        return valor_validado
    except ValueError as e:
        logger.error(f"Erro: {e}")
        return 0.0
```

### Opção 2: Wrapper (Sem Modificar Código Existente)
```python
from utils.validators import enhance_existing_validation, NumericValidator

def funcao_existente(valor):
    """Função que já existe - NÃO MODIFICAR"""
    return float(valor.replace(",", "."))

# Cria versão melhorada sem modificar a original
validator = NumericValidator("valor", min_value=0.0, decimal_places=2)
funcao_melhorada = enhance_existing_validation(funcao_existente, validator)

# Agora tem validação robusta
resultado = funcao_melhorada("123,456")  # Validado e arredondado
```

### Opção 3: Decorator Wrapper
```python
from utils.validators import create_validation_wrapper

# Aplica validação a função existente
@create_validation_wrapper("valor_entrada", "numeric", min_value=0.0)
def processar_valor_existente(valor):
    """Função existente com validação adicionada"""
    return float(valor.replace(",", "."))
```

## 📈 Benefícios do Sistema de Validação

1. **Validação Robusta**: Aceita múltiplos formatos de entrada
2. **Fallback Automático**: Valores padrão em caso de erro
3. **Contexto Estruturado**: Erros detalhados para debugging
4. **Validações Específicas**: Para domínio do posto de combustível
5. **Compatibilidade Total**: Sistema original preservado 100%

## ⚠️ Regras de Uso

1. **NUNCA** remover ou modificar validações existentes
2. **SEMPRE** usar o sistema de validação como ADIÇÃO
3. **TESTAR** cada implementação antes de usar em produção
4. **MANTER** backward compatibility em todas as mudanças

## 🎯 Exemplos Práticos

### Migrar Validação de Litros
```python
# ANTES (mantido funcionando)
def validar_litros_original(valor):
    try:
        litros = float(valor.replace(",", "."))
        if litros < 0:
            raise ValueError("Litros não pode ser negativo")
        return litros
    except ValueError as e:
        logger.error(f"Erro: {e}")
        raise

# DEPOIS (adição)
from utils.validators import NumericValidator

validator = NumericValidator(
    field_name="litros_combustivel",
    min_value=0.0,
    max_value=50000.0,
    decimal_places=2
)

def validar_litros_melhorado(valor):
    # Sistema original (mantido)
    try:
        return validar_litros_original(valor)
    except ValueError:
        # Sistema novo (fallback)
        return validator.validate(valor)
```

### Migrar Validação de Arquivo
```python
# ANTES (mantido funcionando)
def verificar_planilha_original(caminho):
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Planilha não encontrada: {caminho}")
    if not caminho.endswith(('.xlsx', '.xls')):
        raise ValueError("Arquivo deve ser Excel")
    return caminho

# DEPOIS (adição)
from utils.validators import validate_excel_file

def verificar_planilha_melhorado(caminho):
    # Sistema original (mantido)
    try:
        return verificar_planilha_original(caminho)
    except (FileNotFoundError, ValueError):
        # Sistema novo (fallback)
        return validate_excel_file(caminho)
```

### Migrar Entrada de Usuário
```python
# ANTES (mantido funcionando)
def coletar_dados_original():
    try:
        etanol = float(input("Etanol: ").replace(",", "."))
        diesel = float(input("Diesel: ").replace(",", "."))
        return {"etanol": etanol, "diesel": diesel}
    except ValueError:
        messagebox.showerror("Erro", "Valores inválidos")
        return None

# DEPOIS (adição)
from utils.validators import BatchValidator

def coletar_dados_melhorado():
    # Coleta dados (mantido)
    dados_brutos = {
        "etanol": input("Etanol: "),
        "diesel": input("Diesel: ")
    }
    
    # Validação robusta (adição)
    batch = BatchValidator()
    batch.add_numeric_validator("etanol", min_value=0.0, decimal_places=2)
    batch.add_numeric_validator("diesel", min_value=0.0, decimal_places=2)
    
    if batch.validate_all(dados_brutos):
        return batch.get_validated_data()
    else:
        messagebox.showerror("Erro", batch.get_error_summary())
        return None
```

---

**Status**: ✅ IMPLEMENTADO E TESTADO
**Compatibilidade**: ✅ 100% MANTIDA
**Sistema Original**: ✅ FUNCIONANDO PERFEITAMENTE
**Próximo**: Sistema de Cache para Operações Excel
