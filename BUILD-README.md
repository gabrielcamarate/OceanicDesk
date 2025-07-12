# Guia de Build do OceanicDesk

## Problemas Identificados e Soluções

### 1. Problema do arquivo .env

O arquivo `.env` não é lido quando o aplicativo é compilado para `.exe` porque o PyInstaller não inclui automaticamente arquivos de configuração no executável.

### 2. Problema dos caminhos hardcoded

Arquivos como `utils/sistema.py` e `utils/duplicata_ocr.py` tinham caminhos hardcoded que não funcionavam quando compilados:

```python
# ❌ PROBLEMA: Caminhos hardcoded
esperar_elemento(r"C:\Users\Usuario\Desktop\Gabriel Camarate\Projeto_posto\capturas_ocr_pyautogui\autosystem_login.png", timeout=60)
caminho_app = r"c:\ProgramData\Microsoft\Windows\Start Menu\Programs\AutoSystem\AutoSystem - Gerencial.lnk"
os.startfile(r"c:\Rezende\EMSys3\EMSys3.exe")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### 3. Problema das pastas de recursos

As pastas `planilhas/` e `capturas_ocr_pyautogui/` não eram incluídas no build, causando erros quando o aplicativo tentava acessar esses arquivos.

### 4. Problema do ícone da interface

O ícone da janela não era carregado quando compilado para `.exe`, ficando com o ícone padrão do sistema (pena).

## Soluções Implementadas

### 1. Carregamento Inteligente do .env

O arquivo `config.py` foi modificado para procurar o `.env` em múltiplos locais:

1. **Na mesma pasta do executável** (quando compilado)
2. **Na pasta do script Python** (desenvolvimento)
3. **Na pasta pai do script**
4. **Na pasta atual de trabalho**

### 2. Sistema de Caminhos Dinâmicos

Criado o arquivo `utils/path_utils.py` com funções para resolver caminhos:

```python
# ✅ SOLUÇÃO: Caminho dinâmico
from utils.path_utils import get_captura_path
esperar_elemento(get_captura_path("autosystem_login.png"), timeout=60)
```

**Funções disponíveis:**
- `get_captura_path(filename)` - Para imagens de captura
- `get_planilha_path(filename)` - Para planilhas
- `get_image_path(filename)` - Para imagens gerais
- `get_system_path(program_name)` - Para programas do sistema (autosystem, emsys3, tesseract)
- `get_desktop_path()` - Para a área de trabalho do usuário
- `get_project_root()` - Raiz do projeto

### 3. Inclusão Automática no Build

O arquivo `OceanicDesk.spec` foi criado para incluir automaticamente:
- Arquivo `.env` na raiz do executável
- Pasta `images/` com ícones
- Pasta `config/` com configurações
- Pasta `planilhas/` com planilhas de trabalho
- Pasta `capturas_ocr_pyautogui/` com capturas de tela

### 4. Script de Build Automatizado

O arquivo `build.py` automatiza todo o processo de compilação.

### 5. Código Atualizado

Arquivos modificados para usar caminhos dinâmicos:
- `utils/sistema.py` - Todas as referências a capturas, programas do sistema e desktop
- `utils/duplicata_ocr.py` - Caminho da pasta de capturas e Tesseract
- `duplicata_ocr.py` - Caminho do Tesseract
- `interfaces/janela_principal.py` - Carregamento robusto do ícone da interface

### 6. Ícone da Interface Melhorado

- **Múltiplos fallbacks**: Procura o ícone em vários locais
- **Inclusão dupla**: Favicon incluído tanto na pasta `images/` quanto na raiz
- **ID do aplicativo**: Define um ID único para o Windows
- **Logs detalhados**: Mostra onde o ícone foi encontrado ou por que falhou

## Como Fazer o Build

### Opção 1: Usando o script automatizado (Recomendado)

```bash
python build.py
```

Este script irá:
- Limpar builds anteriores
- Verificar dependências
- Compilar o executável
- Copiar o `.env` para a pasta `dist/`
- Renomear o executável com a versão

### Opção 2: Usando PyInstaller diretamente

```bash
pyinstaller --onefile --windowed --icon=images/favicon.ico --name=OceanicDesk --add-data=.env;. --add-data=images;images --add-data=config;config --add-data=planilhas;planilhas --add-data=capturas_ocr_pyautogui;capturas_ocr_pyautogui run.py
```

### Opção 3: Usando o arquivo .spec

```bash
pyinstaller OceanicDesk.spec
```

## Estrutura do Executável

Após o build, você terá:

```
dist/
├── OceanicDesk_v1.4.1.exe  # Executável principal
├── .env                     # Arquivo de configuração
├── images/                  # Pasta com ícones
│   ├── favicon.ico         # Ícone do aplicativo
│   └── preview.png         # Imagem de preview
├── config/                  # Pasta com configurações
├── planilhas/              # Pasta com planilhas de trabalho
│   ├── Vendas Julho.xlsx
│   └── 07-VENDA CHACALTAYA LOJA JULHO 2025.xlsx
└── capturas_ocr_pyautogui/ # Pasta com capturas de tela para OCR
    ├── emsys_alert.png
    ├── emsys_login.png
    ├── autosystem_remove_alert.png
    └── autosystem_login.png
