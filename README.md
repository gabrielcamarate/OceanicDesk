# OceanicDesk

A modern automation system for gas station management with advanced visual feedback and real-time progress tracking.

## 🚀 Features

### ✨ Visual Alert System
- **Modern Dark Theme**: Elegant dark interface with smooth animations
- **Real-time Progress**: Dynamic progress bars that update in real-time
- **Smart Positioning**: Bottom-right corner with intelligent stacking
- **Thread-safe**: Handles multiple concurrent operations safely
- **No Overlap**: Prevents visual conflicts between alerts

### 🔧 Core Functionality
- **Excel Operations**: Advanced spreadsheet processing with COM automation
- **OCR Integration**: Tesseract-based text extraction from images
- **System Automation**: PyAutoGUI-powered system interactions
- **Financial Reports**: Automated financial data processing
- **Multi-user Support**: Configurable user credentials

### 📊 Reporting
- **Sales Reports**: Automated sales data extraction and processing
- **Fuel Reports**: Comprehensive fuel sales analysis
- **Food Reports**: Food service sales tracking
- **Financial Consolidation**: Automated financial data consolidation

## 🛠️ Installation

### Prerequisites
```bash
# Python 3.8+
python --version

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

### Configuration
1. Copy `config.example.py` to `config.py`
2. Configure your credentials and paths
3. Set up Tesseract path in config

## 🎯 Usage

### Basic Usage
```bash
# Run the application
python run.py

# Run tests
python tests/test_alerta_visual.py
python tests/test_progresso_dinamico.py
```

### Visual Alerts API
```python
from interfaces.alerta_visual import mostrar_alerta_visual, atualizar_progresso

# Show success alert
mostrar_alerta_visual("Success", "Operation completed!", tipo="success")

# Show dynamic progress
atualizar_progresso("Processing", "Step 2 of 5", 40)
```

## 📁 Project Structure

```
OceanicDesk/
├── interfaces/           # User interfaces and visual components
│   ├── alerta_visual.py  # Modern visual alert system
│   ├── janela_principal.py
│   └── ...
├── controllers/          # Application controllers
├── utils/               # Utility modules
├── tests/               # Test suite
├── docs/                # Documentation
└── config/              # Configuration files
```

## 🧪 Testing

### Visual Alert Tests
```bash
# Basic alert tests
python tests/test_alerta_visual.py

# Dynamic progress tests
python tests/test_progresso_dinamico.py

# Excel operations tests
python tests/test_excel_ops.py
```

### Test Coverage
- ✅ Visual alert system
- ✅ Dynamic progress tracking
- ✅ Thread safety
- ✅ Position management
- ✅ Overlap prevention
- ✅ Excel operations
- ✅ File operations

## 📚 Documentation

- [Visual Alerts Documentation](docs/ALERTAS_VISUAIS.md)
- [Build Instructions](BUILD-README.md)
- [Portuguese README](PT-BR-README.md)

## 🔄 Recent Updates

### v1.4.7 (Current)
- ✅ **Dynamic Progress System**: Real-time progress updates
- ✅ **Overlap Prevention**: Fixed visual alert conflicts
- ✅ **Modular Architecture**: Moved alerts to `interfaces/`
- ✅ **Advanced Testing**: Comprehensive test suite
- ✅ **Thread Safety**: Improved concurrent operation handling

### v1.4.6
- ✅ **Smart Positioning**: Bottom-right corner placement
- ✅ **Thread Management**: Safe concurrent operations
- ✅ **Performance Optimization**: Reduced resource usage

## 🐛 Bug Fixes

### Resolved Issues
- ✅ **Visual Overlap**: Multiple alerts no longer overlap
- ✅ **Thread Conflicts**: Safe concurrent alert display
- ✅ **Performance**: Optimized alert rendering
- ✅ **Positioning**: Consistent alert placement

## 🎨 Visual Alert Types

| Type | Color | Icon | Usage |
|------|-------|------|-------|
| Success | Green | ✔ | Completed operations |
| Error | Red | ⚠ | Critical failures |
| Info | Blue | ℹ | General information |
| Warning | Yellow | ⚠ | Important warnings |
| Dev | Purple | ⚙ | Technical logs |
| Progress | Cyan | ↻ | Ongoing operations |

## 🔧 Configuration

### Alert System Settings
```python
# Maximum concurrent alerts
max_alerts = 3

# Default position (bottom-right)
default_position = None

# Animation duration
fade_duration = 300

# Alert opacity
default_opacity = 0.92
```

## 📞 Support

For issues or questions:
1. Check the logs in `logs/`
2. Run the test suite
3. Consult the documentation
4. Report bugs with detailed scenarios

## 📄 License

This project is proprietary software developed for OceanicDesk.

---

**OceanicDesk v1.4.7** - *Advanced automation with modern visual feedback*
