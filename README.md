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

## Advanced Features Example

```python
from Navix import container_manager, container_property, route_validator, UIVoyager, navigate
...

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

## Builder API Example

```python
from Navix.builders import Navix_app
...
class BuilderRoutes(Enum):
    MAIN = "builder.main"
    SETTINGS = "builder.settings"

@navigate(BuilderRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    ...
@navigate(BuilderRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    ...
def startup_hook(app): ...
def shutdown_hook(app):...

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
    ...
    .build()
)
app.run()
```

## Documentation
- [Demo Examples](demo/)
- [Full Documentation (HTML, open in browser)](docs/navix_full_documentation.html)

## License

MIT License © 2024 Xiang Haizheng