```

## Pastas Incluídas no Build

### 📁 **images/**
- **favicon.ico**: Ícone do aplicativo (usado no executável e janela)
- **preview.png**: Imagem de preview

### 📊 **planilhas/**
- **Vendas Julho.xlsx**: Planilha de vendas
- **07-VENDA CHACALTAYA LOJA JULHO 2025.xlsx**: Planilha específica do posto
- *Nota*: Estas são as planilhas onde os dados são inseridos durante a execução

### 🖼️ **capturas_ocr_pyautogui/**
- **emsys_alert.png**: Captura para alertas do EMSys
- **emsys_login.png**: Captura para tela de login do EMSys
- **autosystem_remove_alert.png**: Captura para remoção de alertas do AutoSystem
- **autosystem_login.png**: Captura para tela de login do AutoSystem
- *Nota*: Estas imagens são usadas pelo método `locate` do PyAutoGUI para automação

### ⚙️ **config/**
- Arquivos de configuração do sistema

## Ícone do Aplicativo

O aplicativo usa o `favicon.ico` da pasta `images/` como ícone:
- **No executável**: Definido via `--icon=images/favicon.ico`
- **Na janela**: Carregado dinamicamente da pasta `images/`
- **Fallback**: Se não encontrar na pasta `images/`, procura na raiz

## Verificação do .env

O aplicativo agora mostra no console onde o arquivo `.env` foi encontrado:

```
Arquivo .env encontrado em: C:\Users\Usuario\Desktop\OceanicDesk\.env
```

Se o `.env` não for encontrado, você verá:

```
Aviso: Arquivo .env não encontrado nos caminhos esperados:
  - C:\Users\Usuario\Desktop\OceanicDesk\.env
  - C:\Users\Usuario\Desktop\Gabriel Camarate\Projeto_posto\.env
  - ...
```

## Troubleshooting

### O .env ainda não é lido

1. **Verifique se o arquivo existe**: Certifique-se de que o `.env` está na mesma pasta do `.exe`
2. **Verifique o conteúdo**: Abra o `.env` e confirme que as variáveis estão corretas
3. **Execute com console**: Temporariamente mude `console=False` para `console=True` no `.spec` para ver mensagens de debug

### Erro ao carregar imagens de captura

1. **Verifique se as pastas existem**: Certifique-se de que `capturas_ocr_pyautogui/` está na mesma pasta do `.exe`
2. **Verifique os arquivos**: Confirme que os arquivos `.png` estão presentes
3. **Execute o teste**: Use `python test_build.py` para verificar se os caminhos estão corretos

### Erro ao acessar planilhas

1. **Verifique se a pasta existe**: Certifique-se de que `planilhas/` está na mesma pasta do `.exe`
2. **Verifique os arquivos**: Confirme que os arquivos `.xlsx` estão presentes
3. **Teste os caminhos**: Use `python test_build.py` para verificar se os caminhos estão corretos

### Erro de variáveis de ambiente

Se você receber erro sobre variáveis ausentes, verifique se o `.env` contém:

```env
CAMINHO_PLANILHA=C:\caminho\para\sua\planilha.xlsx
LOGIN_SISTEMA=seu_login
SENHA_SISTEMA=sua_senha
EMAIL_REMETENTE=seu_email@gmail.com
SENHA_EMAIL=sua_senha_email
```

### Build falha

1. **Instale o PyInstaller**: `pip install pyinstaller`
2. **Verifique dependências**: `pip install -r requirements.txt`
3. **Limpe builds anteriores**: Delete as pastas `build/` e `dist/`

## Notas Importantes

- O arquivo `.env` deve estar na mesma pasta do executável
- Nunca commite o `.env` no Git (já está no `.gitignore`)
- O executável será nomeado como `OceanicDesk_v{versao}.exe`
- O ícone será o `favicon.ico` da pasta `images/` 