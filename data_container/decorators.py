"""
Navix Data Container Decorators - For IDE completion and automatic setup
"""
# standard library imports
import logging
from typing import Any, Type
from functools import wraps

logger = logging.getLogger(__name__)


def container_property(data_type: Type = str, default: Any = None, description: str = ""):
    """
    Decorator to define container properties for IDE completion
    
    Args:
        data_type: Type hint for the property
        default: Default value
        description: Property description
    Returns:
        Decorated function with metadata for container property
    """
    def decorator(func):
        func._container_property = True  
        func._data_type = data_type
        func._default = default
        func._description = description
        return func
    return decorator

def auto_container(route_enum_or_key):
    """
    Class decorator to automatically setup container properties
    
    Args:
        route_enum_or_key: Route enum or string key
    """
    def decorator(ui_class: Type):
        # Analyze class for container properties
        container_properties = {}
        
        for attr_name in dir(ui_class):
            attr = getattr(ui_class, attr_name)
            if hasattr(attr, '_container_property'):
                container_properties[attr_name] = {
                    'type': attr._data_type,
                    'default': attr._default,
                    'description': attr._description
                }
        
        # Store container property metadata
        ui_class._container_properties = container_properties
        ui_class._container_route = route_enum_or_key
        
        logger.debug(f"Auto-container setup for {ui_class.__name__}: {list(container_properties.keys())}")
        
        return ui_class
    return decorator

class ContainerPropertyDescriptor:
    """
    Property descriptor for container data access
    This descriptor allows for dynamic access to container data based on route keys.
    It provides a way to define properties that can be accessed like attributes,
    """
    
    def __init__(self, route_key: str, property_name: str, data_type: Type = Any, default: Any = None):
        self.route_key = route_key
        self.property_name = property_name
        self.data_type = data_type
        self.default = default
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        from .core import container_manager
        
        container = container_manager.get_container(self.route_key)
        return container.get_data(self.property_name, self.default)
    
    def __set__(self, obj, value):
        from .core import container_manager
        container = container_manager.get_container(self.route_key)
        container.set_data(self.property_name, value)
