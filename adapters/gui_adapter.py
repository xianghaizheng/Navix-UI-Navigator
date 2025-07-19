# standard library imports
from   typing import Any, Type, TYPE_CHECKING
import logging

# qxx libraries
from .framework_detectors import FrameworkDetector
if TYPE_CHECKING:
    from .widget_wrapper import WidgetWrapper

logger = logging.getLogger(__name__)

class GUIAdapter:
    """
    this class provides a unified interface for different GUI frameworks.
    It detects the available framework and adapts the widget methods accordingly.
    This allows for seamless integration of different GUI libraries in the application.
    """
    
    _framework = None
    _widget_base = None
    _detected_framework = None

    @classmethod
    def detect_framework(cls) -> str:
        """
        automatically detect the available GUI framework
        Args:
            None
        Returns:
            The name of the detected GUI framework.
        """
        if cls._detected_framework:
            return cls._detected_framework
            
        # use the FrameworkDetector to find the available framework
        framework_name, framework_module, widget_base = FrameworkDetector.detect_framework()
        
        cls._detected_framework = framework_name
        cls._framework = framework_module  
        cls._widget_base = widget_base
        
        logger.info(f"Detected framework: {framework_name}")
        return framework_name

    @classmethod
    def set_framework(cls, framework_name: str):
        """
        manually set GUI framework
        Args:
            framework_name: name of the framework to set
        Returns:
            None
        """
        framework_module, widget_base = FrameworkDetector.set_framework(framework_name)
        
        cls._detected_framework = framework_name
        cls._framework = framework_module
        cls._widget_base = widget_base
        
        logger.info(f"Set framework: {framework_name}")

    @classmethod
    def get_framework_name(cls) -> str:
        """
        get the name of the currently set GUI framework
        Returns:
            The name of the currently set GUI framework.
        """
        if not cls._detected_framework:
            cls.detect_framework()
        return cls._detected_framework
    
    @classmethod
    def get_widget_base(cls) -> Type:
        """
        get the base widget class for the currently set GUI framework
        Args:
            None
        Returns:
            The base widget class for the currently set GUI framework.
        """
        if not cls._widget_base:
            cls.detect_framework()
        return cls._widget_base
    
    @classmethod
    def is_widget_instance(cls, obj: Any) -> bool:
        """
        check if the object is an instance of the base widget class
        Args:
            obj: The object to check.
        Returns:
            True if the object is an instance of the base widget class, False otherwise.
        """
        widget_base = cls.get_widget_base()
        return isinstance(obj, widget_base)
    
    @classmethod
    def adapt_widget_methods(cls, widget: Any) -> 'WidgetWrapper':
        """
        Wraps the widget to provide a unified interface across different frameworks.
        Args:
            widget: The widget instance to wrap.
        Returns:
            A WidgetWrapper instance that adapts the widget methods.
        """
        from .widget_wrapper import WidgetWrapper
        return WidgetWrapper(widget, cls.get_framework_name())