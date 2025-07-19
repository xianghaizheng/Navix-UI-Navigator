"""
Navix Navigation Module
========================================================
Professional UI Routing & Navigation System for PyQt/PySide Applications
"""

from .voyager import UIVoyager

from .interceptors import (
    LoggingInterceptor,
    PerformanceInterceptor, 
    SecurityInterceptor,
    RateLimitInterceptor,
    logging_interceptor,
    performance_interceptor,
    security_interceptor,
    rate_limit_interceptor
)

from .lifecycle import (
    ui_show_instance,
    ui_hide_instance,
    ui_destroy_instance
)

from .event_bus import navigation_event_bus

__all__ = [
    # Core voyager
    'UIVoyager',
    
    # Interceptors  
    'LoggingInterceptor',
    'PerformanceInterceptor',
    'SecurityInterceptor', 
    'RateLimitInterceptor',
    'logging_interceptor',
    'performance_interceptor',
    'security_interceptor',
    'rate_limit_interceptor',
    
    # Lifecycle utilities
    'ui_show_instance',
    'ui_hide_instance', 
    'ui_destroy_instance',
    
    # Event bus
    'navigation_event_bus',
]
