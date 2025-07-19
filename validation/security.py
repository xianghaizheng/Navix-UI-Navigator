"""
Navix UI Navigator - Validation Module
========================================================
Professional validation system for routes and parameters
"""
# standard library imports
import re
from typing import Dict, Any, List, Pattern, Callable, Optional
import logging

# qxx libraries
from ..security.rbac import rbac_manager

logger = logging.getLogger(__name__)

class SecurityValidator:
    """
    Security-focused validation for enterprise environments
    Provides a comprehensive validation system for routes and parameters"""
    
    def __init__(self):
        self._allowed_modules: set = set()
        self._blocked_patterns: List[Pattern] = []
        self._permission_checker: Optional[Callable] = None
    
    def set_allowed_modules(self, modules: List[str]):
        """
        Set whitelist of allowed modules
        Args:
            modules: List of module names that are allowed
        Returns:
            None
        """
        self._allowed_modules.update(modules)
    
    def add_blocked_pattern(self, pattern: str):
        """
        Add blocked route pattern for security
        Args:
            pattern: Regular expression pattern to block
        """
        self._blocked_patterns.append(re.compile(pattern))
    
    def set_permission_checker(self, checker: Callable[[str], bool]):
        """
        Set custom permission checker
        Args:
            checker: Function that takes a route and returns True if allowed, False otherwise
        Returns:
            None
        """
        self._permission_checker = checker

    def set_param_names(self, param_names: List[str]):
        """
        Set the parameter name to use for user identity.
        """
        self._security_param_names = param_names


    def validate_security(self, route: str, params: dict, user_context: Dict[str, Any] = None) -> bool:
        """
        Validate route access from security perspective
        Args:
            route: The route to validate
            user_context: Optional user context containing user ID and roles
        Returns:
            True if route is allowed, False otherwise
        """
        # Check blocked patterns
        for pattern in self._blocked_patterns:
            if pattern.match(route):
                logger.warning(f"Security: Blocked route pattern matched: {route}")
                return False
        
        # Check module whitelist
        if self._allowed_modules:
            module = route.split('.')[0]
            if module not in self._allowed_modules:
                logger.warning(f"Security: Module not in whitelist: {module}")
                return False
        
        # Check custom permissions
        if self._permission_checker:
            # If custom checker is set, RBAC is skipped
            return self._permission_checker(route, params, self._security_param_names)
        
        # RBAC only runs if no custom checker is set
        if user_context and 'user_id' in user_context:
            user_id = user_context['user_id']  # <-- This is a custom string, typically your application's user identifier.
            if not rbac_manager.is_allowed(user_id, route):
                logger.warning(f"Security: RBAC denied user {user_id} for route {route}")
                return False
        
        return True
    
# Global validator instances
security_validator = SecurityValidator()
