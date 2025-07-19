# stand libraries
from typing import Dict, Optional, Type, Any, Union, List, Callable
from enum import Enum
import importlib
import logging

# Navix libraries 
from   .sources import RouteSource
from   ..interfaces import IRouteRegistry
from   ..exceptions import RouteConflictError
logger = logging.getLogger(__name__)



#=========================================================#
class RouteCatalog(IRouteRegistry):
    """
    route directory registry - provides a centralized registry for route navigators
    Provides a centralized registry for route navigators
    """
    _routes       : Dict[str, Dict[str, Any]] = {}
    _route_enum   : Optional[Type[Enum]] = None
    _interceptors : List[Callable] = []
    
    @classmethod
    def create_enum_from_source(cls, source_type: str, source_path: str, 
                               enum_name: str = "NavigationRoutes", **kwargs) -> Type[Enum]:
        """create an Enum from a route source
        Args:
            source_type: type of the source (json, csv, yaml, module)
            source_path: path to the source file or module
            enum_name: name of the resulting Enum class
        Returns:
            A new Enum class containing all routes from the provided source.
        Example:
            RouteCatalog.create_enum_from_source('json', 'routes.json', enum_name='MyRoutes')
        """
        source_map = {
            'json'  : RouteSource.from_json,
            'csv'   : RouteSource.from_csv,
            'yaml'  : RouteSource.from_yaml,
            'module': RouteSource.from_module
        }
        
        if source_type not in source_map:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        route_data = source_map[source_type](source_path, **kwargs)
        return Enum(enum_name, route_data)
    
    @classmethod
    def setup(cls, route_enum: Type[Enum]):
        """setup route enum
        Args:
            route_enum: Enum class containing route definitions
        """
        cls._route_enum = route_enum
        logger.info(f"Navigator initialized with {len(route_enum)} routes")
    
    @classmethod
    def register_navigator(cls, route: Union[str, Enum], ui_class: Type, 
                          lazy: bool = True, singleton: bool = False, **meta):
        """
        register a new navigator - Now includes validation
        Args:
            route: route name or Enum member
            ui_class: class of the UI component to navigate to
            lazy: whether to create the UI instance lazily
            singleton: whether to enforce a single instance for this route
            meta: additional metadata for the navigator
        """
        route_key = route.value if isinstance(route, Enum) else route
        
        # check if route is already registered
        if route_key in cls._routes:
            existing_class = cls._routes[route_key]['ui_class']
            raise RouteConflictError(
                f"Route '{route_key}' already registered with {existing_class.__name__}"
            )
        
        cls._routes[route_key] = {
            'ui_class': ui_class,
            'module': ui_class.__module__,
            'lazy': lazy,
            'singleton': singleton,
            'meta': meta
        }
        logger.debug(f"Registered navigator: {route_key}")
    
    @classmethod
    def get_navigator_info(cls, route: Union[str, Enum]) -> Optional[Dict[str, Any]]:
        """
        get navigator information for a given route
        Args:
            route: route name or Enum member
        Returns:
            A dictionary containing navigator information, or None if not found.
        """
        route_key = route.value if isinstance(route, Enum) else route
        info = cls._routes.get(route_key)
        if not info:
            logger.warning(f"Navigator not found for route: {route_key}")
        return info
    
    def register_route(self, route: str, handler: type, **meta) -> None:
        """
        register a UI class as a navigator - now includes validation
        Args:
            route: route name or Enum member
            handler: class of the UI component to navigate to
            meta: additional metadata for the navigator
        Returns:
            None
        """
        self.register_navigator(route, handler, **meta)
    
    def get_route_info(self, route: str) -> Optional[Dict[str, Any]]:
        """get navigator information for a given route
        Args:
            route: route name or Enum member
        Returns:
            A dictionary containing navigator information, or None if not found.
        """
        return self.get_navigator_info(route)
    
    @classmethod
    def list_routes(cls) -> List[str]:
        """
        list all registered routes
        Returns:
            A list of route names.
        """
        return list(cls._routes.keys())
    
    @classmethod
    def add_interceptor(cls, interceptor: Callable):
        """
        add a route interceptor - now supports both function and class-based interceptors
        Args:
            interceptor: a callable that implements INavigationInterceptor or a normal function
        """
        # if it's an object implementing INavigationInterceptor interface
        if hasattr(interceptor, 'intercept') and hasattr(interceptor, 'get_priority'):
            # insert by priority
            priority = interceptor.get_priority()
            inserted = False
            for i, existing in enumerate(cls._interceptors):
                if (hasattr(existing, 'get_priority') and 
                    existing.get_priority() < priority):
                    cls._interceptors.insert(i, interceptor)
                    inserted = True
                    break
            if not inserted:
                cls._interceptors.append(interceptor)
        else:
            # normal function interceptor
            cls._interceptors.append(interceptor)
        
        logger.debug(f"Added interceptor: {interceptor}")
    
    @classmethod
    def get_interceptors(cls) -> List[Callable]:
        """
        get all registered interceptors
        Returns:
            A list of interceptor callables.
        """
        return cls._interceptors.copy()
    
    @classmethod
    def list_navigators(cls) -> Dict[str, Dict[str, Any]]:
        """
        list all registered navigators
        Returns:
            A dictionary mapping route names to their navigator information.
        """
        return cls._routes.copy()
    
    @classmethod
    def discover_navigators(cls, base_package: str, pattern: str = "*.py"):
        """
        automatically discover navigators in a package
        Args:
            base_package: the base package to search for navigators
            pattern: file pattern to match (default is "*.py")
        """
        try:
            import pkgutil
            package = importlib.import_module(base_package)
            
            for finder, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
                try:
                    importlib.import_module(name)
                except Exception as e:
                    logger.warning(f"Failed to discover navigator in {name}: {e}")
        except Exception as e:
            logger.error(f"Navigator discovery failed: {e}")
    
    @classmethod
    def get_ui_class(cls, route: Union[str, Enum]) -> Optional[Type]:
        """
        Get UI class directly from catalog
        Args:
            route: route name or Enum member
        Returns:
            UI class or None if route not found
        """
        navigator_info = cls.get_navigator_info(route)
        return navigator_info['ui_class'] if navigator_info else None
    
    @classmethod
    def create_ui_instance(cls, route: Union[str, Enum], **params) -> Optional[Any]:
        """
        Create UI instance directly from catalog (no fleet management)
        Args:
            route: route name or Enum member
            **params: parameters to pass to UI constructor
        Returns:
            UI instance or None if route not found
        """
        navigator_info = cls.get_navigator_info(route)
        if not navigator_info:
            return None
        
        try:
            ui_class = navigator_info['ui_class']
            meta = navigator_info.get('meta', {})
            creation_params = {**meta, **params}
            
            return ui_class(**creation_params)
        except Exception as e:
            logger.error(f"Failed to create instance for route {route}: {e}")
            return None