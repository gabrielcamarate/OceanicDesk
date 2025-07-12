# Changelog

## [1.4.3] - 2024-12-19
### Security
- Removed hardcoded sensitive data (usernames and passwords) from the codebase
- Added environment variables for user authentication (USUARIO_NILTON, SENHA_NILTON, USUARIO_ELIANE, SENHA_ELIANE)
- Enhanced security by requiring all credentials to be stored in .env file
- Added friendly error messages when required environment variables are missing

### Changed
- Updated documentation to reflect new security practices
- Improved error handling for missing authentication credentials

## [1.4.2] - 2024-12-19
### Added
- Added "OceanicDesk" branding to all window titles
- Added icon support for all secondary windows (entrada_dados, metodos_pagamento, valores_fechamento)
- Added comprehensive icon loading function to all interface modules

### Changed
- Updated main window title to "OceanicDesk - Painel de Controle - Relatórios Oceanico"
- Updated secondary window titles to include "OceanicDesk" prefix
- Enhanced icon loading with multiple fallback paths for all windows

### Fixed
- Fixed missing icons in secondary windows
- Fixed window title consistency across all interfaces

## [1.4.1] - 2025-07-12
### Fixed
- Removed all hardcoded paths from the codebase for better portability.
- Fixed .env file loading when compiled to .exe using PyInstaller.
- Fixed image capture paths not being found in compiled version.
- Fixed system program paths (AutoSystem, EMSys3, Tesseract) for different installations.

### Added
- Dynamic path resolution system (`utils/path_utils.py`) for development and compiled environments.
- Robust icon loading for the application window with multiple fallbacks.
- Automatic inclusion of required folders (planilhas, capturas_ocr_pyautogui) in the build.
- Comprehensive build testing script (`test_build.py`) to verify all components.
- Enhanced build automation with proper file copying and version naming.

### Changed
- Updated build configuration to include all necessary resources.
- Improved error handling and logging for path resolution.
- Enhanced documentation with troubleshooting guides.

## [1.4.0] - 2025-07-11
### Added
- Elegant checking of required environment variables (.env) throughout the project.
- Friendly errors if sensitive variables are missing.
- Robustness in the use of file paths and credentials.
- Possibility to configure Tesseract path via TESSERACT_CMD.
- Robustness documentation in README.

## [1.0.3] - 2025-07-11
### Fixed
- Robust conversion of file paths to Path in all critical project functions.
- Prevented errors when handling files received as strings.

## [1.0.2] - 2025-07-10
### Changed
- New app name: OceanicDesk.
- Exclusive use of favicon.ico as the app icon (taskbar and window).
- Automatic reading of the version from the VERSION file in the About screen.
- Automatic cleanup of temporary files after build.

## [1.0.1] - 2025-07-09
### Added
- Added "About" button with app information.
- Generated README_USUARIO.txt for end-user instructions.
- Build adjustments for .zip distribution.

