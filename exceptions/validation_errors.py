from .base import NavixError

class FrameworkError(NavixError):
    """GUI framework related errors"""
    pass

class FrameworkNotDetectedError(FrameworkError):
    """Raised when no supported GUI framework is detected"""
    pass

class FrameworkCompatibilityError(FrameworkError):
    """Raised when framework compatibility issues occur"""
    pass

class ValidationError(NavixError):
    """Validation related errors"""
    pass

class InterceptorError(NavixError):
    """Interceptor related errors"""
    pass

class LifecycleError(NavixError):
    """UI lifecycle management errors"""
    pass
