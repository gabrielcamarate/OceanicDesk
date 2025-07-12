# Changelog

## [1.4.2] - 2024-12-19
### Adicionado
- Adicionada marca "OceanicDesk" em todos os títulos de janela
- Adicionado suporte a ícones para todas as janelas secundárias (entrada_dados, metodos_pagamento, valores_fechamento)
- Adicionada função abrangente de carregamento de ícones para todos os módulos de interface

### Alterado
- Atualizado título da janela principal para "OceanicDesk - Painel de Controle - Relatórios Oceanico"
- Atualizados títulos das janelas secundárias para incluir prefixo "OceanicDesk"
- Aprimorado carregamento de ícones com múltiplos caminhos de fallback para todas as janelas

### Corrigido
- Corrigidos ícones ausentes nas janelas secundárias
- Corrigida consistência dos títulos de janela em todas as interfaces

## [1.4.1] - 2025-07-12
### Corrigido
- Removidos todos os caminhos hardcoded do código para melhor portabilidade.
- Corrigido carregamento do arquivo .env quando compilado para .exe usando PyInstaller.
- Corrigido caminhos de capturas de imagem não sendo encontrados na versão compilada.
- Corrigido caminhos de programas do sistema (AutoSystem, EMSys3, Tesseract) para diferentes instalações.

### Adicionado
- Sistema de resolução dinâmica de caminhos (`utils/path_utils.py`) para ambientes de desenvolvimento e compilados.
- Carregamento robusto de ícone para a janela da aplicação com múltiplos fallbacks.
- Inclusão automática de pastas necessárias (planilhas, capturas_ocr_pyautogui) no build.
- Script abrangente de teste de build (`test_build.py`) para verificar todos os componentes.
- Automação de build aprimorada com cópia adequada de arquivos e nomenclatura de versão.

### Alterado
- Configuração de build atualizada para incluir todos os recursos necessários.
- Tratamento de erros e logging aprimorados para resolução de caminhos.
- Documentação aprimorada com guias de troubleshooting.

## [1.4.0] - 2025-07-11
### Adicionado
- Checagem elegante de variáveis de ambiente obrigatórias (.env) em todo o projeto.
- Erros amigáveis caso variáveis sensíveis estejam ausentes.
- Robustez no uso de caminhos de arquivos e credenciais.
- Possibilidade de configurar o caminho do Tesseract via TESSERACT_CMD.
- Documentação de robustez no README.

## [1.0.3] - 2025-07-11
### Corrigido
- Conversão robusta de caminhos de arquivos para Path em todas as funções críticas do projeto.
- Prevenção de erros ao manipular arquivos recebidos como string.

## [1.0.2] - 2025-07-10
### Alterado
- Novo nome do app: OceanicDesk.
- Uso exclusivo do favicon.ico como ícone do app (barra de tarefas e janela).
- Leitura automática da versão do arquivo VERSION na tela Sobre.
- Limpeza automática de arquivos temporários após o build.

## [1.0.1] - 2025-07-09
### Implementado
- Adição do botão "Sobre" com informações do app.
- Geração de README_USUARIO.txt para instruções do usuário final.
- Ajustes de build para distribuição em .zip.

