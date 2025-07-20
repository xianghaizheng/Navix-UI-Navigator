"""
Navix Demo 01 - Basic Navigation
Demonstrates: Enum-based routing, UI registration, navigation to main window with embedded child window.
This example shows how to use Navix's navigation features to build a minimal main window application with an embedded child window.
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

# Import GUI framework
# Note: PySide6 is used as an example.
# If you use PyQt5 or another framework, adjust the import accordingly.
from PySide6 import QtWidgets
from PySide6 import QtCore

voyager = None

# Additional route enum
# Route Enum definition
# Best practice: Use descriptive names and consistent naming conventions (UPPERCASE with underscores).
# In production, define routes in a separate module for better team management and scalability
class SimpleRoutes(Enum):
    MAIN  = "simple.main"
    CHILD = "simple.child"
class ExtraSimpleRoutes(Enum):
    DASHBOARD = "extra.dashboard"
    PROFILE   = "extra.profile"
    HELP      = "extra.help"
    
# Register main window route
# @navigate decorator registers the UI class for a route.
# Parameters:
#   singleton=True: Enforces single instance for this window.
#   title: Sets window title.
#   metadata: Stores extra info (e.g., icon path, config).
@navigate(SimpleRoutes.MAIN, singleton=True, title="Main Window")
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Navix Simple Main Window")
        self.resize(300, 250)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Welcome!", self)
        self.label.setFixedHeight(30)
        self.childDock = QtWidgets.QFrame(self)
        self.childDock.setMinimumHeight(100)
        self.childDock.setStyleSheet("background-color: blue;")
        self.childDock_layout = QtWidgets.QVBoxLayout(self.childDock)
        self.childDock_layout.setContentsMargins(0, 0, 0, 0)
        self.childDock_layout.setAlignment(QtCore.Qt.AlignTop)
        self.childDock_layout.setSpacing(5)
        self.btn = QtWidgets.QPushButton("Open Child Window", self)
        self.btn.setFixedHeight(30)
        self.btn_dashboard = QtWidgets.QPushButton("Open Dashboard", self)
        self.btn_profile = QtWidgets.QPushButton("Open Profile", self)
        self.btn_help = QtWidgets.QPushButton("Open Help", self)
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.childDock)
        self.mainLayout.addWidget(self.btn)
        self.mainLayout.addWidget(self.btn_dashboard)
        self.mainLayout.addWidget(self.btn_profile)
        self.mainLayout.addWidget(self.btn_help)
        self.setLayout(self.mainLayout)
        self.btn.clicked.connect(self.open_child_window)
        self.btn_dashboard.clicked.connect(self.open_dashboard)
        self.btn_profile.clicked.connect(self.open_profile)
        self.btn_help.clicked.connect(self.open_help)

    def open_child_window(self):
        self.child_window = voyager.navigate_to(
            SimpleRoutes.CHILD,
            parent=self.childDock,
            window_title="Positioned Child Window",
            custom_data={"user": "alice"},
            parent_layout=self.childDock_layout,
            margin=(5, 5, 5, 5),
        )
        if self.child_window:
            # If voyager returns a wrapper, use .native_widget; otherwise, use the instance directly.
            #  wrapper:
            #  widget = getattr(self.child_window, "native_widget", self.child_window)
            #  self.childDock_layout.addWidget(widget)
            self.childDock_layout.addWidget(self.child_window)

    def open_dashboard(self):
        win = voyager.navigate_to(ExtraSimpleRoutes.DASHBOARD)
        if win:
            win.show()

    def open_profile(self):
        win = voyager.navigate_to(ExtraSimpleRoutes.PROFILE)
        if win:
            win.show()

    def open_help(self):
        win = voyager.navigate_to(ExtraSimpleRoutes.HELP)
        if win:
            win.show()

@navigate(SimpleRoutes.CHILD, title="Child Window")
class ChildWindow(QtWidgets.QFrame):
    def __init__(self, parent=None, 
                 window_title=None, custom_data=None, parent_layout=None, margin=None, **kwargs):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightblue;")
        self.setFixedHeight(30)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setWindowTitle(window_title if window_title else "Navix Simple Child Window")
        if custom_data:
            print(f"Received custom data: {custom_data}")
        if margin and parent_layout:
            parent_layout.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
        self.label = QtWidgets.QLabel("This is a child window", self)
        self.main_layout.addWidget(self.label)
        self.setLayout(self.main_layout)

# ExtraSimpleRoutes corresponding UI
@navigate(ExtraSimpleRoutes.DASHBOARD, title="Dashboard")
class DashboardWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(300, 180)
        label = QtWidgets.QLabel("This is the dashboard window", self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)

@navigate(ExtraSimpleRoutes.PROFILE, title="Profile")
class ProfileWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Profile")
        self.resize(300, 180)
        label = QtWidgets.QLabel("This is the profile window", self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)

@navigate(ExtraSimpleRoutes.HELP, title="Help")
class HelpWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Help")
        self.resize(300, 180)
        label = QtWidgets.QLabel("This is the help window", self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)

def main():
    """
    Application entry point.
    In production, call setup_navigator for each route Enum to register all routes.
    Example: setup_navigator(AssetRoutes), setup_navigator(DataRoutes), etc.

    Summary:
    - @navigate: Registers UI class for a route.
    - setup_navigator: Registers all routes from an Enum for global management and validation.
    - navigate_to: Navigates to a registered UI.
    """
    global voyager 
    setup_navigator(SimpleRoutes)
    setup_navigator(ExtraSimpleRoutes)
    app     = QtWidgets.QApplication([])
    # Initialize UIVoyager
    voyager = UIVoyager()
    # Navigate to the main window
    win     = voyager.navigate_to(SimpleRoutes.MAIN)
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
