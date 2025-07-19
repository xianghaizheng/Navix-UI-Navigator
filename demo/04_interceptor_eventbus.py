"""
Navix Demo 04 - Interceptor & Navigation Event Bus

This example demonstrates the interceptor mechanism and navigation event bus (publish/subscribe) features of the Navix framework:

1. Route definition and registration: Use Enum and @navigate decorator to register UI routes.
2. Interceptor mechanism: Register interceptors via RouteCatalog.add_interceptor to block specific routes (e.g., BLOCKED) before navigation.
3. Event bus: Subscribe to navigation events (e.g., before_navigate, navigation_failed) via navigation_event_bus.subscribe, allowing custom logic before/after navigation or on failure.
4. Navigation flow: UIVoyager manages navigation, interceptors can block navigation, and the event bus can respond to navigation events.
5. Typical scenarios: Permission control, logging, navigation failure popups, etc.

When running this demo, attempting to navigate to the blocked window will be intercepted and trigger the navigation_failed event (you can show a popup or log in on_navigation_failed).
This file is suitable for learning and referencing Navix's interceptor and event bus extension mechanisms.
"""
import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

#======================================================================#
from enum import Enum
from Navix import navigate, UIVoyager, setup_navigator
from Navix.routing import RouteCatalog
from Navix.navigation import navigation_event_bus

# Import GUI framework (PySide6 used for demonstration)
# Adjust imports for PyQt5/PyQt6/PySide2 as needed in your environment.
from PySide6 import QtWidgets
from PySide6 import QtCore

class EventRoutes(Enum):
    MAIN    = "event.main"
    BLOCKED = "event.blocked"

@navigate(EventRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("main window")
        self.resize(320, 160)

@navigate(EventRoutes.BLOCKED)
class BlockedWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("blocked window")
        self.resize(320, 160)

def block_interceptor(route, params):
    # block the BLOCKED route
    # This interceptor will prevent navigation to the BLOCKED route
    if route == EventRoutes.BLOCKED.value:
        return False
    return True

def on_before_navigate(route, params, **_):
    print(f"[EventBus] will navigate to: {route}, with params: {params}")

def on_navigation_failed(route, params, error, **_):
    print(f"[EventBus] navigation failed: {route}, error: {error}")
    # show a popup or log the error
    #parent = QtWidgets.QApplication.activeWindow()
    #QtWidgets.QMessageBox.warning(parent, "Interceptor", f"Navigation to {route} was intercepted or failed.\nError: {error}")

def main():
    setup_navigator(EventRoutes)
    app     = QtWidgets.QApplication([])
    voyager = UIVoyager()
    
    # Register the interceptor
    RouteCatalog.add_interceptor(block_interceptor)
    # Subscribe to navigation events
    navigation_event_bus.subscribe("before_navigate", on_before_navigate)
    # Subscribe to navigation failed event
    navigation_event_bus.subscribe("navigation_failed", on_navigation_failed)

    win = voyager.navigate_to(EventRoutes.MAIN)
    win.show()
    
    # Attempt to navigate to the blocked window
    try:
        blocked_win = voyager.navigate_to(EventRoutes.BLOCKED)
        if blocked_win:
            blocked_win.show()
    except Exception as e:
        pass
    app.exec()

if __name__ == "__main__":
    main()
