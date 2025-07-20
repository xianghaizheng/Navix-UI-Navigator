"""
Navix Demo 12 - Exception Handling Example
=====================================
Demonstrates how to catch and handle Navix exceptions during navigation and route operations.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

#======================================================================#
from Navix import UIVoyager, RouteNotFoundError, ValidationError, RouteError, RouteConflictError, FrameworkError, NavixError, NavigationError
from enum import Enum
from PySide6 import QtWidgets

class ErrorRoutes(Enum):
    MAIN = "error.main"

def main():
    app = QtWidgets.QApplication([])
    voyager = UIVoyager()
    # NavigationError (invalid route)
    try:
        voyager.navigate_to("nonexistent.route")
    except NavigationError as e:
        print("NavigationError:", e)
        # check if the cause is a RouteNotFoundError
        if isinstance(e.__cause__, RouteNotFoundError):
            print("Underlying RouteNotFoundError:", e.__cause__)
    # ValidationError
    try:
        voyager.navigate_to(ErrorRoutes.MAIN, user_id=None)
    except NavigationError as e:
        print("NavigationError (validation):", e)
        if isinstance(e.__cause__, ValidationError):
            print("Underlying ValidationError:", e.__cause__)
    # RouteError
    try:
        raise RouteError("Custom route error")
    except RouteError as e:
        print("RouteError:", e)
    # RouteConflictError
    try:
        raise RouteConflictError("Route conflict detected")
    except RouteConflictError as e:
        print("RouteConflictError:", e)
    # FrameworkError
    try:
        raise FrameworkError("Framework error")
    except FrameworkError as e:
        print("FrameworkError:", e)
    # NavixError
    try:
        raise NavixError("Generic Navix error")
    except NavixError as e:
        print("NavixError:", e)

if __name__ == "__main__":
    main()
