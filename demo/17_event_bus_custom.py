"""
Navix Demo 17 - Custom EventBus Example
=====================================
Demonstrates custom event subscription, publishing, and UI updates via navigation_event_bus.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

#======================================================================#
from Navix.navigation.event_bus import navigation_event_bus
from Navix import UIVoyager, navigate, setup_navigator
from enum import Enum
from PySide6 import QtWidgets

class EventRoutes(Enum):
    MAIN = "event.main"

@navigate(EventRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EventBus Demo")
        self.resize(320, 160)
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Waiting for event...", self)
        layout.addWidget(self.label)
        btn = QtWidgets.QPushButton("Send Custom Event", self)
        btn.clicked.connect(self.send_event)
        layout.addWidget(btn)

    def send_event(self):
        navigation_event_bus.publish("custom_event", msg="Button clicked!")

def on_custom_event(*args, **kwargs):
    # fixme: this is a custom event handler
    # it will be called when a custom event is published
    print("Custom event received:", args, kwargs)
    msg = None
    # support both positional and keyword arguments
    if args and isinstance(args[0], dict) and "msg" in args[0]:
        msg = args[0]["msg"]
    elif "msg" in kwargs:
        msg = kwargs["msg"]
    else:
        msg = str(args) if args else str(kwargs)
    app = QtWidgets.QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, MainWindow):
            widget.label.setText(f"Event: {msg}")

def main():
    setup_navigator(EventRoutes)
    app = QtWidgets.QApplication([])
    navigation_event_bus.subscribe("custom_event", on_custom_event)
    voyager = UIVoyager()
    win = voyager.navigate_to(EventRoutes.MAIN)
    win.show()
    # publish a custom event to demonstrate
    navigation_event_bus.publish("custom_event", msg="Hello EventBus!")
    app.exec()

if __name__ == "__main__":
    main()
