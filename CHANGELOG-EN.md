# Changelog - OceanicDesk

## [1.4.9] - 2025-07-17

### Refactor
- Adjustments and refactoring in etapas.py for standardization and robustness

## [1.4.5] - 2024-12-19

### Fixed
- **Alert System**: Fixed issue with multiple simultaneous alerts at application startup
- **Positioning**: Alerts moved to bottom-right corner to avoid conflicts with pyautogui
- **Threads**: Optimized thread system to reduce exceptions and improve performance
- **Performance**: Reduced excessive alerts during stage execution
- **Delays**: Added delays between stages for better user experience
- **Control**: Implemented simultaneous alert control system with thread-safe lock

### Improved
- **UX**: Faster and less intrusive alerts
- **Stability**: More stable system during automation execution
- **Compatibility**: Better compatibility with pyautogui and automations

## [1.4.4] - 2024-12-19
### Added
- Modern and comprehensive visual alert system throughout the project
- Detailed alerts for all stages, functions and system operations
- Automatic positioning control for multiple simultaneous alerts
- Progress alerts with progress bar for long operations
- Alert types: success, error, info, dev, warning, progress
- Specific alerts for technical logs (type 'dev') and end-user information
- Non-intrusive alert system with fade in/out and reduced opacity

### Improved
- Total system transparency with alerts for every action, no matter how small
- Visual alerts in all process stages (1-8)
- Detailed alerts in Excel operations, automation, OCR and reports
- Validation and file verification alerts
- Progress alerts in loops and repetitive operations
- Error alerts with detailed information for troubleshooting
- Success alerts with task completion confirmation

### Changed
- `utils/alerta_visual.py` module completely redesigned with new features
- All main functions now include detailed visual alerts
- Logging system integrated with visual alerts for important events
- More informative and transparent interface for users
- Better user experience with constant visual feedback

### Fixed
- Visual alerts now follow consistent pattern throughout the project
- Standardized alert types (dev only for technical logs)
- Automatic positioning prevents alert overlap
- Control of multiple simultaneous alerts

## [1.4.3] - 2024-12-19
### Security
- Removed hardcoded sensitive data (users and passwords) from code
- Added environment variables for user authentication (USUARIO_NILTON, SENHA_NILTON, USUARIO_ELIANE, SENHA_ELIANE)
- Enhanced security requiring all credentials to be stored in .env file
- Added user-friendly error messages when required environment variables are missing

### Changed
- Updated documentation to reflect new security practices
- Enhanced error handling for missing authentication credentials

## [1.4.2] - 2024-12-19
### Added
- Added "OceanicDesk" branding to all window titles
- Added icon support for all secondary windows (entrada_dados, metodos_pagamento, valores_fechamento)
- Added comprehensive icon loading function for all interface modules

### Changed
- Updated main window title to "OceanicDesk - Painel de Controle - Relatórios Oceanico"
- Updated secondary window titles to include "OceanicDesk" prefix
- Enhanced icon loading with multiple fallback paths for all windows

### Fixed
- Fixed missing icons in secondary windows
- Fixed window title consistency across all interfaces

## [1.4.1] - 2025-07-12
### Fixed
- Removed all hardcoded paths from code for better portability.
- Fixed .env file loading when compiled to .exe using PyInstaller.
- Fixed image capture paths not being found in compiled version.
- Fixed system program paths (AutoSystem, EMSys3, Tesseract) for different installations.

### Added
- Dynamic path resolution system (`utils/path_utils.py`) for development and compiled environments.
- Robust application window icon loading with multiple fallbacks.
- Automatic inclusion of necessary folders (planilhas, capturas_ocr_pyautogui) in build.
- Comprehensive build test script (`test_build.py`) to verify all components.
- Enhanced build automation with proper file copying and version naming.

### Changed
- Updated build configuration to include all necessary resources.
- Enhanced error handling and logging for path resolution.
- Enhanced documentation with troubleshooting guides.

## [1.4.0] - 2025-07-11
### Added
- Elegant checking of required environment variables (.env) throughout the project.
- User-friendly errors if sensitive variables are missing.
- Robustness in use of file paths and credentials.
- Possibility to configure Tesseract path via TESSERACT_CMD.
- Robustness documentation in README.

## [1.0.3] - 2025-07-11
### Fixed
- Robust conversion of file paths to Path in all critical project functions.
- Prevention of errors when handling files received as string.

## [1.0.2] - 2025-07-10
### Changed
- New app name: OceanicDesk.
- Exclusive use of favicon.ico as app icon (taskbar and window).
- Automatic version reading from VERSION file in About screen.
- Automatic cleanup of temporary files after build.

## [1.0.1] - 2025-07-09
### Implemented
- Added "About" button with app information.
- Generation of README_USUARIO.txt for end-user instructions.
- Build adjustments for .zip distribution.

## [1.4.8] - 2025-07-13

### Refactoring and Improvements
- Adjustments and refactoring in process steps (`utils/etapas.py`)
- Refactoring and improvements in Excel operations (`utils/excel_ops.py`)
- Adjustments in sales projection function (`projecao/vendas.py`)
- Update of dependencies in `requirements.txt`
- Removal of obsolete file `how c90495a --name-only`

---

