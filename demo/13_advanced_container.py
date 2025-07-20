"""
Navix Demo 13 - Advanced Data Container Usage Example
=====================================
Demonstrates advanced usage of route and module data containers, including status and cleanup.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()

#======================================================================#
from Navix import container_manager, ModuleDataContainer, ContainerStatus, container_property, navigate, setup_navigator
from enum import Enum
from PySide6 import QtWidgets

class AdvRoutes(Enum):
    SETTINGS = "adv.settings"
    MODULE = "adv.module"

@navigate(AdvRoutes.SETTINGS)
class SettingsDialog(QtWidgets.QDialog):
    @container_property(str, "light", "Theme setting")
    def theme(self): pass

def main():
    setup_navigator(AdvRoutes)
    app = QtWidgets.QApplication([])
    # normal container
    container = container_manager(AdvRoutes.SETTINGS)
    container.set("theme", "dark")
    print("Theme:", container.get("theme"))  
    print("Status:", container.status_report)  
    container.clear()
    print("After clear:", container.status_report)  
    # module container
    module_container = ModuleDataContainer("adv")
    adv_settings_container = module_container.get_route_container("adv.module")
    adv_settings_container.set("global_value", 123)
    print("Module global_value:", adv_settings_container.get("global_value")) 
    print("Module status:", adv_settings_container.status.value)
    win = SettingsDialog()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
