# Changelog - OceanicDesk

## [1.4.6] - 2024-12-19

### Adicionado
- **Documentação Completa**: Criada documentação específica para sistema de alertas visuais
- **Testes Avançados**: Implementados testes separados para simular bugs e cenários específicos
- **Janela Oculta**: Janela principal agora fica oculta para não interferir com interface
- **README Atualizado**: Documentação principal atualizada com informações sobre alertas
- **Teste de Bug**: Teste específico para simular bug de sobreposição visual

### Melhorado
- **Testes**: Sistema de testes mais robusto e organizado
- **Documentação**: Documentação técnica detalhada e acessível
- **UX**: Interface mais limpa sem janelas desnecessárias
- **Manutenibilidade**: Melhor estrutura de testes e documentação

## [1.4.5] - 2024-12-19

### Corrigido
- **Sistema de Alertas**: Corrigido problema de múltiplos alertas simultâneos no início da aplicação
- **Posicionamento**: Alertas movidos para canto inferior direito para evitar conflitos com pyautogui
- **Threads**: Otimizado sistema de threads para reduzir exceções e melhorar performance
- **Performance**: Reduzido número de alertas excessivos durante execução das etapas
- **Delays**: Adicionado delays entre etapas para melhor experiência do usuário
- **Controle**: Implementado sistema de controle de alertas simultâneos com lock thread-safe

### Melhorado
- **UX**: Alertas mais rápidos e menos intrusivos
- **Estabilidade**: Sistema mais estável durante execução de automações
- **Compatibilidade**: Melhor compatibilidade com pyautogui e automações

## [1.4.4] - 2024-12-19
### Adicionado
- Sistema de alertas visuais moderno e abrangente em todo o projeto
- Alertas detalhados para todas as etapas, funções e operações do sistema
- Controle de posicionamento automático para múltiplos alertas simultâneos
- Alertas de progresso com barra de progresso para operações longas
- Tipos de alerta: success, error, info, dev, warning, progress
- Alertas específicos para logs técnicos (tipo 'dev') e informações para usuário final
- Sistema de alertas não intrusivo com fade in/out e opacidade reduzida

### Melhorado
- Transparência total do sistema com alertas para cada ação, por menor que seja
- Alertas visuais em todas as etapas do processo (1-8)
- Alertas detalhados em operações de Excel, automação, OCR e relatórios
- Alertas de validação e verificação de arquivos e configurações
- Alertas de progresso em loops e operações repetitivas
- Alertas de erro com informações detalhadas para troubleshooting
- Alertas de sucesso com confirmação de conclusão de tarefas

### Alterado
- Módulo `utils/alerta_visual.py` completamente reformulado com novas funcionalidades
- Todas as funções principais agora incluem alertas visuais detalhados
- Sistema de logging integrado com alertas visuais para eventos importantes
- Interface mais informativa e transparente para o usuário
- Melhor experiência de usuário com feedback visual constante

### Corrigido
- Alertas visuais agora seguem padrão consistente em todo o projeto
- Tipos de alerta padronizados (dev apenas para logs técnicos)
- Posicionamento automático evita sobreposição de alertas
- Controle de múltiplos alertas simultâneos

## [1.4.3] - 2024-12-19
### Segurança
- Removidos dados sensíveis hardcoded (usuários e senhas) do código
- Adicionadas variáveis de ambiente para autenticação de usuários (USUARIO_NILTON, SENHA_NILTON, USUARIO_ELIANE, SENHA_ELIANE)
- Aprimorada segurança exigindo que todas as credenciais sejam armazenadas no arquivo .env
- Adicionadas mensagens de erro amigáveis quando variáveis de ambiente obrigatórias estão ausentes

### Alterado
- Atualizada documentação para refletir novas práticas de segurança
- Aprimorado tratamento de erros para credenciais de autenticação ausentes

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

