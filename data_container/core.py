"""
Navix Data Container Core - Smart data management for UI components
"""
# standard library imports
import logging
from   typing import Any, Dict, Optional, List,Union
from   enum import Enum
from   dataclasses import dataclass, field
import weakref
import time
import json

logger = logging.getLogger(__name__)

class ContainerStatus(Enum):
    """
    Container lifecycle status
    Represents the current state of a data container.
    - EMPTY: No UI instance, no data
    - PREPARED: No UI instance, has data
    - ACTIVE: UI instance exists, has data
    - ORPHANED: UI instance destroyed, data remains
    """
    EMPTY    = "empty"       
    PREPARED = "prepared"     
    ACTIVE   = "active"       
    ORPHANED = "orphaned"     

@dataclass
class ContainerData:
    """
    Base container data with metadata
    """
    value: Any = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    access_count: int = 0
    ui_instance_ref: Optional[weakref.ReferenceType] = None
    
    def update_value(self, new_value: Any):
        """
        Update value with timestamp
        Args:
            new_value: New value to set
        """
        self.value = new_value
        self.updated_at = time.time()
        self.access_count += 1


class RouteDataContainer:
    """
    Individual route data container with dynamic attribute support
    """
    
    def __init__(self, route_key: str):
        self._route_key = route_key
        self._data: Dict[str, ContainerData] = {}
        self._ui_instance_ref: Optional[weakref.ReferenceType] = None
        self._status = ContainerStatus.EMPTY
    
    @property
    def status(self) -> ContainerStatus:
        """
        Get current container status
        Returns:
            ContainerStatus: Current status of the container
        """
        has_ui   = self._ui_instance_ref and self._ui_instance_ref() is not None
        has_data = bool(self._data)
        
        if not has_data and not has_ui:
            return ContainerStatus.EMPTY
        elif has_data and not has_ui:
            return ContainerStatus.ORPHANED if self._status == ContainerStatus.ACTIVE else ContainerStatus.PREPARED
        elif has_ui and has_data:
            return ContainerStatus.ACTIVE
        else:
            return ContainerStatus.EMPTY
    
    def set_ui_instance(self, instance: Any):
        """
        Set UI instance reference
        Args:
            instance: UI instance to associate with this container
        If instance is None, it clears the reference and updates status accordingly.
        If instance is not None, it updates the reference and sets status to ACTIVE if data exists
        """
        if instance is not None:
            self._ui_instance_ref = weakref.ref(instance)
            if self._data:
                self._status = ContainerStatus.ACTIVE
        else:
            self._ui_instance_ref = None
            if self._data:
                self._status = ContainerStatus.ORPHANED
    
    def set_data(self, key: str, value: Any):
        """
        Set data value
        Args:
            key: Data key to set
            value: Value to associate with the key
        If the key does not exist, it creates a new ContainerData instance.
        It updates the value and associates it with the current UI instance reference.    
        """
        if key not in self._data:
            self._data[key] = ContainerData()
        
        self._data[key].update_value(value)
        self._data[key].ui_instance_ref = self._ui_instance_ref
        
        if self._status == ContainerStatus.EMPTY:
            self._status = ContainerStatus.PREPARED
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Get data value
        Args:
            key: Data key to retrieve
            default: Default value if key does not exist
        Returns:
            The value associated with the key, or default if not found.
        """
        if key in self._data:
            self._data[key].access_count += 1
            return self._data[key].value
        return default
    
    def clear_data(self, key: Optional[str] = None):
        """
        Clear specific data or all data
        Args:
            key: Data key to clear, if None clears all data
        If key is None, it clears all data and updates status to EMPTY.
        If key exists, it removes the key from the data dictionary.
        """
        if key is None:
            self._data.clear()
            if not (self._ui_instance_ref and self._ui_instance_ref()):
                self._status = ContainerStatus.EMPTY
        elif key in self._data:
            del self._data[key]
    
    def list_keys(self) -> list:
        """
        List all data keys
        Returns:
            List of keys in the data container.
        """
        return list(self._data.keys())
    
    def get_metadata(self, key: str) -> Optional[ContainerData]:
        """
        Get complete metadata for a key
        Args:
            key: Data key to retrieve metadata for
        Returns:
            ContainerData: Metadata object containing value, timestamps, access count, and UI instance reference.
        """
        return self._data.get(key)
    
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get data value with explicit method
        Args:
            key: Data key to retrieve
            default: Default value if key does not exist
        Returns:
            The value associated with the key, or default if not found.
        """
        return self.get_data(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set data value with explicit method
        Args:
            key: Data key to set
            value: Value to associate with the key
        """
        self.set_data(key, value)
    
    def update(self, data: Dict[str, Any]):
        """
        Update multiple data values
        Args:
            data: Dictionary of key-value pairs to update
        """
        for key, value in data.items():
            self.set_data(key, value)
    
    def clear(self, key: Optional[str] = None):
        """
        Clear specific data or all data
        Args:
            key: Data key to clear, if None clears all data
        """
        self.clear_data(key)
    
    def keys(self) -> List[str]:
        """Get all data keys"""
        return self.list_keys()
    
    def items(self) -> List[tuple]:
        """
        Get all key-value pairs
        Returns:
            List of tuples containing key and value pairs from the data container.
        """
        return [(key, data.value) for key, data in self._data.items()]
 
    def __getattr__(self, name: str) -> Any:
        """
        Dynamic attribute access for IDE completion
        """
        return self.get_data(name)
    
    def __setattr__(self, name: str, value: Any):
        """
        Dynamic attribute setting
        """
        if name.startswith('_') or name in ['status']:
            super().__setattr__(name, value)
        else:
            self.set_data(name, value)

    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access"""
        return self.get_data(key)
    
    def __setitem__(self, key: str, value: Any):
        """Dictionary-style setting"""
        self.set_data(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists"""
        return key in self._data





class ModuleDataContainer:
    """
    Module-level container (e.g., core, asset, data)
    This container holds route data containers for a specific module.
    It allows dynamic access to route containers based on module name.      
    """
    
    def __init__(self, module_name: str):
        self._module_name = module_name
        self._routes: Dict[str, RouteDataContainer] = {}
    
    def get_route_container(self, route_key: str) -> RouteDataContainer:
        """
        Get / create route container
        Args:
            route_key: Route key to retrieve or create
        Returns:
            RouteDataContainer: The route data container for the specified key.
        If the route key does not exist, it creates a new RouteDataContainer instance.
        """
        if route_key not in self._routes:
            self._routes[route_key] = RouteDataContainer(route_key)
        return self._routes[route_key]
    
    def list_routes(self) -> list:
        """
        List all route containers
        Returns:
            List of route keys in the module container.
        """
        return list(self._routes.keys())
    
    def clear_route(self, route_key: str):
        """
        Clear specific route container
        Args:
            route_key: Route key to clear
        """
        if route_key in self._routes:
            self._routes[route_key].clear_data()
    

    def __getattr__(self, name: str) -> RouteDataContainer:
        """
        Dynamic route access
        """
        full_route = f"{self._module_name}.{name}"
        return self.get_route_container(full_route)



class DataContainerManager:
    """
    Global data container manager - Root container
    This class manages all module-level containers and provides access to route data containers.
    It allows for dynamic registration of routes and provides a unified interface for accessing data containers.
    It supports automatic cleanup of orphaned containers and provides methods for saving and loading container data.    
    """
    
    def __init__(self):
        self._modules: Dict[str, ModuleDataContainer] = {}
        self._route_registry: Dict[str, str] = {}  # route -> module mapping
        self._route_containers: Dict[str, RouteDataContainer] = {}  # direct route access
        
        # Create standard module containers
        self._create_standard_modules()
    
    def _create_standard_modules(self):
        """
        Create standard module containers
        pass this fubction for example
        """
        pass
        #standard_modules = ['core', 'asset', 'data', 'report']
        #for module in standard_modules:
        #    self._modules[module] = ModuleDataContainer(module)
         
    def list_all_modules(self) -> List[str]:
        """
        List all registered module names.
        Returns:
            List of module names (e.g. ['core', 'asset', 'data', 'report']).
            These are always present by default.
        """
        return list(self._modules.keys())
    
    def list_all_routes(self) -> List[str]:
        """
        List all registered route keys.
        Returns:
            List of all route keys across all modules and direct route registrations.
        """
        # Collect from both module containers and direct route containers
        routes = set()
        for module in self._modules.values():
            routes.update(module.list_routes())
        routes.update(self._route_containers.keys())
        return list(routes)
    
    def list_all_containers(self) -> Dict[str, Dict[str, Any]]:
        """
        List all containers with their data.
        Returns:
            Dictionary mapping module names to their route containers and data.
            Also includes direct route containers not in modules.
        """
        all_data = {}
        for module_name, module_container in self._modules.items():
            all_data[module_name] = {}
            for route_key in module_container.list_routes():
                container = module_container.get_route_container(route_key)
                all_data[module_name][route_key] = container.items()
        # Add direct route containers not in modules
        for route_key, container in self._route_containers.items():
            module_name = route_key.split('.')[0]
            if module_name not in all_data:
                all_data[module_name] = {}
            if route_key not in all_data[module_name]:
                all_data[module_name][route_key] = container.items()
        return all_data
    
    def register_route(self, route: Union[str, Enum], module_name: Optional[str] = None):
        """
        Register route with module mapping
        Args:
            route: Route key or Enum to register
            module_name: Optional module name to associate with the route
        """
        route_key = route.value if isinstance(route, Enum) else route
        
        if module_name is None:
            # Auto-detect module from route key
            module_name = route_key.split('.')[0]
        
        self._route_registry[route_key] = module_name
        
        # Ensure module container exists
        if module_name not in self._modules:
            self._modules[module_name] = ModuleDataContainer(module_name)
        
        # Create direct route container for enum access
        if route_key not in self._route_containers:
            self._route_containers[route_key] = RouteDataContainer(route_key)
    
   
    def get_container(self, route: Union[str, Enum]) -> RouteDataContainer:
        """Get route data container"""
        route_key = route.value if isinstance(route, Enum) else route
        
        # Direct route container access
        if route_key in self._route_containers:
            return self._route_containers[route_key]
        
        # Fallback to module-based access
        module_name = self._route_registry.get(route_key, route_key.split('.')[0])
        
        if module_name not in self._modules:
            self._modules[module_name] = ModuleDataContainer(module_name)
        
        container = self._modules[module_name].get_route_container(route_key)
        self._route_containers[route_key] = container  # Cache for future access
        return container
    
    def __call__(self, route: Union[str, Enum]) -> RouteDataContainer:
        """Direct access via function call - supports both enum and string"""
        return self.get_container(route)
    
    def set_ui_instance(self, route: Union[str, Enum], instance: Any):
        """Set UI instance for route container"""
        container = self.get_container(route)
        container.set_ui_instance(instance)
    
    def remove_ui_instance(self, route: Union[str, Enum]):
        """Remove UI instance reference"""
        container = self.get_container(route)
        container.set_ui_instance(None)
    
    def get_status_report(self) -> Dict[str, Dict[str, str]]:
        """
        Get comprehensive status report.
        Returns:
            Dictionary mapping module names to route keys and their status.
            If no routes have been registered for a module, its value will be an empty dict.
        """
        report = {}
        for module_name, module_container in self._modules.items():
            report[module_name] = {}
            for route_key in module_container.list_routes():
                container = module_container.get_route_container(route_key)
                report[module_name][route_key] = container.status.value
        return report
    
    def cleanup_orphaned(self):
        """Clean up orphaned containers"""
        for module_container in self._modules.values():
            for route_key in module_container.list_routes():
                container = module_container.get_route_container(route_key)
                if container.status == ContainerStatus.ORPHANED:
                    container.clear_data()
    
    def save(self, file_path: str):
        """Persist all container data to a JSON file"""
        data = {}
        for route_key, container in self._route_containers.items():
            data[route_key] = {
                k: v.value for k, v in container._data.items()
            }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Container data saved to {file_path}")

    def load(self, file_path: str):
        """Load all container data from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for route_key, values in data.items():
                container = self.get_container(route_key)
                for k, v in values.items():
                    container.set_data(k, v)
            logger.info(f"Container data loaded from {file_path}")
        except Exception as e:
            logger.error(f"Failed to load container data from {file_path}: {e}")

    # Dynamic module access for IDE completion
    @property
    def core(self) -> ModuleDataContainer:
        """Core module data container"""
        return self._modules.get('core', ModuleDataContainer('core'))
    
    @property
    def asset(self) -> ModuleDataContainer:
        """Asset module data container"""
        return self._modules.get('asset', ModuleDataContainer('asset'))
    
    @property
    def data(self) -> ModuleDataContainer:
        """Data module data container"""
        return self._modules.get('data', ModuleDataContainer('data'))
    
    @property
    def report(self) -> ModuleDataContainer:
        """Report module data container"""
        return self._modules.get('report', ModuleDataContainer('report'))
    
    def __getattr__(self, name: str) -> ModuleDataContainer:
        """Dynamic module access"""
        if name not in self._modules:
            self._modules[name] = ModuleDataContainer(name)
        return self._modules[name]

# Global container manager instance
container_manager = DataContainerManager()
