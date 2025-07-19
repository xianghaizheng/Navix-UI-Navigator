"""
Navix Application Builder - Fluent API for complete application setup
"""
# standard library imports
import      logging
from typing import Type, List, Dict, Any, Callable, Optional
from enum   import Enum
import      importlib
import      traceback

# Navix libraries
from ..navigation         import UIVoyager
from ..adapters           import GUIAdapter, FrameworkDetector
from .navigation_builder  import NavigationBuilder
from .validation_builder  import ValidationBuilder
from .interceptor_builder import InterceptorBuilder
from .container_builder   import ContainerBuilder
from ..config             import global_config

logger = logging.getLogger(__name__)

class NavixAppBuilder:
    """
    Fluent builder for Navix applications 
    
    Example:
    please see the module docstring for usage examples.
    """
    
    def __init__(self, app_name: str):
        self._app_name = app_name
        self._framework:   Optional[str] = None
        self._core_routes: Optional[Type[Enum]] = None
        self._main_route:  Optional[Enum] = None
        self._gui_widgets_module = None
        
        # Builder instances
        self._navigation_builder  = NavigationBuilder()
        self._validation_builder  = ValidationBuilder()
        self._interceptor_builder = InterceptorBuilder()
        self._container_builder   = ContainerBuilder()
        
        # Configuration
        self._config: Dict[str, Any] = {}
        self._startup_hooks: List[Callable] = []
        self._shutdown_hooks: List[Callable] = []
        
        logger.debug(f"Navix App Builder initialized for: {app_name}")
    
    def framework(self, framework_name: str) -> 'NavixAppBuilder':
        """
        Set GUI framework
        
        Args:
            framework_name: Framework name (uses FrameworkDetector for validation)
        Returns:
            self for fluent chaining
        """
        # Validate framework using FrameworkDetector
        try:
            FrameworkDetector.set_framework(framework_name) 
            self._framework = framework_name
            logger.debug(f"Framework validated and set: {framework_name}")
        except (ValueError, ImportError) as e:
            logger.error(f"Framework validation failed: {e}")
            raise ValueError(f"Unsupported or unavailable framework: {framework_name}. {e}")
        return self
    
    def auto_detect_framework(self) -> 'NavixAppBuilder':
        """
        Auto-detect available GUI framework
        Returns:
            self for fluent chaining
        """
        try:
            framework_name, _, _ = FrameworkDetector.detect_framework() 
            self._framework = framework_name
            logger.debug(f"Auto-detected framework: {framework_name}")
        except RuntimeError as e:
            logger.error(f"Framework auto-detection failed: {e}")
            raise
        
        return self
    
    def routes(self, core_routes: Type[Enum]) -> 'NavixAppBuilder':
        """
        Set core routes enum
        Args:
            core_routes: Enum class representing core routes
        """
        self._core_routes = core_routes
        return self
    
    def main_window(self, main_route: Enum) -> 'NavixAppBuilder':
        """
        Set main window route
        Args:
            main_route: Enum member representing the main window route
        """
        self._main_route = main_route
        return self
    
    def config(self, **kwargs) -> 'NavixAppBuilder':
        """
        Add configuration parameters
        Args:
            **kwargs: Configuration parameters to set
        """
        self._config.update(kwargs)
        return self
    
    def startup_hook(self, hook: Callable) -> 'NavixAppBuilder':
        """
        Add startup hook
        Args:
            hook: Callable to execute on application startup
        """
        self._startup_hooks.append(hook)
        return self
    
    def shutdown_hook(self, hook: Callable) -> 'NavixAppBuilder':
        """
        Add shutdown hook
        Args:
            hook: Callable to execute on application shutdown
        """
        self._shutdown_hooks.append(hook)
        return self
    
    def import_ui_modules(self, *module_paths: str) -> 'NavixAppBuilder':
        """
        Import UI modules for route registration
        Args:
            *module_paths: List of module paths to import
        Returns:
            self for fluent chaining
        """
        for module_path in module_paths:
            try:
                module = __import__(module_path, fromlist=[''])
              
                # debug logging
                logger.info(f"Success imported UI module: {module_path}")
                
                # check for classes in the module
                route_classes  = self._try_import_ui_classes(module, module_path)
                # debug logging
                if route_classes:
                    logger.debug(f"Found UI classes in {module_path}: {route_classes}")
                else:
                    logger.warning(f"No UI classes found in {module_path}")

            except ImportError as e:
                raise ImportError(f"Critical module import failed: {module_path} - {e}")
            except Exception as e:
                logger.error(f"Unexpected error importing {module_path}: {e}")
                raise
        return self
    
    #  
    def _try_import_ui_classes(self, module: Any, module_path: str)-> List[str]:
        import inspect
        route_classes = []
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                hasattr(obj, '__module__') and  
                obj.__module__ == module_path):
                route_classes.append(name)
        return route_classes
               
    # Fluent sub-builders
    def validation(self) -> ValidationBuilder:
        """
        Enter validation configuration mode
        Returns:
            ValidationBuilder instance for fluent configuration
        """
        self._validation_builder._parent = self
        return self._validation_builder
    
    def interceptors(self) -> InterceptorBuilder:
        """
        Enter interceptor configuration mode
        Returns:
            InterceptorBuilder instance for fluent configuration
        """
        self._interceptor_builder._parent = self
        return self._interceptor_builder
    
    def containers(self) -> ContainerBuilder:
        """
        Enter container configuration mode
        Returns:
            ContainerBuilder instance for fluent configuration
        """
        self._container_builder._parent = self
        return self._container_builder
    
    def navigation(self) -> NavigationBuilder:
        """
        Enter navigation configuration mode
        Returns:
            NavigationBuilder instance for fluent configuration
        """
        self._navigation_builder._parent = self
        return self._navigation_builder
    

    # 
    def build(self) -> 'NavixApplication':
        """
        Build the final Navix application
        """
        # debug logging
        logger.debug(f"Building Navix app: {self._app_name}")
        
        # Build application
        app = NavixApplication(
            name=self._app_name,
            framework=self._framework,
            core_routes=self._core_routes,
            main_route=self._main_route,
            config=self._config,
            startup_hooks=self._startup_hooks,
            shutdown_hooks=self._shutdown_hooks
        )
        
        # Apply configurations
        self._validation_builder._apply_to_app(app)
        self._interceptor_builder._apply_to_app(app)
        self._container_builder._apply_to_app(app)
        self._navigation_builder._apply_to_app(app)
        
        # debug logging
        logger.debug(f"Navix application '{self._app_name}' built successfully")
        return app


