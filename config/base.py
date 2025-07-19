# standard library imports
import json
from pathlib import Path
from typing import Any, Dict

# qxx libraries
from ..interfaces import IJsonSerializable

# Helper function to load global configuration from config.json
def _get_global_config()-> Dict[str, Any]:
    """Get global configuration data from config.json"""
    from pathlib import Path
    import json
    _config_file = Path(__file__).parent.parent / "config.json"
    if not _config_file.exists():
        raise FileNotFoundError(f"Configuration file {_config_file} not found.")
    return json.loads(_config_file.read_text(encoding='utf-8'))


class GlobalConfig(IJsonSerializable):
    """
    Configuration manager for Navix framework
    Provides methods to load, save, and access configuration data.
    This class implements the IJsonSerializable interface for JSON serialization.
    """
    
    def __init__(self):
        self._data = _get_global_config()
        if not self._data:
            raise ValueError("Configuration data is empty or not loaded properly.")
    
    def DefaultConfig(self) -> Dict[str, Any]:
        """Get default configuration settings."""
        return self._data.get("DefaultConfig", {})
    
    def AppName(self) -> str:
        """Get the application name."""
        return self._data.get("DefaultConfig", {}).get("app_name", "Navix Application")
    
    def Version(self) -> str:
        """Get the application version."""
        return self._data.get("DefaultConfig", {}).get("version", "1.0.0")

    def DataDirectory(self) -> str:
        """Get the data directory path."""
        return self._data.get("DefaultConfig", {}).get("data_directory", "./data")
    
    def Frameworks(self) -> Dict[str, Any]:
        """Get all configured GUI frameworks."""
        return self._data.get("GuiFrameworks", {})

    def Framework_module(self, framework_name: str) -> Any:
        """Get the module name for a specific GUI framework."""
        return self._data.get("GuiFrameworks", {}).get(framework_name, {}).get("module_name")
    
    def Framework_widget_class(self, framework_name: str) -> Any:
        """Get the widget class for a specific GUI framework."""
        return self._data.get("GuiFrameworks", {}).get(framework_name, {}).get("widget_class")
    
    def Framework_application_class(self, framework_name: str) -> Any:
        """Get the application class for a specific GUI framework."""
        return self._data.get("GuiFrameworks", {}).get(framework_name, {}).get("application_class")
    
    def Framework_main_window_class(self, framework_name: str) -> Any:
        """Get the main window class for a specific GUI framework."""
        return self._data.get("GuiFrameworks", {}).get(framework_name, {}).get("main_window_class")
    
    def Framework_main_loop(self, framework_name: str) -> Any:
        """Get the main loop method for a specific GUI framework."""
        return self._data.get("GuiFrameworks", {}).get(framework_name, {}).get("main_loop")
    
    def Framework_version(self, framework_name: str) -> str:
        """Get the version of a specific GUI framework."""
        return self._data.get("GuiFrameworks", {}).get(framework_name, {}).get("version", "unknown")

    def to_json(self) -> Dict[str, Any]:
        """Convert configuration data to JSON format."""
        return self._data
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'GlobalConfig':
        """Create an instance from JSON data."""
        instance = cls()
        instance._data = data
        return instance


global_config = GlobalConfig()
