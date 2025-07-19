"""
Navix UI Navigator - Core Interfaces
========================================================
Professional interface definitions for UI routing system
"""

from typing import Protocol, Any, Dict, Optional, Union, List, Callable
from enum import Enum

class IRouteValidator(Protocol):
    """
    Route validation interface
    This interface defines methods for validating routes and parameters
    used in the Navix UI Navigator."""
    def validate_route(self, route: Union[str, Enum]) -> bool: ...
    def validate_params(self, params: Dict[str, Any]) -> bool: ...

class INavigationInterceptor(Protocol):
    """
    Navigation interceptor interface
    This interface defines methods for intercepting navigation requests
    and applying custom logic before allowing or blocking navigation.
    """
    def intercept(self, route: str, params: Dict[str, Any]) -> bool: ...
    def get_priority(self) -> int: ...


class IUILifecycleManager(Protocol):
    """
    UI lifecycle management interface
    This interface defines methods for managing the lifecycle of UI components,
    including creation, display, hiding, and destruction.
    """
    def create_instance(self, ui_class: type, **kwargs) -> Any: ...
    def show_instance(self, instance: Any) -> None: ...
    def hide_instance(self, instance: Any) -> None: ...
    def destroy_instance(self, instance: Any) -> None: ...



class IWidgetWrapper(Protocol):
    """
    Widget wrapper interface for cross-framework compatibility
    This interface defines methods for common widget operations
    across different GUI frameworks.
    """
    def show(self) -> None: ...
    def hide(self) -> None: ...
    def close(self) -> None: ...
    def is_visible(self) -> bool: ...
    def set_parent(self, parent: Any) -> None: ...
    def bring_to_front(self) -> None: ...
    
    @property
    def native_widget(self) -> Any: ...



class IJsonSerializable(Protocol):
    """
    Interface for JSON serializable objects
    This interface defines methods for converting objects to and from JSON format.
    """
    def to_json(self) -> Dict[str, Any]: ...
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'IJsonSerializable': ...
