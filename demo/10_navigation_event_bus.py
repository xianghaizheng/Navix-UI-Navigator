"""
Navix Demo 10 - Navigation Event Bus Full Example
=====================================
Demonstrates full usage of subscribe, unsubscribe, and publish.
"""
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
#======================================================================#

from enum import Enum
from Navix import navigate, UIVoyager, setup_navigator
from Navix.navigation import navigation_event_bus

# Import GUI framework
# Note: PySide6 is used as an example.
# If you use PyQt5 or another framework, adjust the import accordingly.
from PySide6 import QtWidgets
from PySide6 import QtCore

class DemoRoutes(Enum):
    MAIN = "demo.main"

@navigate(DemoRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(300, 120)
        label = QtWidgets.QLabel("Main Window (demo.main)", self)
        label.move(40, 40)

def on_before_navigate(route, params, **_):
    print(f"[EventBus] Before navigating to {route}, params={params}")

def on_after_navigate(route, params, instance, **_):
    print(f"[EventBus] After navigating to {route}, instance={instance}")

def on_navigation_failed(route, params, error, **_):
    print(f"[EventBus] Navigation to {route} failed: {error}")

def on_custom_event(info, **_):
    print(f"[EventBus] Custom event received: {info}")

def main():
    setup_navigator(DemoRoutes)
    app = QtWidgets.QApplication(sys.argv)
    voyager = UIVoyager()

    # 1. Subscribe to events
    navigation_event_bus.subscribe("before_navigate", on_before_navigate)
    navigation_event_bus.subscribe("after_navigate", on_after_navigate)
    navigation_event_bus.subscribe("navigation_failed", on_navigation_failed)
    navigation_event_bus.subscribe("custom_event", on_custom_event)

    # 2. Navigate, trigger events
    win = voyager.navigate_to(DemoRoutes.MAIN, user_id="alice")
    if win:
        win.show()
        print("Main window shown. Try closing to exit.")

        # 3. Unsubscribe after_navigate
        navigation_event_bus.unsubscribe("after_navigate", on_after_navigate)

        # 4. Navigate again, after_navigate will not be triggered
        voyager.navigate_to(DemoRoutes.MAIN, user_id="alice")

        # 5. Manually publish a custom event
        navigation_event_bus.publish("custom_event", info="This is a custom event.")

        sys.exit(app.exec())
    else:
        print("Failed to start main window.")

if __name__ == "__main__":
    main()
