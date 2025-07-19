"""
Navix Validation Builder - Fluent API for validation configuration
"""
# standard library imports
import logging
from typing import Callable, Any, TYPE_CHECKING

# qxx libraries
if TYPE_CHECKING:
    from .app_builder import NavixAppBuilder

logger = logging.getLogger(__name__)

class ValidationBuilder:
    """
    Fluent builder for validation configuration
    
    Example:
        .validation()
            .patterns(r'^[a-z_]+\.[a-z_]+$')
            .parameters('user_id', lambda x: isinstance(x, str))
            .parameters('admin_level', lambda x: 0 <= x <= 10)
            .security_checker(my_security_function)
            .enable_security(True)
    """
    
    def __init__(self):
        self._parent: 'NavixAppBuilder' = None
        self._route_patterns     = []
        self._parameter_rules    = {}
        self._security_checker   = None
        self._enable_validation  = True
        self._enable_security    = True
        self._security_param_name = "user_id"
    
    def patterns(self, *patterns: str) -> 'ValidationBuilder':
        """
        Add route naming patterns
        Args:
            patterns: Regular expression patterns to match route names
        Returns:
            self
        """
        self._route_patterns.extend(patterns)
        return self
    
    def parameters(self, param_name: str, validator: Callable[[Any], bool]) -> 'ValidationBuilder':
        """
        Add parameter validation rule
        Args:
            param_name: Name of the parameter to validate
            validator: Function that takes a parameter value and returns True if valid, False otherwise
        Returns:
            self
        """
        self._parameter_rules[param_name] = validator
        return self
    
    def security_checker(self, checker: Callable[[str, dict], bool], param_name: str = "user_id") -> 'ValidationBuilder':
        """
        Set custom security checker function
        Args:
            checker: Function(route, params) -> bool
            param_name: The parameter name to use for user identity (default 'user_id')
        Returns:
            self
        """
        self._security_checker = checker
        self._security_param_name = param_name
        return self
    
    def enable_validation(self, enabled: bool = True) -> 'ValidationBuilder':
        """
        Enable/disable validation
        Args:
            enabled: Whether to enable validation
        Returns:
            self
        """
        self._enable_validation = enabled
        return self
    
    def enable_security(self, enabled: bool = True) -> 'ValidationBuilder':
        """
        Enable/disable security validation
        Args:
            enabled: Whether to enable security validation
        Returns:
            self
        """
        self._enable_security = enabled
        return self
    
    # Standard parameter validators (convenience methods)
    def user_id_validation(self) -> 'ValidationBuilder':
        """
        Add standard user ID validation
        Returns:
            ValidationBuilder instance with user ID validation rule applied.
        """
        return self.parameters('user_id', lambda x: isinstance(x, str) and len(x) > 0)
    
    def admin_level_validation(self, min_level: int = 0, max_level: int = 10) -> 'ValidationBuilder':
        """
        Add admin level validation
        Args:
            min_level: Minimum admin level (default 0)
            max_level: Maximum admin level (default 10)
        Returns:
            ValidationBuilder instance with admin level validation rule applied.
        """
        return self.parameters('admin_level', lambda x: isinstance(x, int) and min_level <= x <= max_level)
    
    def asset_id_validation(self) -> 'ValidationBuilder':
        """
        Add asset ID validation
        Returns:
            ValidationBuilder instance with asset ID validation rule applied.
        """
        return self.parameters('asset_id', lambda x: isinstance(x, (int, str)) and str(x).isdigit())
    
    # Return to parent builder
    def end(self) -> 'NavixAppBuilder':
        """
        Return to parent app builder
        Returns:
            The parent NavixAppBuilder instance.
        """
        return self._parent
    
    def _apply_to_app(self, app):
        """
        Apply validation configuration to the application
        Args:
            app: The Navix application instance to apply configuration to
        """ 

        # Apply validation settings to the app
        app.config.update({
            'enable_validation': self._enable_validation,
            'enable_security': self._enable_security
        })
        
        # Store validation config for later application
        app._validation_config = {
            'patterns': self._route_patterns,
            'parameter_rules': self._parameter_rules,
            'security_checker': self._security_checker,
            'security_param_name': self._security_param_name
        }
        
        logger.debug(f"Applied validation config: {len(self._route_patterns)} patterns, {len(self._parameter_rules)} parameter rules")

# Convenience function
def validation() -> ValidationBuilder:
    """Create standalone validation builder"""
    return ValidationBuilder()
