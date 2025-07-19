# Navix UI Navigator
Modular, Type-Safe UI Routing & Navigation Framework for Python Desktop Applications.

## Features

- Enum-based routing for PyQt5/6, PySide2/6, wxPython, tkinter
- Centralized navigation manager (`UIVoyager`)
- **Type-safe, cross-UI data containers** (`container_manager`) for global and modular data sharing
- Validation & security (route/parameter/rbac)
- Fluent builder API for configuration
- Unified widget wrappers for major GUI frameworks
- Extensible via protocols, ABCs, custom interceptors
- Rich documentation and examples

## Data Container System (Highlight)

Navix's data container system enables safe, structured, and IDE-friendly data sharing across all UI components.

- **Auto-registration**: Each route gets a global container for data exchange.
- **Type-safe declaration**: Use `@container_property(type, default, desc)` for IDE completion and type checking.
- **Access**: `container_manager(route_enum_member)` or `container_manager.module.route.property` for safe access.
- **Features**: Module/global data, status monitoring, auto cleanup.


## Installation

```bash
pip install -r requirements.txt
# Or add Navix to your PYTHONPATH
```

## Quick Start
```python
from enum import Enum
from Navix import navigate, UIVoyager, setup_navigator
from PySide6 import QtWidgets

class CoreRoutes(Enum):
    MAIN = "core.main"

@navigate(CoreRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navix Main Window")

setup_navigator(CoreRoutes)
app     = QtWidgets.QApplication([])
voyager = UIVoyager()
win     = voyager.navigate_to(CoreRoutes.MAIN)
win.show()
app.exec()
```

## Documentation
- [Demo Examples](demo/)
- [Full Documentation (HTML)](doc/qmx_full_documentation.html)
  
MIT License © 2024 Xiang Haizheng
