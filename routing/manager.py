"""
Navix  UI Navigator - Professional UI Routing & Navigation System
========================================================
Navix route management core module
Provides an enterprise-level modular route management solution:
1 modular route architecture
2 automatic route discovery and merging
3 team collaboration friendly
4 full IDE support
"""
from enum import Enum
from typing import Type, Dict, Any, List, Optional
import importlib
import pkgutil
import logging

logger = logging.getLogger(__name__)


# this is the core route manager that provides a unified interface for managing routes across the application.
# it supports modular route definitions, automatic discovery of route modules, and merging of routes into a unified structure.
class RouteManager:
    """
    route manager for Navix applications
    Provides a unified interface for managing routes across the application.
    Supports modular route definitions, automatic discovery of route modules, and merging of routes into a unified
    structure.
    """
    
    # core routes for the application
    _merged_routes:   Optional[Type[Enum]] = None
    _route_modules:   Dict[str, Type[Enum]] = {}
    _discovery_paths: List[str] = []
    
    @classmethod
    def register_route_module(cls, name: str, route_enum: Type[Enum]):
        """
        register a route module
        Args:
            name:         module name
            route_enum:   route enum class
        Returns:            None
        Raises:             ValueError if the route name already exists in the module
        Example:
            RouteManager.register_route_module("admin_routes", AdminRoutes)
        """
        cls._route_modules[name] = route_enum
        logger.info(f"Registered route module: {name} with {len(route_enum)} routes")
    
    @classmethod
    def discover_routes(cls, base_package: str, pattern: str = "*_routes") -> Dict[str, Type[Enum]]:
        """
        find and register route modules in the specified package
        Args:
            base_package:  base package path, e.g. 'myapp.routes'
            pattern:       route module file name pattern
        Returns:
            A dictionary mapping module names to their route enums.
        Example:
            RouteManager.discover_routes("myapp.routes", pattern="*_routes")
        """
        discovered_routes = {}
        
        try:
            package   = importlib.import_module(base_package)
            base_path = package.__path__[0] if hasattr(package, '__path__') else None
            
            if base_path:
                # use pkgutil to traverse the specified path for modules
                for finder, name, ispkg in pkgutil.iter_modules([base_path]):
                    if pattern.replace('*', '') in name:
                        cls._push_discovery_path(discovered_routes,base_package, name)

        except ImportError as e:
            logger.error(f"Failed to import base package {base_package}: {e}")
        
        return discovered_routes
    
    def _push_discovery_path( cls, discovered_routes: Dict[str, Type[Enum]], base_package: str, name: str):
        """
        internal method to push discovered route module into the discovery paths
        """
        try:
            module_name = f"{base_package}.{name}"
            module = importlib.import_module(module_name)
                            
            # for each attribute in the module, check if it's a route enum
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, Enum) and 
                    attr != Enum and
                    attr_name.endswith('Routes')):
                    discovered_routes[name] = attr
                    #logger.debug(f"Discovered route enum: {attr_name} in {module_name}")
                   
        except ImportError as e:
            logger.warning(f"Failed to import route module {name}: {e}")

    @classmethod
    def merge_routes(cls, *route_enums: Type[Enum], name: str = "MergedRoutes") -> Type[Enum]:
        """
        merge multiple route enums into a single enum
        Args:
            *route_enums: route enums to merge
            name: name of the merged enum
        Returns:
            A new Enum class containing all routes from the provided enums.
        Raises:
            ValueError if a route name conflict occurs
        Example:
            merged_routes = RouteManager.merge_routes(CoreRoutes, AssetRoutes, name="AppRoutes")
        """

        merged_routes = {}
        source_info   = {}
        for route_enum in route_enums:
            enum_name = route_enum.__name__
            for route in route_enum:
                if route.name in merged_routes:
                    existing_source = source_info[route.name]
                    raise ValueError(
                        f"Route conflict: '{route.name}' defined in both "
                        f"'{existing_source}' and '{enum_name}'"
                    )
                merged_routes[route.name] = route.value
                source_info[route.name]   = enum_name
        
        logger.info(f"Merged {len(merged_routes)} routes from {len(route_enums)} modules")
        return Enum(name, merged_routes)
    
    @classmethod
    def build_unified_routes(cls, core_routes: Type[Enum], 
                           discovery_packages: List[str] = None,
                           name: str = "UnifiedRoutes") -> Type[Enum]:
        """
        Build a unified route enum from core routes and discovered modules
        Args:
            core_routes: the core route enum to use as the base
            discovery_packages: a list of packages to scan for additional route modules
            name: the name of the unified route enum
        Returns:
            A new Enum class containing all routes from the core routes and discovered modules.
        Raises:
            ValueError if a route name conflict occurs
        Example:
            unified_routes = RouteManager.build_unified_routes(CoreRoutes, discovery_packages=["myapp.routes"], name="AppRoutes")
        """
        all_route_enums = [core_routes]
        
        # automatically discover modules routes
        if discovery_packages:
            for package in discovery_packages:
                discovered = cls.discover_routes(package)
                all_route_enums.extend(discovered.values())
        
        # add registered route modules
        all_route_enums.extend(cls._route_modules.values())
        
        cls._merged_routes = cls.merge_routes(*all_route_enums, name=name)
        return cls._merged_routes
    
    @classmethod
    def get_unified_routes(cls) -> Optional[Type[Enum]]:
        """
        Get the currently merged unified routes enum
        Returns:
            The merged routes enum if available, otherwise None.
        Example:
            unified_routes = RouteManager.get_unified_routes()
        """
        return cls._merged_routes
    
    @classmethod
    def get_route_info(cls, route_name: str) -> Dict[str, Any]:
        """
        Get information about a specific route by its name
        Args:
            route_name: the name of the route to get information for
        Returns:
            A dictionary containing the route's name, value, and enum class.
        Example:
            route_info = RouteManager.get_route_info("MAIN_WINDOW")
        """
        if not cls._merged_routes:
            return {}
        
        try:
            route = getattr(cls._merged_routes, route_name)
            return {
                'name' : route.name,
                'value': route.value,
                'enum_class': cls._merged_routes.__name__
            }
        except AttributeError:
            return {}

