"""
Navix UI Navigator - Validation Module
========================================================
Professional validation system for routes and parameters
"""
# standard library imports
import re
from typing import Dict, Any, Union, List, Pattern, Callable, Optional
from enum import Enum
import logging

# qxx libraries
from ..interfaces import IRouteValidator

logger = logging.getLogger(__name__)

class RouteValidationError(Exception):
    """Route validation specific exception"""
    pass

class ParameterValidationError(Exception):
    """Parameter validation specific exception"""
    pass

class RouteValidator(IRouteValidator):
    """Professional route validator with configurable rules"""
    
    def __init__(self):
        self._route_patterns: List[Pattern] = []
        self._parameter_rules: Dict[str, Callable] = {}
        self._reserved_routes: set = set()
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """
        Setup default validation rules
        """
        # Route naming convention: module.component
        self.add_route_pattern(r'^[a-z_]+\.[a-z_]+$')
        
        # Reserved system routes
        self._reserved_routes.update([
            'system.error',
            'system.loading',
            'system.unauthorized'
        ])
    
    def add_route_pattern(self, pattern: str):
        """
        Add route naming pattern
        Args:
            pattern: Regular expression pattern for route names
        """
        self._route_patterns.append(re.compile(pattern))
    
    def add_parameter_rule(self, param_name: str, validator: Callable[[Any], bool]):
        """
        Add parameter validation rule
        Args:
            param_name: Name of the parameter to validate
            validator: Function that takes a parameter value and returns True if valid, False otherwise
        Returns:
            None
        """
        self._parameter_rules[param_name] = validator
    
    def validate_route(self, route: Union[str, Enum]) -> bool:
        """
        Validate route format and availability
        Args:
            route: Route name or Enum member
        Returns:
            True if route is valid, raises RouteValidationError if not
        """
        route_str = route.value if isinstance(route, Enum) else route
        
        # Check if reserved
        if route_str in self._reserved_routes:
            raise RouteValidationError(f"Route '{route_str}' is reserved for system use")
        
        # Check naming patterns
        if not any(pattern.match(route_str) for pattern in self._route_patterns):
            raise RouteValidationError(f"Route '{route_str}' doesn't match naming conventions")
        
        return True
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        Validate route parameters
        Args:
            params: Dictionary of parameter names and values
        Returns:
            True if all parameters are valid, raises ParameterValidationError if not
        """
        for param_name, param_value in params.items():
            if param_name in self._parameter_rules:
                validator = self._parameter_rules[param_name]
                if not validator(param_value):
                    raise ParameterValidationError(
                        f"Parameter '{param_name}' validation failed for value: {param_value}"
                    )
        return True
    
    
route_validator    = RouteValidator()

class SecurityValidator:
    """
    Professional security validator for route-level permission checks
    """
    def __init__(self):
        self._permission_checker: Optional[Callable] = None
        self._security_param_name: str = "user_id"

    def set_permission_checker(self, checker: Callable):
        """
        Set custom permission checker function
        Args:
            checker: Function(route, params, param_name) -> bool
        """
        self._permission_checker = checker

    def set_param_name(self, param_name: str):
        """
        Set the parameter name to use for user identity.
        """
        self._security_param_name = param_name

    def validate_security(self, route: str, params: dict) -> bool:
        """
        Validate security for a route and parameters
        Args:
            route: Route name
            params: Parameters dict
        Returns:
            True if allowed, False otherwise
        """
        if not self._permission_checker:
            return True
        # 关键：传递参数名给安全检查函数
        return self._permission_checker(route, params, self._security_param_name)

security_validator = SecurityValidator()