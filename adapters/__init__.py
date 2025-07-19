"""
QXX Adapters - framework Agnostic GUI Toolkit
========================================================
This module provides a framework-agnostic interface for GUI development, 
"""

from .gui_adapter import GUIAdapter
from .widget_wrapper import WidgetWrapper, WidgetProtocol
from .framework_detectors import FrameworkDetector

__all__ = [
    'GUIAdapter',
    'WidgetWrapper', 
    'WidgetProtocol',
    'FrameworkDetector',
]