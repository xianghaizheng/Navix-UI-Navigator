"""
========================================================
UI Voyager: Professional UI Navigation System
"""
# standard library imports
from   typing import Dict, Optional, Any, Union, List
from   enum import Enum
import logging

# qxx libraries
from ..routing  import RouteCatalog
from ..adapters import GUIAdapter, WidgetWrapper
from ..interfaces import IUILifecycleManager
from ..validation import route_validator, security_validator, RouteValidationError, ParameterValidationError
from ..exceptions import NavigationError, RouteNotFoundError, FrameworkError
from ..data_container import container_manager  
from ..navigation.event_bus import navigation_event_bus

logger = logging.getLogger(__name__)

class UIVoyager(IUILifecycleManager):
    """
    UI Navigator: manages UI instance creation, navigation and lifecycle
    This class implements the IUILifecycleManager interface and provides methods
    for navigating between different UI components, managing their lifecycle,"""
    
    def __init__(self, gui_framework: Optional[str] = None, 
                 enable_validation: bool = True,
                 enable_security: bool = True):
       
        self._fleet: Dict[str, Dict[str, WidgetWrapper]] = {}  # route_key -> {instance_id: WidgetWrapper}
        self._history: List[str] = []  # navigation history
        self._current_route: Optional[str] = None # current route key
        self._max_history: int  = 50 # maximum history length
        self._enable_validation = enable_validation # enable route and parameter validation
        self._enable_security   = enable_security # enable security checks
        self._security_param_name = "user_id"  # 新增：安全参数名，默认为 user_id
        # try initialize GUI adapter
        try:
            if gui_framework:
                GUIAdapter.set_framework(gui_framework)
            else:
                GUIAdapter.detect_framework()
        except Exception as e:
            raise FrameworkError(f"Failed to initialize GUI framework: {e}")
        logger.info(f"UIVoyager initialized with {GUIAdapter.get_framework_name()}")
    
    def _make_fleet_key(self, route_key: str, instance_id: Optional[str] = None, endpoint: Optional[str] = None) -> str:
        """
        create a unique key for the fleet based on route, instance_id and endpoint
        Args:
            route_key: The route key to use.
            instance_id: Optional instance identifier.
            endpoint: Optional endpoint identifier.
        Returns:
            A unique key for the fleet.
        """
        key = route_key
        if endpoint:
            key += f"@{endpoint}"
        if instance_id:
            key += f"#{instance_id}"
        return key

    def navigate_to(self, route: Union[str, Enum], parent: Optional[Any] = None,
                   force_new: bool = False, instance_id: Optional[str] = None, endpoint: Optional[str] = None, **voyage_params) -> Optional[Any]:
        """
        navigate to specified route - now includes professional validation
        Args:
            route: The route to navigate to, can be a string or Enum member.
            parent: Optional parent widget for the new UI instance.
            force_new: If True, always create a new instance even if one exists.
            instance_id: Optional identifier for the instance.
            endpoint: Optional endpoint identifier for multi-instance support.
            **voyage_params: Additional parameters to pass to the UI instance.
        Returns:
            The UI instance if navigation was successful, None if blocked or failed.
        """
        route_key = route.value if isinstance(route, Enum) else route
        fleet_key = self._make_fleet_key(route_key, instance_id, endpoint)
       
        # publish navigation event
        navigation_event_bus.publish("before_navigate", route=route_key, params=voyage_params)
        try:
            # 1. route validation
            if self._enable_validation:
                self._validate_navigation(route, voyage_params)
            
            # 2. security validation
            if self._enable_security:
                self._validate_security(route_key, voyage_params)
            
            # 3. execute interceptors
            if not self._execute_interceptors(route_key, voyage_params):
                logger.debug(f"Navigation to {route_key} intercepted")
                # navigation_event_bus.publish("navigation_intercepted", route=route_key, params=voyage_params)
                navigation_event_bus.publish("navigation_failed", route=route_key, params=voyage_params, error="Navigation intercepted by interceptor")
                raise NavigationError(f"Navigation to {route_key} intercepted by interceptor")
            
            # 4. get navigation information
            navigator_info = RouteCatalog.get_navigator_info(route)
            if not navigator_info:
                raise RouteNotFoundError(f"Navigator not found for route: {route_key}")
            
            # 5. check if instance already exists
            if navigator_info.get('singleton') and not force_new and not instance_id:
                existing = self._fleet.get(route_key, {}).get("default")
                if existing and not existing.is_hidden():
                    existing.bring_to_front()
                    self._update_navigation_history(fleet_key)
                    return existing.native_widget

            # 6. check if specific instance exists
            if not force_new and instance_id:
                existing = self._fleet.get(route_key, {}).get(instance_id)
                if existing and not existing.is_hidden():
                    existing.bring_to_front()
                    self._update_navigation_history(fleet_key)
                    return existing.native_widget

            #  7. create new UI instance
            ui_instance = self._create_ui_instance(navigator_info, voyage_params)
            self._show_ui_instance(ui_instance, route_key, parent, instance_id, endpoint)
            
            # 8. publish successful navigation event
            navigation_event_bus.publish("after_navigate", route=route_key, params=voyage_params, instance=ui_instance)
            
            # debug log
            logger.debug(f"Successfully navigated to: {route_key}")
            return ui_instance
            
        except (RouteValidationError, ParameterValidationError, RouteNotFoundError) as e:
            navigation_event_bus.publish("navigation_failed", route=route_key, params=voyage_params, error=e)
            logger.error(f"Navigation validation failed: {e}")
            raise NavigationError(f"Failed to navigate to {route_key}: {e}")
   
        except Exception as e:
            navigation_event_bus.publish("navigation_failed", route=route_key, params=voyage_params, error=e)
            logger.error(f"Unexpected navigation error: {e}")
            raise NavigationError(f"Navigation to {route_key} failed: {e}")
    
    def _validate_navigation(self, route: Union[str, Enum], params: Dict[str, Any]):
        """
        execute route and parameter validation
        Args:
            route: The route to validate.
            params: Parameters to validate.
        Raises:
            RouteValidationError: If the route is invalid.
        """
        route_validator.validate_route(route)
        route_validator.validate_params(params)
    
  
    def _validate_security(self, route_key: str, params: Dict[str, Any]):
        """
        execute security validation
        Args:
            route_key: The route key to validate.
            params: Parameters to validate.
        Raises:
            NavigationError: If security validation fails.
        """
        # 只传递 route_key 和 params，不传 param_name
        if not security_validator.validate_security(route_key, params):
            raise NavigationError(f"Security validation failed for route: {route_key}")
    
    def _execute_interceptors(self, route_key: str, params: Dict[str, Any]) -> bool:
        """
        execute all interceptors
        Args:
            route_key: The route key to check.
            params: Parameters to pass to interceptors.
        Returns:
            True if all interceptors allow navigation, False if any blocks it.
        """
        for interceptor in RouteCatalog.get_interceptors():
            # check if it's an object implementing INavigationInterceptor interface
            if hasattr(interceptor, 'intercept') and hasattr(interceptor, 'get_priority'):
                # call intercept method
                if not interceptor.intercept(route_key, params):
                    return False
            else:
                # normal function interceptor
                if not interceptor(route_key, params):
                    return False
        return True
    
    def _create_ui_instance(self, navigator_info: Dict[str, Any], 
                           voyage_params: Dict[str, Any]) -> Any:
        """
        create UI instance - implements IUILifecycleManager interface
        Args:
            navigator_info: Information about the navigator including UI class and metadata.
            voyage_params: Parameters to pass to the UI instance constructor.
        """
        ui_class = navigator_info['ui_class']
        meta     = navigator_info.get('meta', {})
        # filter voyage_params to exclude sensitive data
        # such as user_id, token, session etc.
        filtered_params = {k: v for k, v in voyage_params.items() if k not in ('user_id', 'token', 'session')}
        creation_params = {**meta, **filtered_params}
        
        return self.create_instance(ui_class, **creation_params)
    
    def _show_ui_instance(self, ui_instance: Any, route_key: str, parent: Optional[Any], instance_id: Optional[str] = None, endpoint: Optional[str] = None):
        """
        show UI instance
        Args:
            ui_instance: The UI instance to show.
            route_key: The route key for the instance.
            parent: Optional parent widget for the new UI instance.
            instance_id: Optional identifier for the instance.
            endpoint: Optional endpoint identifier for multi-instance support.
        Returns:
            None
        """
        # validate Widget type
        if not GUIAdapter.is_widget_instance(ui_instance):
            logger.warning(f"Created instance may not be a valid widget: {type(ui_instance)}")
        
        fleet_key = self._make_fleet_key(route_key, instance_id, endpoint)
        # wrap Widget
        wrapped_widget = GUIAdapter.adapt_widget_methods(ui_instance)
        
        # set parent
        if parent:
            wrapped_widget.set_parent(parent)
        
        # Register with data container system
        container_manager.set_ui_instance(route_key, ui_instance)
        
        # add to fleet
        if route_key not in self._fleet:
            self._fleet[route_key] = {}
        self._fleet[route_key][instance_id or "default"] = wrapped_widget
        
        # add to fleet and show
        self.show_instance(ui_instance)
        
        # update navigation state
        self._update_navigation_history(fleet_key) 
        self._current_route = fleet_key
    

    def _update_navigation_history(self, route_key: str):
        """
        update navigation history
        Args:
            route_key: The route key to add to history.
        """
        if route_key in self._history:
            self._history.remove(route_key)
        
        self._history.append(route_key)
        
        # limit history length
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
    
    def get_current_ui(self, route: Union[str, Enum], instance_id: Optional[str] = None, endpoint: Optional[str] = None) -> Optional[Any]:
        """
        get current UI instance
        Args:
            route: The route to get the UI instance for.
            instance_id: Optional identifier for the instance.
            endpoint: Optional endpoint identifier for multi-instance support.
        """
        route_key = route.value if isinstance(route, Enum) else route
        key = instance_id or "default"
        return self._fleet.get(route_key, {}).get(key, None).native_widget if key in self._fleet.get(route_key, {}) else None
    
    def close_navigation(self, route: Union[str, Enum], instance_id: Optional[str] = None, endpoint: Optional[str] = None) -> bool:
        """
        close navigation
        Args:
            route: The route to close.
            instance_id: Optional identifier for the instance.
            endpoint: Optional endpoint identifier for multi-instance support.
        Returns:
            True if navigation was closed successfully, False if not found.
        """
        route_key = route.value if isinstance(route, Enum) else route
        key = instance_id or "default"
        navigation_event_bus.publish("before_close", route=route_key)
        wrapped_widget = self._fleet.get(route_key, {}).get(key)
        
        if wrapped_widget:
            # Remove from data container system
            container_manager.remove_ui_instance(route_key)
            
            wrapped_widget.close()
            del self._fleet[route_key][key]
            if not self._fleet[route_key]:
                del self._fleet[route_key]
           
            # update current route
            if self._current_route == self._make_fleet_key(route_key, instance_id, endpoint):
                self._current_route = self._history[-1] if self._history else None
            
            logger.debug(f"Closed navigation: {route_key} instance_id={instance_id}")
            # publish event
            navigation_event_bus.publish("after_close", route=route_key)
           
            return True
        return False
    
    def navigate_back(self) -> Optional[Any]:
        """
        navigate back to previous route
        """
        if len(self._history) < 2:
            return None
        # remove current route
        self._history.pop()
        previous_route = self._history[-1]
        return self.navigate_to(previous_route)
    
    def get_active_navigations(self) -> Dict[str, Any]:
        """
        get all active navigations (all instances)
        Returns:
            A dictionary of active navigations with route keys as keys and UI instances as values.
        """
        result = {}
        for route_key, instances in self._fleet.items():
            for instance_id, wrapped in instances.items():
                if wrapped and not wrapped.is_hidden():
                    result[f"{route_key}#{instance_id}"] = wrapped.native_widget
        return result
    
    def clear_fleet(self):
        """
        clear entire fleet
        """
        for wrapped_widget in self._fleet.values():
            if wrapped_widget and not wrapped_widget.is_hidden():
                wrapped_widget.close()

        self._fleet.clear()
        self._history.clear()
        self._current_route = None
        logger.debug("Fleet cleared")

    def configure_validation(self, enable_validation: bool = True, 
                           enable_security: bool = True):
        """
        configure validation options
        Args:
            enable_validation: Enable route and parameter validation.
            enable_security: Enable security checks.
        Returns:
            None
        """
        self._enable_validation = enable_validation
        self._enable_security = enable_security
        logger.info(f"Validation configured: validation={enable_validation}, security={enable_security}")
    
    def add_route_pattern(self, pattern: str):
        """
        add route naming pattern
        Args:
            pattern: Regular expression pattern for route validation.
        """
        route_validator.add_route_pattern(pattern)
    
    def add_parameter_rule(self, param_name: str, validator_func):
        """
        add parameter validation rule
        Args:
            param_name: Name of the parameter to validate.
            validator_func: Function that takes a parameter value and returns True if valid, False otherwise.
        """
        route_validator.add_parameter_rule(param_name, validator_func)
    
    def set_security_checker(self, checker_func,  param_names: Union[str, List[str]] = "user_id"):
        """
        set custom security checker
        Args:
            checker_func: Function(route, params, param_name) -> bool
            param_names: The parameter name to use for user identity (default 'user_id').
        """
        if isinstance(param_names, str):
            param_names = [param_names]
        self._security_param_names = param_names
        security_validator.set_permission_checker(checker_func)
        security_validator.set_param_names(param_names)

    @property
    def current_route(self) -> Optional[str]:
        """current route"""
        return self._current_route
    
    @property
    def navigation_history(self) -> List[str]:
        """navigation history"""
        return self._history.copy()
    
    @property
    def gui_framework(self) -> str:
        """current GUI framework"""
        return GUIAdapter.get_framework_name()
    

    # implement IUILifecycleManager interface
    def create_instance(self, ui_class: type, **kwargs) -> Any:
        """
        create UI instance
        Args:
            ui_class: The UI class to instantiate.
            **kwargs: Parameters to pass to the UI class constructor.
        Returns:
            An instance of the UI class.
        """
        try:
            return ui_class(**kwargs)
        except Exception as e:
            raise NavigationError(f"Failed to create instance of {ui_class.__name__}: {e}")
    
    def show_instance(self, instance: Any) -> None:
        """show UI instance"""
        if hasattr(instance, 'show'):
            instance.show()
        else:
            logger.warning(f"Instance {type(instance)} doesn't have show method")
    
    def hide_instance(self, instance: Any) -> None:
        """hide UI instance"""
        if hasattr(instance, 'hide'):
            instance.hide()
        else:
            logger.warning(f"Instance {type(instance)} doesn't have hide method")
    
    def destroy_instance(self, instance: Any) -> None:
        """destroy UI instance"""
        if hasattr(instance, 'close'):
            instance.close()
        elif hasattr(instance, 'destroy'):
            instance.destroy()
        else:
            logger.warning(f"Instance {type(instance)} doesn't have close/destroy method")
    
    def get_ui_instance(self, route: Union[str, Enum], **params) -> Optional[Any]:
        """
        Get UI instance directly without navigation - creates if not exists
        Args:
            route: route name or Enum member
            **params: parameters to pass to UI constructor
        Returns:
            UI instance or None if route not found
        """
        route_key = route.value if isinstance(route, Enum) else route
        
        # Check if instance already exists in fleet
        existing = self._fleet.get(route_key)
        if existing:
            return existing.native_widget
        
        # Get navigator info
        navigator_info = RouteCatalog.get_navigator_info(route)
        if not navigator_info:
            logger.warning(f"Navigator not found for route: {route_key}")
            return None
        
        # Create instance without navigation (no validation, no interceptors)
        try:
            ui_class = navigator_info['ui_class']
            meta = navigator_info.get('meta', {})
            creation_params = {**meta, **params}
            
            ui_instance = self.create_instance(ui_class, **creation_params)
            
            # Add to fleet for tracking but don't show
            wrapped_widget = GUIAdapter.adapt_widget_methods(ui_instance)
            self._fleet[route_key] = wrapped_widget
            
            # debug log
            #logger.debug(f"Created UI instance for route: {route_key}")
            return ui_instance
            
        except Exception as e:
            logger.error(f"Failed to create UI instance for {route_key}: {e}")
            return None
    
    def get_ui_class(self, route: Union[str, Enum]) -> Optional[type]:
        """
        Get UI class for manual instantiation
        Args:
            route: route name or Enum member
        Returns:
            UI class or None if route not found
        """
        route_key = route.value if isinstance(route, Enum) else route
        navigator_info = RouteCatalog.get_navigator_info(route)
        
        if not navigator_info:
            logger.warning(f"Navigator not found for route: {route_key}")
            return None
        
        return navigator_info['ui_class']
    
    def release_instance(self, route: Union[str, Enum]) -> bool:
        """
        Release instance from fleet management (user takes full control)
        Args:
            route: route name or Enum member
        Returns:
            True if instance was released, False if not found
        """
        route_key = route.value if isinstance(route, Enum) else route
        
        if route_key in self._fleet:
            # Remove from fleet without closing
            del self._fleet[route_key]
            
            # Remove from history if present
            if route_key in self._history:
                self._history.remove(route_key)
            
            # Update current route if needed
            if self._current_route == route_key:
                self._current_route = self._history[-1] if self._history else None
            
            # debug log
            logger.debug(f"Released instance control for route: {route_key}")
            return True
        
        return False
