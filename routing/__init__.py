"""
Navix Routing Module
========================================================
Professional UI Routing & Navigation System for PyQt/PySide Applications
"""

from .catalog import RouteCatalog
from .decorators import navigate, setup_navigator
from .sources import RouteSource
from .manager import RouteManager 

__all__ = ['RouteCatalog', 
           'navigate', 
           'setup_navigator', 
           'RouteSource', 
           'RouteManager'
           ]