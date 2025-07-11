# ⛽ OceanicDesk - Oceanic Gas Station Automation

Modern and robust automation system for administrative routines at a gas station.

[🇺🇸 English Version](README.md) | [🇧🇷 Versão em Português](PT-BR-README.md)

![GitHub language count](https://img.shields.io/github/languages/count/gabrielcamarate/Projeto_posto?style=for-the-badge)

<br>

<p align="center">
  <!-- Add your project preview image below -->
  <img src="images/preview.png" alt="Project Preview"/>
</p>

<br>

## 📋 Table of Contents

* [About](#-about)
* [Technologies Used](#-technologies-used)
* [How to Run](#-how-to-run)
* [License](#-license)
* [Contact](#-contact)

<br>

## 📖 About

**Oceanic Gas Station Automation** is a Python desktop application designed to automate and optimize daily administrative and operational tasks at a gas station. It reduces manual work, minimizes errors, and speeds up processes like report generation, spreadsheet handling, backups, integration with management systems (AutoSystem and EMSys3), and email communication.

**Key features:**
*   **Intuitive GUI (Tkinter):** Simple interface with dedicated buttons and log panel.
*   **Automation with External Systems (pyautogui):** Simulates keyboard/mouse to interact with AutoSystem and EMSys3.
*   **Advanced Excel Handling (openpyxl, pandas):** Reads, writes, and processes Excel files for financial and sales data.
*   **Automated Email Reports:** Sends daily reports to stakeholders.
*   **Automatic Spreadsheet Backup:** Timestamped backups for data safety.
*   **Developer Mode:** Detailed, scrollable logs for debugging.
*   **Daily Log Files:** All operations are logged for auditing.
*   **Automated Testing:** Unit tests ensure reliability.

<br>

## 💻 Technologies Used

- Python 3.10+
- Tkinter
- pandas
- openpyxl
- pyautogui
- pywin32
- python-dotenv

<br>

## 🛡️ Robustez e Boas Práticas

- O sistema exige que variáveis sensíveis (login, senha, caminhos de planilhas, email) estejam corretamente preenchidas no arquivo `.env`.
- Caso alguma variável obrigatória esteja ausente, o sistema exibirá um erro amigável e não permitirá a execução.
- Caminhos de arquivos são checados antes de uso para evitar falhas inesperadas.
- O caminho do Tesseract pode ser configurado via variável de ambiente `TESSERACT_CMD`.

## 🚀 How to Run

```bash
# Clone this repository
$ git clone https://github.com/gabrielcamarate/Projeto_posto.git

# Enter the project folder
$ cd Projeto_posto

# Install dependencies
$ pip install -r requirements.txt
```

Create a `.env` file in the root with your credentials:

```dotenv
LOGIN_SISTEMA=your_user
SENHA_SISTEMA=your_password
EMAIL_REMETENTE=your_email@domain.com
SENHA_EMAIL=your_email_password
EMAIL_DESTINATARIO=recipient@domain.com
```

To run the application:

```bash
python run.py
```

To run the tests:

```bash
python -m unittest discover -s tests
```

> **Note:** The automation depends on screen resolution and window positions. Target systems must be visible and in the foreground. Only works on Windows.

<br>

## 📝 License

This project is private and for restricted use. Distribution, modification, or commercial use is not permitted without explicit authorization from the author.

<br>

## 📬 Contact

Made with ❤️ by Gabriel Camarate. Get in touch!

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabrielcamarate/)
[![Gmail](https://img.shields.io/badge/EMAIL-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:gabrielcamarate@icloud.com)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/gabrielcamarate)
