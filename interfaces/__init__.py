"""
Navix Interfaces Module
========================================================
Professional interfaces for Navix application components
"""
from .protocols import (
    IRouteValidator, 
    INavigationInterceptor, 
    IUILifecycleManager, 
    IWidgetWrapper,
    IJsonSerializable
)

from .abc_interfaces import (
    IRouteRegistry, 
    IGUIFrameworkAdapter
)

__all__ = [
    # Protocols
    'IRouteValidator',  
    'INavigationInterceptor', 
    'IUILifecycleManager',  
    'IWidgetWrapper',
    'IJsonSerializable',

    # Abc interfaces
    'IRouteRegistry',
    'IGUIFrameworkAdapter'
]

