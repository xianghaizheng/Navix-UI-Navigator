"""
Navix Demo 07 - Adapter Framework & Multi-GUI Support

This example demonstrates:
- How Navix automatically detects and adapts to different GUI frameworks (PyQt5/6, PySide2/6, wxPython, tkinter).
- How to use GUIAdapter to switch frameworks at runtime.
- How WidgetWrapper provides a unified interface for widgets across frameworks.
- How to write framework-agnostic UI code using Navix adapters.

You can run this demo with different GUI frameworks installed to see automatic detection and adaptation.
"""
import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()
#======================================================================#

from Navix.adapters import GUIAdapter, WidgetWrapper, FrameworkDetector
from Navix import navigate, setup_navigator, UIVoyager
from Navix.config import global_config
from enum import Enum
import importlib

# Try to auto-detect framework
framework_name, _, _ = FrameworkDetector.detect_framework()
print(f"Detected GUI framework: {framework_name}")

# Optionally, force a specific framework (uncomment to test)
# GUIAdapter.set_framework("PyQt5")
# GUIAdapter.set_framework("PySide6")
# GUIAdapter.set_framework("wxPython")
# GUIAdapter.set_framework("tkinter")

# Import the correct Qt/wx/tk widgets based on config mapping (no hardcoding)
frameworks = global_config.Frameworks()
if framework_name not in frameworks:
    raise ImportError(f"Unsupported framework: {framework_name}")
module_name = frameworks[framework_name]["module_name"]
QtWidgets = importlib.import_module(module_name)
print(f"Using QtWidgets from: {QtWidgets.__name__}")


class AdapterRoutes(Enum):
    MAIN = "adapter.main"

@navigate(AdapterRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle(f"Adapter Demo - {framework_name}")
        self.resize(320, 160)
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(f"Framework: {framework_name}", self)
        layout.addWidget(label)
        btn = QtWidgets.QPushButton("Show Widget Info", self)
        layout.addWidget(btn)
        self.setLayout(layout)
        btn.clicked.connect(self.show_widget_info)

    def show_widget_info(self):
        # Demonstrate WidgetWrapper usage
        wrapper = WidgetWrapper(self, framework_name)
        info = f"Widget type: {type(self).__name__}\n" \
               f"Is hidden: {wrapper.is_hidden()}\n" \
               f"Native widget: {wrapper.native_widget}"
        QtWidgets.QMessageBox.information(self, "Widget Info", info)

def main():
    setup_navigator(AdapterRoutes)
    app = QtWidgets.QApplication([])
    voyager = UIVoyager()
    win = voyager.navigate_to(AdapterRoutes.MAIN)
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
