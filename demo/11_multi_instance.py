"""
Navix Demo 11 - Multi-Instance Navigation Example
=====================================
Demonstrates how to open and manage multiple UI instances with instance_id and endpoint.
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
#======================================================================#

from enum import Enum
from Navix import navigate, UIVoyager, setup_navigator

# Import GUI framework
# Note: PySide6 is used as an example.
# If you use PyQt5 or another framework, adjust the import accordingly.
from PySide6 import QtWidgets
from PySide6 import QtCore

class DemoRoutes(Enum):
    EDITOR = "demo.editor"


@navigate(DemoRoutes.EDITOR)
class EditorWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle(f"Editor Window")
        self.resize(350, 180)
        # show instance_id and endpoint
        self.instance_id = kwargs.get("instance_id", "default")
        self.endpoint = kwargs.get("endpoint", "local")
        label = QtWidgets.QLabel(f"Editor Instance\ninstance_id: {self.instance_id}\nendpoint: {self.endpoint}", self)
        label.move(40, 20)

        # keep track of open windows
        # This allows us to manage multiple instances and endpoints
        if not hasattr(EditorWindow, "_open_windows"):
            EditorWindow._open_windows = {}
        EditorWindow._open_windows[f"{self.instance_id}@{self.endpoint}"] = self

        # just some buttons to demonstrate navigation
        btn1 = QtWidgets.QPushButton("open user1 editor", self)
        btn1.move(40, 70)
        btn1.clicked.connect(self.open_user1_editor)

        btn2 = QtWidgets.QPushButton("open user2 editor", self)
        btn2.move(180, 70)
        btn2.clicked.connect(self.open_user2_editor)

        btn3 = QtWidgets.QPushButton("open user3 remote editor", self)
        btn3.move(40, 110)
        btn3.clicked.connect(self.open_user3_remote_editor)

        btn4 = QtWidgets.QPushButton("close and remove", self)
        btn4.move(180, 110)
        btn4.clicked.connect(self.close_and_remove)

    def open_user1_editor(self):
        voyager = UIVoyager()
        win = voyager.navigate_to(DemoRoutes.EDITOR, instance_id="user1", endpoint="local")
        if win:
            win.show()
            EditorWindow._open_windows["user1@local"] = win

    def open_user2_editor(self):
        voyager = UIVoyager()
        win = voyager.navigate_to(DemoRoutes.EDITOR, instance_id="user2", endpoint="local")
        if win:
            win.show()
            EditorWindow._open_windows["user2@local"] = win

    def open_user3_remote_editor(self):
        voyager = UIVoyager()
        win = voyager.navigate_to(DemoRoutes.EDITOR, instance_id="user3", endpoint="remote")
        if win:
            win.show()
            EditorWindow._open_windows["user3@remote"] = win

    def close_and_remove(self):
        key = f"{self.instance_id}@{self.endpoint}"
        if hasattr(EditorWindow, "_open_windows") and key in EditorWindow._open_windows:
            del EditorWindow._open_windows[key]
        self.close()

def main():
    setup_navigator(DemoRoutes)
    app = QtWidgets.QApplication(sys.argv)
    voyager = UIVoyager()

    # open multiple instances of the editor
    win1 = voyager.navigate_to(DemoRoutes.EDITOR, instance_id="user1", endpoint="local")
    win2 = voyager.navigate_to(DemoRoutes.EDITOR, instance_id="user2", endpoint="local")
    win3 = voyager.navigate_to(DemoRoutes.EDITOR, instance_id="user3", endpoint="remote")

    if win1: win1.show()
    if win2: win2.show()
    if win3: win3.show()

    print("Active navigations:", voyager.get_active_navigations())
    print("Note:")
    print("1. every editor window is a separate instance with its own state.")
    print("2. click buttons to open more instances.")
    print("   You can open multiple instances with different instance_id and endpoint.")
    print("3. support multiple endpoints, e.g., local and remote.")
    print("4. you can close any instance, it will be removed from the active navigations.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