class RouteModule:
    """
    this class represents a route module that can be registered with the RouteManager.
    It provides a standard way to define and register route enums for different application modules.
    """
    
    def __init__(self, name: str, description: str, maintainer: str):
        self.name = name
        self.description = description
        self.maintainer = maintainer
        self.routes: Type[Enum] = None
    
    def define_routes(self, routes: Type[Enum]):
        """
        use this method to define the routes for this module
        Args:
            routes: Type[Enum] - the route enum class to use for this module
        Returns:            None
        Raises:             ValueError if the route name already exists in the module
        Example:
            module = RouteModule("admin_routes", "Admin related routes", "admin_team")
            module.define_routes(AdminRoutes)
        """
        self.routes = routes
        RouteManager.register_route_module(self.name, routes)
        return self
    
    def __repr__(self):
        """
        String representation of the route module
        """
        route_count = len(self.routes) if self.routes else 0
        return f"RouteModule(name='{self.name}', routes={route_count}, maintainer='{self.maintainer}')"

def create_route_builder(core_routes: Type[Enum]):
    """
    create a route builder factory function
    Args:
        core_routes: the core route enum to use as the base
    Returns:
        A function that builds unified routes from the core routes and discovered modules.
    """
    
    def build_routes(*discovery_packages: str, name: str = "AppRoutes") -> Type[Enum]:
        """
        Build application routes from core routes and discovered modules
        Args:
            *discovery_packages: a list of packages to scan for additional route modules
            name: the name of the unified route enum
        Returns:
            A new Enum class containing all routes from the core routes and discovered modules.
        Raises:
            ValueError if a route name conflict occurs
        Example:
            unified_routes = create_route_builder(CoreRoutes)(discovery_packages=["myapp.routes"], name="AppRoutes")
        """
        return RouteManager.build_unified_routes(
            core_routes=core_routes,
            discovery_packages=list(discovery_packages),
            name=name
        )
    
    return build_routes
