"""
Navix RBAC - Role-Based Access Control for UI Navigation (Advanced API)
=====================================================================
Provides advanced role, user, and permission management for route-level access control.
"""
# standard libraries
from typing import Dict, Set, List, Callable, Any

class RBACManager:
    def __init__(self):
       
        self._roles: Dict[str, Set[str]] = {}           # role -> set(permission)
        self._role_parents: Dict[str, Set[str]] = {}    # role -> set(parent_role)
        self._users: Dict[str, Set[str]] = {}           # user_id -> set(role)
        self._route_permissions: Dict[str, Set[str]] = {} # route -> set(permission)
        self._event_hooks: Dict[str, List[Callable]] = {} # event_name -> [func]
    
 
    #Role Management 
    def add_role(self, role: str, permissions: List[str] = None, parents: List[str] = None):
        """
        Add a new role with optional permissions and parent roles
        Args:
            role: The name of the role to add.
            permissions: Optional list of permissions for the role.
            parents: Optional list of parent roles to inherit permissions from.
        Returns:
            None
        """
        self._roles.setdefault(role, set())
        if permissions:
            self._roles[role].update(permissions)
        if parents:
            self._role_parents.setdefault(role, set()).update(parents)
        self._trigger_event('role_added', role=role)

    def remove_role(self, role: str):
        """
        Remove a role and its associated permissions
        Args:
            role: The name of the role to remove.
        Returns:
            None
        """
        self._roles.pop(role, None)
        self._role_parents.pop(role, None)
        for user_roles in self._users.values():
            user_roles.discard(role)
        self._trigger_event('role_removed', role=role)

    def set_role_permissions(self, role: str, permissions: List[str]):
        """
        Set permissions for a specific role
        Args:
            role: The name of the role.
            permissions: List of permissions to assign to the role.
        Returns:
            None
        """
        self._roles[role] = set(permissions)
        self._trigger_event('role_permissions_updated', role=role)

    def get_role_permissions(self, role: str, recursive: bool = True) -> Set[str]:
        """
        Get permissions for a specific role
        Args:
            role: The name of the role.
            recursive: Whether to include permissions from parent roles.
        Returns:
            A set of permissions for the role.
        """
        perms = set(self._roles.get(role, set()))
        if recursive:
            for parent in self._role_parents.get(role, set()):
                perms.update(self.get_role_permissions(parent, recursive=True))
        return perms

    def list_roles(self) -> List[str]:
        return list(self._roles.keys())

    #User Management
    def assign_role(self, user_id: str, role: str):
        """
        Assign a role to a user
        Args:
            user_id: The ID of the user.
            role: The name of the role to assign.
        Returns:
            None
        """
        self._users.setdefault(user_id, set()).add(role)
        self._trigger_event('user_role_assigned', user_id=user_id, role=role)

    def revoke_role(self, user_id: str, role: str):
        """
        Revoke a role from a user
        Args:
            user_id: The ID of the user.
            role: The name of the role to revoke.
        Returns:
            None
        """
        if user_id in self._users:
            self._users[user_id].discard(role)
            self._trigger_event('user_role_revoked', user_id=user_id, role=role)

    def set_user_roles(self, user_id: str, roles: List[str]):
        """
        Set roles for a user
        Args:
            user_id: The ID of the user.
            roles: List of roles to assign to the user.
        Returns:
            None
        """
        self._users[user_id] = set(roles)
        self._trigger_event('user_roles_updated', user_id=user_id)

    def get_user_roles(self, user_id: str) -> Set[str]:
        """
        Get roles assigned to a user
        Args:
            user_id: The ID of the user.
        Returns:
            A set of roles assigned to the user.
        """
        return set(self._users.get(user_id, set()))

    def list_users(self) -> List[str]:
        return list(self._users.keys())

    # Permission Management 
    def set_route_permissions(self, route: str, permissions: List[str]):
        """
        Set permissions required to access a specific route
        Args:
            route: The name of the route.
            permissions: List of permissions required to access the route.
        Returns:
            None
        """
        self._route_permissions[route] = set(permissions)
        self._trigger_event('route_permissions_updated', route=route)

    def get_route_permissions(self, route: str) -> Set[str]:
        return set(self._route_permissions.get(route, set()))

    def list_routes(self) -> List[str]:
        return list(self._route_permissions.keys())

    #Query & Check
    def get_user_permissions(self, user_id: str, recursive: bool = True) -> Set[str]:
        """
        Get all permissions for a user, including inherited permissions from roles
        Args:
            user_id: The ID of the user.
            recursive: Whether to include permissions from roles recursively.
        Returns:
            A set of permissions for the user.
        """
        perms = set()
        for role in self.get_user_roles(user_id):
            perms.update(self.get_role_permissions(role, recursive=recursive))
        return perms

    def is_allowed(self, user_id_or_params, route: str, param_name: str = "user_id") -> bool:
        """
        Check if a user has permission to access a specific route
        Args:
            user_id_or_params: user_id (str) or params dict
            route: The name of the route.
            param_name: The parameter name to use for user identity (default 'user_id')
        Returns:
            True if the user has permission, False otherwise.
        """
        # 支持直接传入 user_id 或 params dict
        if isinstance(user_id_or_params, dict):
            user_id = user_id_or_params.get(param_name, "")
        else:
            user_id = user_id_or_params
        route_perms = self.get_route_permissions(route)
        user_perms  = self.get_user_permissions(user_id)
        if not route_perms:
            return True
        return bool(route_perms & user_perms)

    def who_can_access(self, route: str) -> List[str]:
        """
        Return user_ids who can access the route
        Args:
            route: The name of the route.
        Returns:    
            A list of user IDs who have permission to access the route.
        """
        allowed = []
        for user_id in self._users:
            if self.is_allowed(user_id, route):
                allowed.append(user_id)
        return allowed

    def routes_for_user(self, user_id: str) -> List[str]:
        """Return all routes accessible by user"""
        return [route for route in self._route_permissions if self.is_allowed(user_id, route)]

    #Batch
    def batch_assign_roles(self, user_roles: Dict[str, List[str]]):
        """
        Assign multiple roles to users in batch
        Args:
            user_roles: Dictionary mapping user IDs to lists of roles.
        Returns:
            None
        """
        for user_id, roles in user_roles.items():
            self.set_user_roles(user_id, roles)

    def batch_set_route_permissions(self, route_perms: Dict[str, List[str]]):
        """
        Set permissions for multiple routes in batch
        Args:
            route_perms: Dictionary mapping route names to lists of permissions.
        Returns:
            None
        """
        for route, perms in route_perms.items():
            self.set_route_permissions(route, perms)

    # Event Hooks-
    def add_event_hook(self, event: str, func: Callable[..., Any]):
        """
        Add an event hook for a specific event
        Args:
            event: The name of the event to hook into.
            func: The function to call when the event is triggered.
        Returns:
            None
        """
        self._event_hooks.setdefault(event, []).append(func)

    def _trigger_event(self, event: str, **kwargs):
        for func in self._event_hooks.get(event, []):
            try:
                func(**kwargs)
            except Exception:
                pass

    #Clear/Reset
    def clear(self):
        self._roles.clear()
        self._role_parents.clear()
        self._users.clear()
        self._route_permissions.clear()
        self._event_hooks.clear()

# Global RBAC manager instance
rbac_manager = RBACManager()
