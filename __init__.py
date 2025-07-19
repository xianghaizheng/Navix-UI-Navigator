"""
Navix UI Navigator - Professional UI Routing & Navigation System
========================================================
PyQt/PySide UI routing and navigation system, providing an elegant UI management solution.
Author : Xiang Haizheng
Email  : 85438256@qq.com
License: MIT License
"""

__version__     = "1.0.0"
__author__      = "haizheng xiang"
__email__       = "85438256@qq.com"
__title__       = 'Navix UI Navigator'
__description__ = 'Professional UI Routing & Navigation System for PyQt/PySide Applications'
__url__         = 'https://github.com/xianghaizheng/Navix'
__license__     = 'MIT License'
__status__      = 'Production'
__maintainer__  = 'RedWishkers Vfx Studio'



# Core navigation components
from .routing import (
    RouteCatalog,
    RouteSource,
    navigate,
    setup_navigator,
    RouteManager
)

from .navigation import UIVoyager

# Professional interfaces
from .interfaces import (
    IRouteValidator,
    INavigationInterceptor,
    IUILifecycleManager,
    IRouteRegistry,
    IGUIFrameworkAdapter,
    IWidgetWrapper
)

# Validation system
from .validation import (
    RouteValidator,
    SecurityValidator,
    route_validator,
    security_validator
)

# Exception system
from .exceptions import (
    NavixError,
    NavigationError,
    RouteError,
    RouteNotFoundError,
    RouteConflictError,
    FrameworkError,
    ValidationError
)

# Data container system
from .data_container import (
    RouteDataContainer,
    ModuleDataContainer,
    DataContainerManager,
    ContainerStatus,
    ContainerData,
    container_manager,
    container_property,
    auto_container,
    DataReference
)

# Builder system for elegant configuration
from .builders import (
    NavixAppBuilder,
    Navix_app,
    NavigationBuilder,
    ValidationBuilder, 
    InterceptorBuilder,
    ContainerBuilder,
    navigation,
    validation,
    interceptors,
    containers
)

# RBAC manager
from .security.rbac import (
    rbac_manager
)



# Convenience functions for direct instance access
def get_ui_class(route):
    """Get UI class for a route"""
    return RouteCatalog.get_ui_class(route)

def create_ui_instance(route, **params):
    """Create UI instance directly without navigation"""
    return RouteCatalog.create_ui_instance(route, **params)

__all__ = [
    # Core components
    'RouteCatalog', 
    'UIVoyager',
    'RouteSource', 
    'RouteManager',
    
    # Navigation utilities
    'navigate', 
    'setup_navigator',
    
    # Professional interfaces
    'IRouteValidator',
    'INavigationInterceptor', 
    'IUILifecycleManager',
    'IRouteRegistry',
    'IGUIFrameworkAdapter',
    'IWidgetWrapper',
    
    # Validation system
    'RouteValidator',
    'SecurityValidator',
    'route_validator',
    'security_validator',
    
    # Exception system
    'NavixError',
    'NavigationError',
    'RouteError',
    'RouteNotFoundError',
    'RouteConflictError',
    'FrameworkError',
    'ValidationError',
    
    # Direct instance access
    'get_ui_class',
    'create_ui_instance',

    # Data container system
    'RouteDataContainer',
    'ModuleDataContainer',
    'DataContainerManager', 
    'ContainerStatus',
    'ContainerData',
    'container_manager',
    'container_property',
    'auto_container',
    'DataReference',

    # Builder system
    'NavixAppBuilder',
    'Navix_app',
    'NavigationBuilder',
    'ValidationBuilder',
    'InterceptorBuilder', 
    'ContainerBuilder',
    'navigation',
    'validation',
    'interceptors',
    'containers',

    #tool
    'rbac_manager',
]


