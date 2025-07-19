# stand libraries
from typing import Dict, Union
import importlib
import json
import logging
import yaml
import csv
from   pathlib import Path

logger = logging.getLogger(__name__)


#=========================================================#
class RouteSource:
    """
    route data source manager
    Provides functionality to load route configurations from various formats (JSON, CSV, YAML, Python modules)
    Supports multiple data source formats for flexible integration and configuration management
    """
    
    @staticmethod
    def from_json(file_path: Union[str, Path]) -> Dict[str, str]:
        """
        load routes from a JSON file
        Args:
            file_path: route configuration file path
        Returns:
            A dictionary mapping route names to their paths.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def from_csv(file_path: Union[str, Path], key_col: str = 'route_name', 
                 value_col: str = 'route_path') -> Dict[str, str]:
        """
        from CSV file load route configuration
        Args:
            file_path: route configuration file path
            key_col: column name for route keys
        Returns:
            A dictionary mapping route names to their paths.
        """
        routes = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                routes[row[key_col]] = row[value_col]
        return routes
    
    @staticmethod
    def from_yaml(file_path: Union[str, Path]) -> Dict[str, str]:
        """
        from YAML file load route configuration
        Args:
            file_path: route configuration file path
        Returns:
            A dictionary mapping route names to their paths.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def from_module(module_path: str, attr_name: str = 'ROUTES') -> Dict[str, str]:
        """
        from a Python module load route configuration
        Note: the module must define a variable with the specified name
              this method allows dynamic loading of routes from any module
              we can use this to load routes defined in a specific module       
        Args:
            module_path: path to the Python module
            attr_name: attribute name containing route definitions  
        Returns:
            A dictionary mapping route names to their paths.
        """
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)
