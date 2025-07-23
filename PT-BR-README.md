# ⛽ OceanicDesk - Automação de Relatórios Posto Oceanico

Sistema moderno e robusto de automação de rotinas administrativas para postos de combustível.

[🇺🇸 English Version](README.md) | [🇧🇷 Versão em Português](PT-BR-README.md)

![GitHub language count](https://img.shields.io/github/languages/count/gabrielcamarate/Projeto_posto?style=for-the-badge)

<br>

<p align="center">
  <!-- Adicione uma imagem de preview do projeto abaixo -->
  <img src="images/preview.png" alt="Demonstração do Projeto"/>
</p>

<br>

## 📋 Índice

* [Sobre](#-sobre)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Como Executar](#-como-executar)
* [Licença](#-licença)
* [Contato](#-contato)

<br>

## 📖 Sobre

A **Automação de Relatórios - Posto Oceanico** é uma aplicação desktop em Python para automatizar e otimizar tarefas administrativas e operacionais do dia a dia de um posto de combustível. Reduz o trabalho manual, minimiza erros e agiliza processos como geração de relatórios, manipulação de planilhas, backups, integração com sistemas de gestão (AutoSystem e EMSys3) e envio de e-mails.

**Funcionalidades principais:**
*   **Interface Gráfica Intuitiva (Tkinter):** Interface simples com botões dedicados e painel de logs.
*   **Automação com Sistemas Externos (pyautogui):** Simula teclado/mouse para interagir com AutoSystem e EMSys3.
*   **Manipulação Avançada de Excel (openpyxl, pandas):** Lê, escreve e processa arquivos Excel para dados financeiros e de vendas.
*   **Envio Automatizado de Relatórios:** Envia relatórios diários por e-mail para os responsáveis.
*   **Backup Automático de Planilhas:** Backups com data/hora para segurança dos dados.
*   **Modo Desenvolvedor:** Logs detalhados e roláveis para depuração.
*   **Logs Diários:** Todas as operações são registradas para auditoria.
*   **Testes Automatizados:** Testes unitários garantem confiabilidade.

<br>

## 💻 Tecnologias Utilizadas

- Python 3.10+
- Tkinter
- pandas
- openpyxl
- pyautogui
- pywin32
- python-dotenv

<br>

## 🚀 Como Executar

```bash
# Clone este repositório
$ git clone https://github.com/gabrielcamarate/Projeto_posto.git

# Acesse a pasta do projeto
$ cd Projeto_posto

# Instale as dependências
$ pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz com suas credenciais:

```dotenv
# Autenticação do sistema
LOGIN_SISTEMA=seu_usuario
SENHA_SISTEMA=sua_senha

# Configuração de email
EMAIL_REMETENTE=seu_email@dominio.com
SENHA_EMAIL=sua_senha_email
EMAIL_DESTINATARIO=destinatario@dominio.com

# Autenticação de usuários EMSys3
USUARIO_NILTON=NILTON.BARBOSA
SENHA_NILTON=sua_senha_nilton
USUARIO_ELIANE=ELIANE.MARIA
SENHA_ELIANE=sua_senha_eliane

# Opcional: Caminho do Tesseract OCR
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

Para rodar a aplicação:

```bash
python run.py
```

Para rodar os testes:

```bash
python -m unittest discover -s tests
```

> **Observação:** A automação depende da resolução da tela e posição das janelas. Os sistemas alvo devem estar visíveis e em primeiro plano. Funciona apenas no Windows.

<br>

## 📝 Licença

Este projeto é particular e de uso restrito. Distribuição, modificação ou uso comercial não são permitidos sem autorização expressa do autor.

<br>

## 📬 Contato

Feito com ❤️ por Gabriel Camarate. Entre em contato!

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabrielcamarate/)
[![Gmail](https://img.shields.io/badge/EMAIL-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:gabrielcamarate@icloud.com)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/gabrielcamarate) 

## 🛡️ Segurança e Boas Práticas

- O sistema exige que variáveis sensíveis (login, senha, caminhos de planilhas, email) estejam corretamente preenchidas no arquivo `.env`.
- Caso alguma variável obrigatória esteja ausente, o sistema exibirá um erro amigável e não permitirá a execução.
- Caminhos de arquivos são checados antes de uso para evitar falhas inesperadas.
- O caminho do Tesseract pode ser configurado via variável de ambiente `TESSERACT_CMD`.
- **IMPORTANTE:** Nunca faça commit do arquivo `.env` no controle de versão, pois ele contém informações sensíveis.
- Todas as credenciais de usuário agora são armazenadas como variáveis de ambiente para maior segurança. 

## 📝 Changelog

### v1.4.9
- Refatoração: ajustes e refatoração em etapas.py para padronização e robustez

### v1.4.8
- Refatoração e melhorias nas etapas do processo (`utils/etapas.py`)
- Refatoração e melhorias em operações de Excel (`utils/excel_ops.py`)
- Ajustes na função de projeção de vendas (`projecao/vendas.py`)
- Atualização de dependências em `requirements.txt`
- Remoção de arquivo obsoleto `how c90495a --name-only`

### v1.4.1
- Correções de tipagem e robustez em `sistema.py` e `helpers.py` (compatibilidade Pyright)
- Tratamento de erros aprimorado para Excel e variáveis de ambiente 
