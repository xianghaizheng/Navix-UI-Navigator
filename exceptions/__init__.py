"""
Navix Exceptions Module
========================================================
Professional exception handling for Navix application components
"""

from .base import NavixError

from .routing_errors import (
    RouteError,
    RouteNotFoundError,
    RouteConflictError
)

from .navigation_errors import NavigationError

from .validation_errors import (
    FrameworkError,
    FrameworkNotDetectedError,
    FrameworkCompatibilityError,
    ValidationError,
    InterceptorError,
    LifecycleError
)

__all__ = [
    # Base exception
    'NavixError',
    
    # Routing errors
    'RouteError',
    'RouteNotFoundError', 
    'RouteConflictError',
    
    # Navigation errors
    'NavigationError',
    
    # Validation and framework errors
    'FrameworkError',
    'FrameworkNotDetectedError',
    'FrameworkCompatibilityError', 
    'ValidationError',
    'InterceptorError',
    'LifecycleError',
]