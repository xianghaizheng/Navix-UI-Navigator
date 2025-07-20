"""
Navix Demo 15 - Framework Auto-Detect Example
=====================================
Demonstrates automatic GUI framework detection and switching in Navix.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

#======================================================================#
from Navix.builders import Navix_app
from enum import Enum
from PySide6 import QtWidgets
from Navix import navigate

voyager = None
class AutoRoutes(Enum):
    MAIN = "auto.main"

@navigate(AutoRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Auto Main Window")

def startup_hook(app):
    print("Detected framework:", getattr(voyager, "gui_framework", "Unknown"))

def main():
    global voyager
    voyager = None
    from Navix import UIVoyager
    voyager = UIVoyager()
    app_builder = (
        Navix_app("Auto Detect Demo")
        .auto_detect_framework()
        .routes(AutoRoutes)
        .main_window(AutoRoutes.MAIN)
        .startup_hook(startup_hook)
        .build()
    )
    app_builder.voyager = voyager
    app_builder.run()

if __name__ == "__main__":
    main()
