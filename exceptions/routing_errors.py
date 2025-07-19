from .base import NavixError

class RouteError(NavixError):
    """Route definition and registration errors"""
    pass

class RouteNotFoundError(RouteError):
    """Raised when route cannot be found"""
    pass

class RouteConflictError(RouteError):
    """Raised when route conflicts occur"""
    pass