"""
Navix Demo 05 - Full Builder API Showcase

Why use a builder? Why design it this way?

- The builder API is designed for rapid, readable, and maintainable configuration of complex Python desktop applications.
- It allows team leaders, technical directors, and architects to centrally control all aspects of the UI system (routes, validation, security, interceptors, data containers, etc.) in a single, fluent chain.
- This approach makes it easy for teams to collaborate: everyone can see and review the full application setup in one place, and changes are easy to track.
- The builder pattern avoids scattered configuration code, reduces errors, and enables enterprise-level governance (audit, permission, validation, hooks).
- For large teams and scalable projects, this means faster onboarding, better code quality, and easier refactoring.
- The builder is also IDE-friendly: type hints, auto-completion, and documentation are available at every step.

**In summary:**  
Navix's builder API is not just for convenience—it's a strategic tool for professional teams to build, manage, and evolve complex UI applications with confidence and clarity.

This example demonstrates the complete usage of the Navix fluent builder API for configuring a professional Python desktop application.
Each step in the chain is explained below for clarity:

1. Navix_app("Navix Builder Demo")
   - Create a new Navix application builder instance with the given app name.

2. .config(custom_option="demo", theme="light")
   - Set custom configuration options for the application (can be accessed in app.config).

3. .startup_hook(startup_hook)
   - Register a function to be called when the application starts (for initialization, logging, etc).

4. .shutdown_hook(shutdown_hook)
   - Register a function to be called when the application exits (for cleanup, logging, etc).

5. .auto_detect_framework()
   - Automatically detect the available GUI framework (PyQt/PySide/wxPython/tkinter).

6. .routes(BuilderRoutes)
   - Register the application's route Enum, which defines all UI routes.

7. .main_window(BuilderRoutes.MAIN)
   - Specify the main window route (the entry point UI).

8. .import_ui_modules(__name__)
   - Import UI modules so that all @navigate-decorated classes are registered.

9. .validation()
      .patterns(r'^builder\.[a-z_]+$')
      - Add route name validation patterns (regex).
      .parameters("theme", lambda x: x in ("light", "dark"))
      - Add parameter validation rules (for navigation parameters).
      .security_checker(lambda route, params, param_names: True)
      - Set a custom security checker function (for permission control).
      .end()
   - Configure validation and security rules for navigation.

10. .interceptors()
      .logging()
      - Add a logging interceptor (logs navigation events).
      .performance()
      - Add a performance monitoring interceptor.
      .security()
          .end()
      - Add a security interceptor (can block routes, set permissions).
      .rate_limit(max_requests=10)
      - Add a rate limiting interceptor (limits navigation frequency).
      .end()
   - Configure interceptors for navigation (logging, security, performance, rate limiting).

11. .containers()
      .global_data({"theme": "light", "user": "demo_user"})
      - Set global shared data for all UI containers.
      .end()
   - Configure data containers for type-safe, cross-UI data sharing.

12. .navigation()
      .max_history(100)
      - Set the maximum navigation history length.
      .end()
   - Configure navigation manager options.

13. .build()
   - Build and finalize the Navix application.

14. app.run()
   - Start the application main loop.

This example covers all major features of the Navix builder API. You can comment/uncomment steps to see their effects.
"""

#======================================================================#
import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

from Navix.builders import Navix_app 
from Navix import navigate, setup_navigator
from enum import Enum

from PySide6 import QtWidgets
from PySide6.QtCore import QTimer

voyager = None

class BuilderRoutes(Enum):
    MAIN     = "builder.main"
    SETTINGS = "builder.settings"
    ABOUT    = "builder.about"

class ExtraRoutes(Enum):
    DASHBOARD = "extra.dashboard"
    PROFILE   = "extra.profile"
    HELP      = "extra.help"

