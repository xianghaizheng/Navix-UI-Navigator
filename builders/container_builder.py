"""
Navix Container Builder - Fluent API for data container configuration
"""

import logging
from typing import Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .app_builder import NavixAppBuilder

logger = logging.getLogger(__name__)

class ContainerBuilder:
    """
    Fluent builder for data container configuration
    
    Example:
        .containers()
            .preload_modules(['core', 'asset', 'data'])
            .global_data({'app_version': '1.0.0', 'theme': 'dark'})
            .auto_cleanup(True)
            .status_monitoring(True)
    """
    
    def __init__(self):
        self._parent: 'NavixAppBuilder' = None
        self._preload_modules = []
        self._global_data = {}
        self._auto_cleanup = False
        self._status_monitoring = False
        self._container_hooks = []
    
    def preload_modules(self, modules: List[str]) -> 'ContainerBuilder':
        """
        Preload container modules
        Args:
            modules: List of module names to preload
        Returns:
            self
        """
        self._preload_modules.extend(modules)
        return self
    
    def global_data(self, data: Dict[str, Any]) -> 'ContainerBuilder':
        """
        Set global shared data
        Args:
            data: Dictionary of global data to set
        Returns:
            self
        """
        self._global_data.update(data)
        return self
    
    def auto_cleanup(self, enabled: bool = True) -> 'ContainerBuilder':
        """
        Enable automatic cleanup of orphaned containers
        Args:
            enabled: Whether to enable auto cleanup
        Returns:
            self
        """
        self._auto_cleanup = enabled
        return self
    
    def status_monitoring(self, enabled: bool = True) -> 'ContainerBuilder':
        """
        Enable container status monitoring
        Args:
            enabled: Whether to enable status monitoring
        Returns:
            self
        """
        self._status_monitoring = enabled
        return self
    
    def container_hook(self, hook: callable) -> 'ContainerBuilder':
        """
        Add container lifecycle hook
        Args:
            hook: Callable hook function to add
        Returns:
            self
        """
        self._container_hooks.append(hook)
        return self
    
    # Convenience methods for common global data
    def app_metadata(self, name: str, version: str, author: str = None) -> 'ContainerBuilder':
        """
        Set application metadata
        Args:
            name: Application name
            version: Application version
            author: Application author (optional)
        Returns:
            self
        """
        metadata = {'app_name': name, 'app_version': version}
        if author:
            metadata['app_author'] = author
        return self.global_data(metadata)
    
    def theme_settings(self, theme: str = 'light', custom_settings: Dict[str, Any] = None) -> 'ContainerBuilder':
        """
        Set theme configuration
        Args:
            theme: Theme name (e.g., 'light', 'dark')
            custom_settings: Additional theme settings as a dictionary
        Returns:
            self
        """
        theme_data = {'app_theme': theme}
        if custom_settings:
            theme_data.update(custom_settings)
        return self.global_data(theme_data)
    
    def user_preferences(self, preferences: Dict[str, Any]) -> 'ContainerBuilder':
        """
        Set user preferences
        Args:
            preferences: Dictionary of user preferences
        Returns:
            self
        """
        return self.global_data({'user_preferences': preferences})
    
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
        Apply container configuration to the application
        Args:
            app: The Navix application instance to apply configuration to
        """
        app._container_config = {
            'preload_modules': self._preload_modules,
            'global_data': self._global_data,
            'auto_cleanup': self._auto_cleanup,
            'status_monitoring': self._status_monitoring,
            'container_hooks': self._container_hooks
        }
        
        logger.debug(f"Applied container config: {len(self._preload_modules)} preload modules, {len(self._global_data)} global data items")

# Convenience function
def containers() -> ContainerBuilder:
    """Create standalone container builder"""
    return ContainerBuilder()
