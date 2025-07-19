"""
Navix Data Container Types - Type definitions for IDE support
"""

from typing import TypeVar, Generic, Any, Optional, Dict, List
from abc import ABC, abstractmethod

T = TypeVar('T')

class DataReference(Generic[T]):
    """
    Type-safe data reference for IDE completion
    This class provides a way to define typed references to data properties
    that can be used in data containers.
    """
    
    def __init__(self, route_key: str, property_name: str, data_type: type = Any):
        self._route_key = route_key
        self._property_name = property_name
        self._data_type = data_type
    
    def get(self) -> Optional[T]:
        """
        Get typed value
        Returns:
            Typed value from the data container
        """
        from .core import container_manager
        container = container_manager.get_container(self._route_key)
        return container.get_data(self._property_name)
    
    def set(self, value: T):
        """
        Set typed value
        Args:
            value: Value to set in the data container
        """
        from .core import container_manager
        container = container_manager.get_container(self._route_key)
        container.set_data(self._property_name, value)
    
    @property
    def value(self) -> Optional[T]:
        """Property-style access"""
        return self.get()
    
    @value.setter
    def value(self, val: T):
        """Property-style setting"""
        self.set(val)

# Pre-defined typed references for common data types
StringRef = DataReference[str]
IntRef    = DataReference[int]
ListRef   = DataReference[List[Any]]
DictRef   = DataReference[Dict[str, Any]]
