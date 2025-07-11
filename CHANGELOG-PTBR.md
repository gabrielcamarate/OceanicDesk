# Changelog

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
- Adição do botão “Sobre” com informações do app.
- Geração de README_USUARIO.txt para instruções do usuário final.
- Ajustes de build para distribuição em .zip. 
## [1.4.0] - 2025-07-11
### Adicionado
- Checagem elegante de vari�veis de ambiente obrigat�rias (.env) em todo o projeto.
- Erros amig�veis caso vari�veis sens�veis estejam ausentes.
- Robustez no uso de caminhos de arquivos e credenciais.
- Possibilidade de configurar o caminho do Tesseract via TESSERACT_CMD.
- Documenta��o de robustez no README.

