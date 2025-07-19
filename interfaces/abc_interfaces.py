"""
Navix UI Navigator - Core Interfaces
========================================================
Professional interface definitions for UI routing system
"""
# standard library imports
from typing import  Any, Dict, Optional, List, TYPE_CHECKING
from abc import ABC, abstractmethod

# qxx libraries
if TYPE_CHECKING:
    from .protocols import IWidgetWrapper
    
class IRouteRegistry(ABC):
    """
    Abstract base class for route registry
    This interface defines methods for registering, retrieving, and managing routes
    in the Navix UI Navigator.
    """
    
    @abstractmethod
    def register_route(self, route: str, handler: type, **meta) -> None: ...
    
    @abstractmethod
    def get_route_info(self, route: str) -> Optional[Dict[str, Any]]: ...
    
    @abstractmethod
    def list_routes(self) -> List[str]: ...

class IGUIFrameworkAdapter(ABC):
    """
    Abstract GUI framework adapter
    This interface defines methods for detecting the GUI framework,
    creating widget wrappers, and checking widget compatibility.
    """
    
    @abstractmethod
    def detect_framework(self) -> str: ...
    
    @abstractmethod
    def create_widget_wrapper(self, widget: Any) -> 'IWidgetWrapper': ...
    
    @abstractmethod
    def is_widget_compatible(self, widget: Any) -> bool: ...

