"""
Navix Demo 08 - Protocol & Extension Mechanism

This advanced example demonstrates:
- How to implement custom navigation interceptors using the INavigationInterceptor protocol, allowing you to block or modify navigation logic at runtime.
- How to extend Navix with your own route validators by implementing IRouteValidator, enabling enterprise-grade route and parameter validation.
- How to register and use custom extensions (interceptors, validators) in the Navix framework for maximum flexibility and governance.

Key Concepts:
1. **Protocol-Based Extension**:  
   Navix uses Python protocols (interfaces) for interceptors, validators, adapters, etc.  
   You can implement these protocols to inject custom business logic, security, auditing, or compliance features.

2. **Custom Interceptor**:  
   By implementing INavigationInterceptor, you can block navigation to certain routes, log events, enforce business rules, or trigger hooks.  
   Example: BlockAllInterceptor only allows navigation to "protocol.main", blocking all other routes.

3. **Custom Route Validator**:  
   By implementing IRouteValidator, you can enforce strict route naming conventions, parameter types, or business validation.  
   Example: CustomRouteValidator only allows routes starting with "protocol.".

4. **Registration**:  
   Use RouteCatalog.add_interceptor() to register your interceptor, and assign your validator to route_validator.validator.  
   This makes your extensions active for all navigation events.

5. **Enterprise Use**:  
   This mechanism allows CTOs, architects, and team leads to enforce company-wide UI policies, compliance, and security without modifying Navix core code.

Difference from basic demos:
- This demo is for advanced users who need to integrate custom protocols, compliance, or enterprise features.
- It shows how to plug in your own logic at the framework level, not just at the UI or route level.

Best Practice:
- Use protocol-based extension for all enterprise requirements: security, logging, auditing, compliance, custom navigation, etc.
- Keep your interceptors and validators modular and testable.

This is how you build truly professional, extensible Python desktop applications with Navix.
"""

import sys
from pathlib import Path
def setup_project_path():
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
setup_project_path()
#======================================================================#

from Navix.interfaces import INavigationInterceptor, IRouteValidator, IWidgetWrapper
from Navix.routing import RouteCatalog
from Navix import navigate, setup_navigator, UIVoyager
from enum import Enum
from PySide6 import QtWidgets

class ProtocolRoutes(Enum):
    MAIN = "protocol.main"

@navigate(ProtocolRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("Protocol Extension Demo")
        self.resize(320, 160)
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Custom Interceptor & Validator Demo", self)
        layout.addWidget(label)
        self.setLayout(layout)

# Custom interceptor implementing INavigationInterceptor
class BlockAllInterceptor(INavigationInterceptor):
    def intercept(self, route, params):
        # Block all navigation except protocol.main
        return route == ProtocolRoutes.MAIN.value
    def get_priority(self):
        return 10

# Custom route validator
class CustomRouteValidator(IRouteValidator):
    def validate_route(self, route):
        # Only allow routes starting with "protocol."
        if not str(route).startswith("protocol."):
            raise ValueError("Route must start with 'protocol.'")
    def validate_params(self, params):
        # Accept all params
        return True

def main():
    setup_navigator(ProtocolRoutes)
    app = QtWidgets.QApplication([])
    voyager = UIVoyager()
    # Register custom interceptor
    RouteCatalog.add_interceptor(BlockAllInterceptor())
    # Register custom route validator (fix: assign to route_validator.validator)
  
    from Navix.validation import route_validator
    route_validator.validator = CustomRouteValidator()
    win = voyager.navigate_to(ProtocolRoutes.MAIN)
    win.show()
    # Try to navigate to a blocked route
    try:
        voyager.navigate_to("other.route")
    except Exception as e:
        QtWidgets.QMessageBox.warning(win, "Custom Interceptor", str(e))
    app.exec()

if __name__ == "__main__":
    main()
