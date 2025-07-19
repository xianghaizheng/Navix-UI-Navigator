"""
Navix Example 06 - RBAC Permission Control & Enterprise Security

Why add RBAC (Role-Based Access Control) to Python UI?
- In enterprise applications, different users (roles) need different permissions for UI features and routes.
- RBAC allows you to define roles, assign permissions, and restrict access to sensitive windows or actions.
- This ensures only authorized users can access admin panels, settings, or critical operations, improving security and compliance.

Principle:
- Each route (window/dialog) is mapped to required permissions.
- Users are assigned roles, and roles have permissions.
- When navigating, the security checker verifies if the current user has permission for the target route.
- If not, navigation is blocked and a warning is shown.

Difference from 03_validation_security.py:
- 03_validation_security.py demonstrates basic route/parameter validation and custom security logic (e.g., parameter-based checks).
- 06_rbac_enterprise.py uses a full RBAC manager: roles, users, permissions, and route-permission mapping.
- RBAC is more scalable and maintainable for large teams and complex permission requirements.

This example shows how to integrate RBAC into Navix navigation Python desktop applications.
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
from Navix.security.rbac import rbac_manager

# Import GUI framework
# Note: PySide6 is used as an example.
# If you use PyQt5 or another framework, adjust the import accordingly.
from PySide6 import QtWidgets
from PySide6 import QtCore

class RbacRoutes(Enum):
    MAIN = "rbac.main"
    ADMIN = "rbac.admin"

@navigate(RbacRoutes.MAIN)
class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("普通用户窗口")
        self.resize(320, 160)

@navigate(RbacRoutes.ADMIN)
class AdminWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setWindowTitle("管理员窗口")
        self.resize(320, 160)

def main():
    setup_navigator(RbacRoutes)
    app = QtWidgets.QApplication([])
    voyager = UIVoyager()

    # 配置 RBAC
    rbac_manager.add_role("admin", permissions=["access_admin"])
    rbac_manager.add_role("user", permissions=["access_main"])
    rbac_manager.assign_role("alice", "user")
    rbac_manager.assign_role("bob", "admin")
    rbac_manager.set_route_permissions(RbacRoutes.MAIN.value, ["access_main"])
    rbac_manager.set_route_permissions(RbacRoutes.ADMIN.value, ["access_admin"])

    # Security check function (must accept 3 arguments: route, params, param_names)
    def rbac_security(route, params, param_names):
        # param_names can be a list or string, but we only need "user_id"
        user_id = params.get("user_id", "")
        return rbac_manager.is_allowed(user_id, route)

    voyager.set_security_checker(rbac_security, param_names="user_id")

    # Normal user access
    win = voyager.navigate_to(RbacRoutes.MAIN, user_id="alice")
    win.show()
    # Normal user tries to access admin window
    try:
        admin_win = voyager.navigate_to(RbacRoutes.ADMIN, user_id="alice")
        if admin_win:
            admin_win.show()
    except Exception as e:
        QtWidgets.QMessageBox.warning(win, "Permission Control", str(e))
    # Admin access
    admin_win2 = voyager.navigate_to(RbacRoutes.ADMIN, user_id="bob")
    if admin_win2:
        admin_win2.show()
    app.exec()

if __name__ == "__main__":
    main()
