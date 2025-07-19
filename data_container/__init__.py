"""
Navix Data Container - Intelligent UI Data Management System
========================================================
Provides structured, queryable, and IDE-friendly data containers for UI communication
"""

from .core import (
    RouteDataContainer,
    ModuleDataContainer,
    DataContainerManager,
    ContainerStatus,
    ContainerData,
    container_manager
)
from .decorators import (
    container_property,
    auto_container
)
from .types import (
    DataReference
)

__all__ = [
    'RouteDataContainer', 
    'ModuleDataContainer',
    'DataContainerManager',
    'ContainerStatus',
    'ContainerData',
    'container_manager',
    'container_property',
    'auto_container',
    'DataReference',
    'save',
    'load',
]

# cancled methods for future use
# save   = container_manager.save
# load   = container_manager.load
