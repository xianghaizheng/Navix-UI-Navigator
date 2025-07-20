"""
Navix Demo 16 - Navigation History & Back Example
=====================================
Demonstrates navigation history tracking and back navigation in UIVoyager.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

#======================================================================#
from Navix import UIVoyager, navigate, setup_navigator
from enum import Enum
from PySide6 import QtWidgets

class HistRoutes(Enum):
    MAIN = "hist.main"
    PAGE1 = "hist.page1"
    PAGE2 = "hist.page2"

@navigate(HistRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    pass

@navigate(HistRoutes.PAGE1)
class Page1(QtWidgets.QWidget):
    pass

@navigate(HistRoutes.PAGE2)
class Page2(QtWidgets.QWidget):
    pass

def main():
    setup_navigator(HistRoutes)
    app = QtWidgets.QApplication([])
    voyager = UIVoyager()
    # add route naming pattern to avoid RouteValidationError
    voyager.add_route_pattern(r'^hist\.[a-z0-9_]+$')
    win_main = voyager.navigate_to(HistRoutes.MAIN)
    win_main.show()
    win1 = voyager.navigate_to(HistRoutes.PAGE1)
    win2 = voyager.navigate_to(HistRoutes.PAGE2)
    print("History:", voyager.navigation_history)
    voyager.navigate_back()  # returns to PAGE1
    print("After back, history:", voyager.navigation_history)
    app.exec()

if __name__ == "__main__":
    main()
