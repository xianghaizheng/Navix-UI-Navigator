"""
Navix Demo 02 - Data Container
Demonstrates: Declaring container properties, sharing data across UIs.
In practice, the container is a global data store.

Note:
This example does not use voyager; it mainly demonstrates how to use container_manager for data sharing.
This is one of Navix's features: decoupling UI components from data management. You are not forced to use the navigator,
but if you do not, you must manually manage the lifecycle and data flow of container properties, which is outside the Navix framework.
"""
#======================================================================#
# intentionally left blank to ensure proper module structure
import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()
#======================================================================#
# Import necessary modules
from enum import Enum
from Navix import  navigate, container_manager, container_property, setup_navigator

# Import GUI framework
# Note: PySide6 is used as an example.
# If you use PyQt5 or another framework, adjust the import accordingly.
from PySide6 import QtWidgets
from PySide6.QtCore import QTimer

#= Enum for routes =#
class DataRoutes(Enum):
    MAIN     = "data.main"
    SETTINGS = "data.settings"

# Register settings dialog route
@navigate(DataRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(240, 120)

        # Read container property
        description_data = container_manager(DataRoutes.SETTINGS).get('theme')
        self.edit = QtWidgets.QLineEdit(self)
        self.edit.move(40, 40)
        self.edit.setText(description_data)
        self.btn = QtWidgets.QPushButton("push", self)
        self.btn.move(40, 80)
        # Button click event: stores user input in the container
        # Other UI components can read this setting
        self.btn.clicked.connect(self.save_theme)
        main_description_data = container_manager("data.main").get('maintheme', 'default')
        print(f"main description data: {main_description_data}")

    def save_theme(self):
        # Save theme setting to global container
        container_manager(DataRoutes.SETTINGS).set('theme', self.edit.text())
        # Demonstrate container methods

        # 1. List all keys in the container
        keys = container_manager("data.main").list_keys()
        print(f"container keys: {keys}")

        # 2. Get data from the container
        sturctured_data = container_manager("data.main").get("maintheme1", [])
        print(f"structured data: {sturctured_data}")
        sturctured_data2 = container_manager("data.main").get("maintheme2", [])
        print(f"structured data2: {sturctured_data2}")

        # 3. Set/create data in the container
        container_manager.get_container(DataRoutes.MAIN).set("maintheme3", {"key1": "value1", "key2": "value2"})
        print(f"container data: {container_manager.get_container(DataRoutes.MAIN).get('maintheme3', {})}")

        # 4. Update data in the container
        container_manager.get_container(DataRoutes.MAIN).update({"maintheme3": {"key1": "new_value1", "key2": "new_value2"}})
        print(f"updated container data: {container_manager.get_container(DataRoutes.MAIN).get('maintheme3', {})}")

        # 5. Clear data in the container
        container_manager.get_container(DataRoutes.MAIN).clear("maintheme3")
        print(f"cleared container data: {container_manager.get_container(DataRoutes.MAIN).get('maintheme3', {})}")

        # 6. Get container status report
        rep = container_manager.get_status_report()
        print(f"container status report: {rep}")

        # 7. Get all data in the container
        all_data = container_manager.get_container(DataRoutes.MAIN).items()
        print(f"all container data: {all_data}")

        # 8. List all modules in the container manager
        all_mod = container_manager.list_all_modules()
        print(f"all container modules: {all_mod}")

        # 9. List all registered routes
        all_routes = container_manager.list_all_routes()
        print(f"all container routes: {all_routes}")

        # 10. List all container instances
        all_containers = container_manager.list_all_containers()
        print(f"all container instances: {all_containers}")
        # To clear all data in the container:
        # container_manager.get_container(DataRoutes.MAIN).clear_data()
        # print(f"cleared all container data: {container_manager.get_container(DataRoutes.MAIN).list_keys()}")

#======================================================================#
# Register main window route
@navigate(DataRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("main_window")
        self.resize(320, 160)
        btn = QtWidgets.QPushButton("open settings", self)
        btn.move(100, 60)
        btn.clicked.connect(self.open_settings)
        self.time_label = QtWidgets.QLabel("current time:", self)
        self.time_label.setGeometry(200, 100, 200, 30)
        self.timeChecker()

        # You can use either the route enum or string to access container properties
        # The container is structured and can store complex data structures
        container_manager("data.main").set("maintheme1", ["A", "B", "C"])
        container_manager("data.main").set("maintheme2", {"key1": "value1", "key2": "value2"})

    def open_settings(self):
        # Set container property so the settings dialog can read it
        # DataRoutes.SETTINGS is the route defined above
        # 'theme' is the property name, 'dark' is the default value
        # You can modify this value in the settings dialog
        container_manager(DataRoutes.SETTINGS).set("theme", "dark")
        dlg = SettingsDialog()
        dlg.exec()

    def timeChecker(self):
        # Get current time and update label
        # Here we read the theme setting from the container
        theme = container_manager(DataRoutes.SETTINGS).get('theme', 'waiting')
        self.time_label.setText(theme)
        # Update every second
        QTimer.singleShot(500, self.timeChecker)

def main():
    # Setup navigator
    setup_navigator(DataRoutes)
    app = QtWidgets.QApplication([])
    win =  MainWindow()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
