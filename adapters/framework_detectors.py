# standard library imports
import importlib
import logging
from   typing import Tuple, Any
# qxx libraries

logger = logging.getLogger(__name__)

from ..config import global_config

class FrameworkDetector:
    """
    Detects the available GUI framework
    and provides a way to set it manually.
    """
    # unified list of supported frameworks
    frameworks = global_config.Frameworks()
    if not frameworks:
        raise ValueError("No GUI frameworks configured in GlobalConfig.")

    @classmethod
    def detect_framework(cls) -> Tuple[str, Any, Any]:
        """
        automatically detect the available GUI framework
        Args:
            None
        Returns:
            Tuple of (framework_name, framework_module, widget_base)
        """
        if cls.frameworks is None:
            raise RuntimeError("No GUI frameworks configured in GlobalConfig.")
       
        for key in cls.frameworks: 
            framework = cls.frameworks[key]
            try:
                module = importlib.import_module(framework["module_name"])
                widget_base = getattr(module, framework["widget_class"])
                return key, module, widget_base
            except ImportError as e:
                logger.warning(f"Framework {key} not available: {e}")
        raise RuntimeError("No supported GUI framework found")
    
    @classmethod
    def set_framework(cls, framework_name: str) -> Tuple[Any, Any]:
        """
        manually set GUI framework
        Args:
            framework_name: name of the framework to set
        Returns:
            Tuple of (framework_module, widget_base)
        """
        if framework_name not in cls.frameworks: 
            raise ValueError(f"Framework {framework_name} is not configured in GlobalConfig.")
        
        framework = cls.frameworks[framework_name]
        try:
            module = importlib.import_module(framework["module_name"])
            widget_base = getattr(module, framework["widget_class"])
            return module, widget_base
        except ImportError as e:
            logger.error(f"Failed to set framework {framework_name}: {e}")
            raise RuntimeError(f"Failed to set framework {framework_name}")

        