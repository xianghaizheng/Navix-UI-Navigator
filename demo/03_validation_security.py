"""
Navix Example 03 - Validation & Security
# How Validation & Security Work (Navix Framework)

# 1. **Route Validation**
#    - Navix supports validating route names using regular expressions to prevent typos or unregistered routes.
#    - You can use `voyager.add_route_pattern(r'^secure\.[a-z_]+$')` to add valid route rules.
#    - When navigating (`navigate_to`), Navix checks if the route matches these rules; if not, it raises an exception.

# 2. **Parameter Validation**
#    - Navix supports type and content validation for navigation parameters.
#    - You can use `voyager.add_parameter_rule('user_id', lambda x: isinstance(x, str) and len(x) > 0)` to add parameter validation rules.
#    - During navigation, Navix checks if parameters meet these rules; if not, it raises an exception.

# 3. **Security Validation**
#    - Navix supports custom security check functions (`security_checker`) for permission control.
#    - Register your security check function with `voyager.set_security_checker(security_checker)`.
#    - The function must accept two arguments: `route` (route name or enum) and `params` (navigation parameter dict).
#    - On each navigation, Navix calls your security check function to determine if the current user has access.
#    - If it returns `False`, navigation is denied and an exception is raised.

# 4. **Navigation Flow**
#    - When you call `voyager.navigate_to(route, **params)`, Navix performs:
#      1. Route validation (regex rules)
#      2. Parameter validation (parameter rules)
#      3. Security validation (permission check function)
#      4. Interceptors (optional)
#      5. Instantiate and show UI

# 5. **Exception Handling**
#    - If any validation step fails, Navix raises an exception (e.g., `NavigationError`), which you can catch and display a popup.

# **Summary:**
# - Route validation ensures navigation targets are valid.
# - Parameter validation ensures data passed is valid.
# - Security validation ensures permission control.
# - You can flexibly customize rules and security logic; Navix automatically checks them during navigation.

# # This enables enterprise-grade navigation security and data validation in your application!
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
import logging
from Navix import navigate, UIVoyager, setup_navigator,security_validator
# Import GUI framework
# Note: PySide6 is used as an example.
# If you use PyQt5 or another framework, adjust the import accordingly.
from PySide6 import QtWidgets

# Route Enum definition
# Best practice: Use descriptive names and consistent naming conventions (UPPERCASE with underscores).
# In production, define routes in a separate module for better team management and scalability.
class SecureRoutes(Enum):
    MAIN  = "secure.main"
    ADMIN = "secure.admin"

@navigate(SecureRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, address=None, user_id=None, **kwargs):
        super().__init__()
        self.setWindowTitle("normal user window")
        self.resize(320, 160)
        # Show address and user_id in UI
        # If you did not want insert some parmeters, you can remove the address and user_id parameters
        # and use default values in the UI
        # because sometimes you didnot want anyone to see the address and user_id
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(f"Address: {address}\nUser ID: {user_id}", self)
        layout.addWidget(label)
        self.setLayout(layout)

@navigate(SecureRoutes.ADMIN)
class AdminWindow(QtWidgets.QWidget):
    def __init__(self, address=None, user_id=None, **kwargs):
        super().__init__()
        self.setWindowTitle("admin window")
        self.resize(320, 160)
        # Show address and user_id in UI
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel(f"Address: {address}\nUser ID: {user_id}", self)
        layout.addWidget(label)
        self.setLayout(layout)

# Method 1: voyager.set_security_checker (recommended, automatic validation during navigation)
def security_checker(route, params, param_names):
    # param_names is a list, e.g. ["address", "user_id"]
    # Implement complex permission checks based on business logic here
    # Example: Only allow access to admin route if address is "alice" and user ID is "admin"
    address = params.get("address")
    user_id = params.get("user_id")
    return address == "192.168.0.199" and user_id == "alice"

# Method 2: security_validator.set_permission_checker (manual validation)
def permission_checker(route, params, param_name="datetime"):
    # Only allow secure.admin route if datetime parameter is "2014-01-01"
    if route == "secure.admin":
        return params.get(param_name) == "2014-01-01"  
    return True

# Safe navigation function, wraps navigation logic and exception handling
# Ensures navigation failures do not crash the app and provides unified handling
def safe_navigate(voyager, route, parent=None, **params):
    try:
        win = voyager.navigate_to(route, parent=parent, **params)
        if win:
            win.show()
        return win
    except Exception as e:
        logging.error(f"Navigation failed: {e}")
        return None
    
def main():
    setup_navigator(SecureRoutes)
    app = QtWidgets.QApplication([])
    voyager = UIVoyager()

    # Add route validation rule
    # Best practice: Use regex patterns to enforce naming conventions and prevent typos.
    voyager.add_route_pattern(r'^secure\.[a-z_]+$')
   
    # Add parameter validation rules
    voyager.add_parameter_rule('address', lambda x: isinstance(x, str) and len(x) > 0)
    voyager.add_parameter_rule('user_id', lambda x: isinstance(x, str) and len(x) > 0)
    voyager.add_parameter_rule('datetime', lambda x: isinstance(x, str) and len(x) > 0)
  
    # ----------- Method 1: Automatic security validation (recommended) -----------
    # Key: Specify security parameter validation
    voyager.set_security_checker(security_checker, param_names=["address", "user_id"])    
    # Correct parameters
    safe_navigate(voyager, SecureRoutes.MAIN, address="192.168.0.199", user_id="alice")
    # Incorrect parameters will raise exception and window will not show
    safe_navigate(voyager, SecureRoutes.ADMIN, address="192.168.1.1", user_id="alice")
 
    # ----------- Method 2: Manual security validation (demonstrate set_permission_checker) Not recommended -----------
    # Custom permission check function
    # Note: If you use set_permission_checker, it will override the default security check logic
    security_validator.set_permission_checker(permission_checker)
    # Correct permission
    params_ok = {"datetime": "2014-01-01"}
    result_ok = security_validator.validate_security(SecureRoutes.ADMIN, params_ok)
    print(f"Manual permission check (correct params): {result_ok}")  # True
    # Incorrect permission
    params_bad = {"datetime": "2020-01-01"}
    result_bad = security_validator.validate_security(SecureRoutes.ADMIN, params_bad)
    print(f"Manual permission check (incorrect params): {result_bad}")  # False

    app.exec()

if __name__ == "__main__":
    main()

