"""
Navix Navigation Builder - Fluent API for navigation configuration
"""
# standard library imports
import logging
from typing import TYPE_CHECKING

# qxx libraries
if TYPE_CHECKING:
    from .app_builder import NavixAppBuilder

logger = logging.getLogger(__name__)

class NavigationBuilder:
    """
    Fluent builder for navigation configuration
    
    Example:
        .navigation()
            .max_history(100)
            .auto_discovery(['myapp.ui_parts'])
            .default_parent_mode('dialog')
    """
    
    def __init__(self):
        self._parent: 'NavixAppBuilder' = None
        self._max_history             = 50
        self._auto_discovery_packages = []
        self._default_parent_mode     = 'window'
        self._navigation_hooks        = []
    
    def max_history(self, count: int) -> 'NavigationBuilder':
        """
        Set maximum navigation history size
        Args:
            count: Maximum number of history entries to keep
        Returns:
            self
        """
        self._max_history = count
        return self
    
    def auto_discovery(self, packages: list) -> 'NavigationBuilder':
        """
        Enable auto-discovery of UI modules
        Args:
            packages: List of package names to scan for UI components
        Returns:
            self
        """
        self._auto_discovery_packages.extend(packages)
        return self
    
    def default_parent_mode(self, mode: str) -> 'NavigationBuilder':
        """
        Set default parent mode (window, dialog, modal)
        Args:
            mode: Parent mode for navigation (e.g., 'window', 'dialog', 'modal')
        Returns:
            self
        """
        self._default_parent_mode = mode
        return self
    
    def navigation_hook(self, hook: callable) -> 'NavigationBuilder':
        """
        Add navigation lifecycle hook
        Args:
            hook: Callable function to execute during navigation lifecycle
        Returns:
            self
        """
        self._navigation_hooks.append(hook)
        return self
    
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
        Apply navigation configuration to the application
        Args:
            app: The Navix application instance to apply configuration to
        """
        app._navigation_config = {
            'max_history': self._max_history,
            'auto_discovery_packages': self._auto_discovery_packages,
            'default_parent_mode': self._default_parent_mode,
            'navigation_hooks': self._navigation_hooks
        }
        
        logger.debug(f"Applied navigation config: max_history={self._max_history}")

# Convenience function
def navigation() -> NavigationBuilder:
    """Create standalone navigation builder"""
    return NavigationBuilder()
