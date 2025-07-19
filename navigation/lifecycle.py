import logging
from typing import Any

logger = logging.getLogger(__name__)

def ui_show_instance(instance: Any) -> None:
    if hasattr(instance, 'show'):
        instance.show()
    else:
        logger.warning(f"Instance {type(instance)} doesn't have show method")
    
def ui_hide_instance( instance: Any) -> None:
    if hasattr(instance, 'hide'):
        instance.hide()
    else:
        logger.warning(f"Instance {type(instance)} doesn't have hide method")
    
def ui_destroy_instance(instance: Any) -> None:
    if hasattr(instance, 'close'):
        instance.close()
    elif hasattr(instance, 'destroy'):
        instance.destroy()
    else:
        logger.warning(f"Instance {type(instance)} doesn't have close/destroy method")
    