@navigate(BuilderRoutes.MAIN, singleton=True, title="Builder Main Window")
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Navix Builder Main Window")
        self.resize(320, 160)
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Builder API Demo", self)
        layout.addWidget(label)
        btn_settings = QtWidgets.QPushButton("Open Settings Dialog", self)
        btn_about = QtWidgets.QPushButton("Open About Dialog", self)
        btn_dashboard = QtWidgets.QPushButton("Open Dashboard", self)
        btn_profile = QtWidgets.QPushButton("Open Profile", self)
        btn_help = QtWidgets.QPushButton("Open Help", self)
        layout.addWidget(btn_settings)
        layout.addWidget(btn_about)
        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_profile)
        layout.addWidget(btn_help)
        self.setLayout(layout)
        btn_settings.clicked.connect(self.open_settings)
        btn_about.clicked.connect(self.open_about)
        btn_dashboard.clicked.connect(self.open_dashboard)
        btn_profile.clicked.connect(self.open_profile)
        btn_help.clicked.connect(self.open_help)

    def open_settings(self):
        global voyager
        if voyager:
            win = voyager.navigate_to(BuilderRoutes.SETTINGS)
            if win:
                if isinstance(win, QtWidgets.QDialog):
                    win.exec()
                else:
                    win.show()

    def open_about(self):
        global voyager
        if voyager:
            win = voyager.navigate_to(BuilderRoutes.ABOUT)
            if win:
                if isinstance(win, QtWidgets.QDialog):
                    win.exec()
                else:
                    win.show()

    def open_dashboard(self):
        global voyager
        if voyager:
            win = voyager.navigate_to(ExtraRoutes.DASHBOARD)
            if win:
                win.show()

    def open_profile(self):
        global voyager
        if voyager:
            win = voyager.navigate_to(ExtraRoutes.PROFILE)
            if win:
                win.show()

    def open_help(self):
        global voyager
        if voyager:
            win = voyager.navigate_to(ExtraRoutes.HELP)
            if win:
                win.show()

@navigate(BuilderRoutes.SETTINGS, title="Settings Dialog")
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Settings Dialog")
        self.resize(240, 120)
        label = QtWidgets.QLabel("Settings Content", self)
        label.move(60, 40)

@navigate(BuilderRoutes.ABOUT, title="About Dialog")
class AboutDialog(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("About Dialog")
        self.resize(240, 120)
        label = QtWidgets.QLabel("About Navix", self)
        label.move(60, 40)

@navigate(ExtraRoutes.DASHBOARD, title="Dashboard")
class DashboardWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(300, 180)
        label = QtWidgets.QLabel("This is the dashboard window", self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)

@navigate(ExtraRoutes.PROFILE, title="Profile")
class ProfileWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Profile")
        self.resize(300, 180)
        label = QtWidgets.QLabel("This is the profile window", self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)

@navigate(ExtraRoutes.HELP, title="Help")
class HelpWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Help")
        self.resize(300, 180)
        label = QtWidgets.QLabel("This is the help window", self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)

def startup_hook(app):
    print("[Startup Hook] Application is starting...")

def shutdown_hook(app):
    print("[Shutdown Hook] Application is shutting down...")

def simple_builder_demo():
    """
    Simple Navix builder demo: only the most common configuration steps.
    """
    app = (
        Navix_app("Simple Navix Demo")
        .framework("PySide6")
        .routes(BuilderRoutes)
        .main_window(BuilderRoutes.MAIN)
        .import_ui_modules(__name__)
        .build()
    )
    app.run()

def main():
    global voyager
    voyager = None
    from Navix import UIVoyager
    voyager = UIVoyager()
    app = (
        Navix_app("Navix Builder Demo")
        .config(custom_option="demo", theme="light")
        .startup_hook(startup_hook)
        .shutdown_hook(shutdown_hook)
        .auto_detect_framework()
        .routes(BuilderRoutes)
        .routes(ExtraRoutes)
        .main_window(BuilderRoutes.MAIN)
        .import_ui_modules(__name__)
        .validation()
            .patterns(r'^builder\.[a-z_]+$', r'^extra\.[a-z_]+$')
            .parameters("theme", lambda x: x in ("light", "dark"))
            .security_checker(lambda route, params, param_names: True)
            .end()
        .interceptors()
            .logging()
            .performance() 
            .security()
                .end()
            .rate_limit(max_requests=10)
            .end() 
        .containers()
            .global_data({"theme": "light", "user": "demo_user"})
            .end()
        .navigation()
            .max_history(100)
            .end()
        .build()
    )
    app.voyager = voyager
    app.run()

if __name__ == "__main__":
    main()

# Explanation:
# Only the "MainWindow" is shown at startup because:
# - .main_window(BuilderRoutes.MAIN) sets the entry point to MAIN