# the final Navix application class
class NavixApplication:
    """
    Built Navix Application - Ready to run
    """
    
    def __init__(self, name: str, framework: Optional[str], core_routes: Optional[Type[Enum]],
                 main_route: Optional[Enum], config: Dict[str, Any],
                 startup_hooks: List[Callable], shutdown_hooks: List[Callable]):
        self.name           = name
        self.framework      = framework
        self.core_routes    = core_routes
        self.main_route     = main_route
        self.config         = config
        self.startup_hooks  = startup_hooks
        self.shutdown_hooks = shutdown_hooks
        
        self.voyager: Optional[UIVoyager] = None
        self.main_window = None
        self._gui_app    = None
        
        # Configuration storage for builders
        self._validation_config  = {}
        self._interceptor_config = {}
        self._container_config   = {}
        self._navigation_config  = {}
        
        self.frameworks = global_config.Frameworks()
        if not self.frameworks:
            raise ValueError("No GUI frameworks configured in GlobalConfig.")
        
        # Initialize framework
        self._setup_framework()
    
    def _setup_framework(self):
        """
        Setup GUI framework using GUIAdapter
        """
        if self.framework:
            GUIAdapter.set_framework(self.framework)
        else:
            GUIAdapter.detect_framework()
       
        # debug logging
        #detected_framework = GUIAdapter.get_framework_name()
        #logger.debug(f"Navix Application using framework: {detected_framework}")
     
        # Import GUI widgets using GUIAdapter's detection
        self._import_gui_widgets()
    
    def _import_gui_widgets(self):
        """
        Import appropriate GUI widgets using GUIAdapter
        This method uses the detected framework to import the correct widgets.
        If the framework is not supported, it raises an ImportError.
        """
        framework_name = GUIAdapter.get_framework_name()
        if framework_name not in self.frameworks:
            raise ImportError(f"Framework {framework_name} is not configured in GlobalConfig.")
        try:
            framework_info           = self.frameworks[framework_name]
            module_name, widget_base = framework_info['module_name'], framework_info['widget_class']
            self._gui_widgets_module = importlib.import_module(module_name)
            # Optionally, check widget_base exists
            if not hasattr(self._gui_widgets_module, widget_base):
                raise ImportError(f"Widget base class {widget_base} not found in {module_name}")
            # Do NOT overwrite self._gui_widgets with the class
            # self._gui_widgets = getattr(self._gui_widgets, widget_base)
        except ImportError as e:
            logger.error(f"Failed to import widgets for framework {framework_name}: {e}")
            raise ImportError(f"Failed to import widgets for framework {framework_name}: {e}")

    # Application lifecycle methods
    def run(self) -> int:
        """
        Run the Navix application
        Returns:
            Exit code (0 for success, 1 for failure)
        """
        try:
            # Execute startup hooks 
            for hook in self.startup_hooks:  hook(self)
            
            # Create GUI application  by framework type
            framework_name = GUIAdapter.get_framework_name()
            if framework_name not in self.frameworks:
                raise ImportError(f"Framework {framework_name} is not configured in GlobalConfig.")
          
            application_class = self.frameworks[framework_name]['application_class']

            # Use the module to get the application class
            instance_class = getattr(self._gui_widgets_module, application_class, None)
            if not instance_class:
                raise ImportError(f"Application class {application_class} not found in {self._gui_widgets_module.__name__}")
            self._gui_app = instance_class([])  # Create application instance
           
            # Setup navigation - from core routes
            if self.core_routes:
                from ..routing import setup_navigator
                setup_navigator(self.core_routes)
                logger.debug(f"Setup navigator with {len(self.core_routes)} core routes")
            
            # Create voyager with configuration
            voyager_instance = UIVoyager(
                enable_validation=self.config.get('enable_validation', True),
                enable_security=self.config.get('enable_security', True)
            )
            self.voyager = voyager_instance  #
            
            # !! very important: apply builder configurations !!
            self._apply_builder_configurations()
            
            # Navigate to main window
            if self.main_route:
                # 主窗口构造时传递 voyager 参数
                self.main_window = voyager_instance.navigate_to(self.main_route, voyager=voyager_instance)
                
                if self.main_window:
                    self._print_startup_info()
                    return self._run_main_loop()
                else:
                    logger.error("Failed to create main window")
                    return 1
            else:
                logger.warning("No main route specified, application may not show UI")
                return self._run_main_loop()
                
        except Exception as e:
            logger.error(f"Application startup failed: {e}")
            traceback.print_exc()
            return 1
        
        finally:
            for hook in self.shutdown_hooks:
                try:
                    hook(self)
                except Exception as e:
                    logger.warning(f"Shutdown hook failed: {e}")

    def _apply_builder_configurations(self):
        """
        Apply all builder configurations to the voyager
        This method applies validation, interceptor, container, and navigation configurations
        to the UIVoyager instance.
        """
        # debug logging
        logger.debug("Applying builder configurations...")
        
        # Apply validation configuration
        if hasattr(self, '_validation_config') and self._validation_config:
            validation_config = self._validation_config
            
            # Add route patterns
            patterns = validation_config.get('patterns', [])
            for pattern in patterns:
                self.voyager.add_route_pattern(pattern)
                logger.debug(f"Added route pattern: {pattern}")
            
            # Add parameter rules
            parameter_rules = validation_config.get('parameter_rules', {})
            for param_name, validator_func in parameter_rules.items():
                self.voyager.add_parameter_rule(param_name, validator_func)
                logger.debug(f"Added parameter rule: {param_name}")
            
            # Set security checker
            security_checker = validation_config.get('security_checker')
            security_param_name = validation_config.get('security_param_name', "user_id")
            if security_checker:
                self.voyager.set_security_checker(security_checker, param_names=security_param_name)
                logger.debug("Applied security checker")
            
            logger.info(f"Applied validation config: {len(patterns)} patterns, {len(parameter_rules)} parameter rules")
        
        # Apply interceptor configuration
        if hasattr(self, '_interceptor_config') and self._interceptor_config:
            interceptor_config = self._interceptor_config
            
            # Register interceptors
            from ..routing import RouteCatalog
            interceptors = interceptor_config.get('interceptors', [])
            for interceptor_name, interceptor in interceptors:
                RouteCatalog.add_interceptor(interceptor)
                logger.debug(f"Registered interceptor: {interceptor_name}")
            
            logger.info(f"Applied interceptor config: {len(interceptors)} interceptors")
        
        # Apply container configuration
        if hasattr(self, '_container_config') and self._container_config:
            container_config = self._container_config
            
            # Set global data
            global_data = container_config.get('global_data', {})
            if global_data:
                from ..data_container import container_manager
                # Set global data in core module
                for key, value in global_data.items():
                    container_manager.core.main_window.set_data(key, value)
                    logger.debug(f"Set global data: {key}")
            
            logger.info(f"Applied container config: {len(global_data)} global data items")
        
        # Apply navigation configuration
        if hasattr(self, '_navigation_config') and self._navigation_config:
            navigation_config = self._navigation_config
            
            # Set max history
            max_history = navigation_config.get('max_history', 50)
            if hasattr(self.voyager, '_max_history'):
                self.voyager._max_history = max_history
                logger.debug(f"Set max history: {max_history}")
            
            logger.info("Applied navigation configuration")
        
        logger.info("All builder configurations applied successfully")

    def _run_main_loop(self) -> int:
        """
        Run the main event loop based on framework
        Returns:
            Exit code (0 for success, 1 for failure)
        """
        framework_name  = GUIAdapter.get_framework_name()
        mainloop_method = global_config.Framework_main_loop(framework_name)
        if not mainloop_method:
            logger.error(f"Main loop method not found for framework: {framework_name}")
            return 1
        instance_method = getattr(self._gui_app, mainloop_method, None)
      
        if not instance_method:
            logger.error(f"Main loop method {mainloop_method} not found in GUI application")
            return 1
    
        return instance_method()

        if framework.startswith(('PyQt', 'PySide')):
            return self._gui_app.exec()
      
        elif framework == 'wxPython':
            self._gui_app.MainLoop()
            return 0
      
        elif framework == 'tkinter':
            self._gui_app.mainloop()
            return 0
     
        else:
            logger.error(f"Don't know how to run main loop for framework: {framework}")
            return 1
    
    def _print_startup_info(self):
        """
        Print startup information
        now we close this method 
        """
        pass
        #print(f"{self.name} Started Successfully!")
        #print(f"Framework: {GUIAdapter.get_framework_name()}")
        #print(f"Main Window: {self.main_route.value if self.main_route else 'None'}")
        
        #if self.core_routes:
        #    routes_count = len(list(self.core_routes))
        #    print(f"Registered Routes: {routes_count}")



# Convenience function for fluent API entry point
def Navix_app(name: str) -> NavixAppBuilder:
    """
    Create a new Navix application builder
    
    Args:
        name: Application name
        
    Returns:
        NavixAppBuilder instance for fluent configuration
        
    Example:
        app = Navix_app("MyApp").framework("PySide6").routes(CoreRoutes).build()
    """
    return NavixAppBuilder(name)
