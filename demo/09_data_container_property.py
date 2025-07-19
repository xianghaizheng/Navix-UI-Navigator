"""
Navix Demo 09 - Data Container Property
Demonstrates: Declaring type-safe container properties for IDE completion and documentation.
Shows how to use @container_property for structured, documented, and type-hinted data sharing.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

from enum import Enum
from Navix import container_manager, container_property, navigate, setup_navigator
from PySide6 import QtWidgets

class PropertyRoutes(Enum):
    SETTINGS = "property.settings"

@navigate(PropertyRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    @container_property(str, "light", "Theme setting")
    def theme(self): pass

    @container_property(int, 0, "Admin level")
    def admin_level(self): pass

    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Settings Dialog")
        self.resize(240, 120)
        # Show current theme and admin level from container
        container = container_manager(PropertyRoutes.SETTINGS)
        theme = container.get("theme")
        admin_level = container.get("admin_level")
        label = QtWidgets.QLabel(f"Theme: {theme}\nAdmin Level: {admin_level}", self)
        label.move(40, 40)

def main():
    setup_navigator(PropertyRoutes)
    app = QtWidgets.QApplication([])
    # Set type-safe container properties
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
