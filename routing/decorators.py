# stand libraries
from typing import  Union, Type
from enum import Enum
import logging
logger = logging.getLogger(__name__)

# Navix libraries
from .catalog     import RouteCatalog
from ..exceptions import RouteConflictError

def navigate(route: Union[str, Enum], **meta):
    """
    decorator to register a UI class as a navigator - Now includes validation
    Args:
        route: route name or Enum member
        meta: additional metadata for the navigator
    Returns:
        A decorator that registers the UI class as a navigator.
    """
    def decorator(ui_class: Type):
        try:
            RouteCatalog.register_navigator(route, ui_class, **meta)
            # Auto-register 
            # with data container system
            from ..data_container import container_manager 
            container_manager.register_route(route)
            return ui_class
        except RouteConflictError as e:
            logger.error(f"Failed to register navigator: {e}")
            raise
    return decorator

def setup_navigator(route_enum: Type[Enum]):
    """
    setup route enum
    Args:
        route_enum: Enum class containing route definitions
    Returns:
        The RouteCatalog after setup.
    """
    # Registers all routes from the Enum into the central registry.
    RouteCatalog.setup(route_enum)
    return RouteCatalog