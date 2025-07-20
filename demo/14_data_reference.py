"""
Navix Demo 14 - DataReference Cross-Container Example
=====================================
Demonstrates how to use DataReference for type-safe cross-container data sharing.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

#======================================================================#
from Navix import container_manager, container_property, DataReference, navigate, setup_navigator
from enum import Enum
from PySide6 import QtWidgets

class RefRoutes(Enum):
    MAIN = "ref.main"
    SETTINGS = "ref.settings"

@navigate(RefRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    @container_property(str, "light", "Theme setting")
    def theme(self): pass

@navigate(RefRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    @container_property(DataReference, None, "Reference to theme in settings")
    def theme_ref(self): pass

def main():
    setup_navigator(RefRoutes)
    app = QtWidgets.QApplication([])
    settings_container = container_manager(RefRoutes.SETTINGS)
    settings_container.set("theme", "dark")
    main_container = container_manager(RefRoutes.MAIN)
    # create a DataReference to the theme property in settings
    theme_ref = DataReference(RefRoutes.SETTINGS.value, "theme")
    main_container.set("theme_ref", theme_ref)
    # get data via reference
    ref_obj = main_container.get("theme_ref")
    print("Theme via reference:", ref_obj.get())
    win = MainWindow()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
