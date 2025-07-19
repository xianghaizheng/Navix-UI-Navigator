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
- **Designed for professional teams and enterprise applications.**

## Quick Start  
_Basic usage: minimal navigation setup._

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

## Advanced Features Example  
_Type-safe data container and validation usage._

```python
from Navix import container_manager, container_property, route_validator, UIVoyager, navigate
from enum import Enum
from PySide6 import QtWidgets

class DataRoutes(Enum):
    SETTINGS = "data.settings"

@navigate(DataRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    @container_property(str, "light", "Theme setting")
    def theme(self): pass

# Add route validation and security
voyager = UIVoyager()
voyager.add_route_pattern(r'^data\.[a-z_]+$')
voyager.add_parameter_rule('theme', lambda x: x in ('light', 'dark'))

# Use data container for cross-UI sharing
container = container_manager(DataRoutes.SETTINGS)
container.set("theme", "dark")
theme = container.get("theme")
```

## Data Container Property Example  
_Declare type-safe container properties for IDE completion and documentation._

```python
from Navix import container_manager, container_property, navigate, setup_navigator
from enum import Enum
from PySide6 import QtWidgets

class PropertyRoutes(Enum):
    SETTINGS = "property.settings"

@navigate(PropertyRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    @container_property(str, "light", "Theme setting")
    def theme(self): pass

    @container_property(int, 0, "Admin level")
    def admin_level(self): pass

def main():
    setup_navigator(PropertyRoutes)
    app = QtWidgets.QApplication([])
    container = container_manager(PropertyRoutes.SETTINGS)
    container.set("theme", "dark")
    container.set("admin_level", 5)
    print(container.get("theme"))         # IDE type hint: str
    print(container.get("admin_level"))   # IDE type hint: int
    win = SettingsDialog()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
```

## Builder API Example  
_Enterprise builder API usage for team configuration and governance._

```python
from Navix.builders import Navix_app
from enum import Enum
from PySide6 import QtWidgets

class BuilderRoutes(Enum):
    MAIN = "builder.main"
    SETTINGS = "builder.settings"

@navigate(BuilderRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Builder Main Window")

@navigate(BuilderRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings Dialog")

def startup_hook(app):
    print("[Startup Hook] Application is starting...")

def shutdown_hook(app):
    print("[Shutdown Hook] Application is shutting down...")

app = (
    Navix_app("Navix Builder Demo")
    .config(theme="light")
    .startup_hook(startup_hook)
    .shutdown_hook(shutdown_hook)
    .framework("PySide6")
    .routes(BuilderRoutes)
    .main_window(BuilderRoutes.MAIN)
    .import_ui_modules(__name__)
    .validation()
        .patterns(r'^builder\.[a-z_]+$')
        .parameters("theme", lambda x: x in ("light", "dark"))
        .security_checker(lambda route, params, param_names: True)
        .end()
    .interceptors()
        .logging()
        .performance()
        .end()
    .containers()
        .global_data({"theme": "light"})
        .end()
    .navigation()
        .max_history(50)
        .end()
    .build()
)
app.run()
```

## Documentation
- [Demo Examples](demo/)
- [Full Documentation (HTML, open in browser)](docs/navix_full_documentation.html)

## License

MIT License © 2024 Xiang Haizheng
