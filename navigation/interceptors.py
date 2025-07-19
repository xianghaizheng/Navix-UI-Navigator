"""
Navix UI Navigator - Built-in Interceptors
========================================================
Professional interceptor implementations for common use cases
"""
# standard library imports
import time
import logging
from   typing import Dict, Any

# qxx libraries
from ..interfaces import INavigationInterceptor

logger = logging.getLogger(__name__)


class LoggingInterceptor(INavigationInterceptor):
    """
    interceptor for logging all navigation operations
    This interceptor logs the route and parameters of each navigation attempt.
    It can be used to monitor navigation flow and debug issues.
    """
    
    def __init__(self, priority: int = 100):
        self._priority = priority
    
    def intercept(self, route: str, params: Dict[str, Any]) -> bool:
        """
        Log the navigation attempt
        Args:
            route: The route being navigated to.
            params: Additional parameters for the navigation.
        Returns:
            True to allow navigation, False to block it.
        """
        logger.info(f"Navigation attempt: {route} with params: {params}")
        return True
    
    def get_priority(self) -> int:
        return self._priority



class PerformanceInterceptor(INavigationInterceptor):
    """
    performance monitoring interceptor
    This interceptor tracks the time taken for navigation operations.
    """
    
    def __init__(self, priority: int = 90):
        self._priority = priority
        self._start_time = None
    
    def intercept(self, route: str, params: Dict[str, Any]) -> bool:
        """
        Start performance tracking for the navigation operation
        Args:
            route: The route being navigated to.
            params: Additional parameters for the navigation.
        Returns:
            True to allow navigation, False to block it.
        """
        self._start_time = time.time()
        logger.debug(f"Performance tracking started for: {route}")
        return True
    
    def get_priority(self) -> int:
        return self._priority



class SecurityInterceptor(INavigationInterceptor):
    """
    security check interceptor
    This interceptor performs security checks before allowing navigation.
    It can block access to certain routes based on user permissions or other criteria.
    """
    
    def __init__(self, priority: int = 200):
        self._priority         = priority
        self._blocked_routes   = set()
        self._user_permissions = {}
    
    def block_route(self, route: str):
        """
        block specific route
        Args:
            route: The route to block.
        """
        self._blocked_routes.add(route)
    
    def set_user_permissions(self, user_id: str, permissions: set):
        """
        set user permissions
        Args:
            user_id: The ID of the user.
            permissions: A set of permissions for the user.
        Returns:
            None
        """
        self._user_permissions[user_id] = permissions
    
    def intercept(self, route: str, params: Dict[str, Any]) -> bool:
        # check blocked list
        """
        Perform security checks before allowing navigation
        Args:
            route: The route being navigated to.
            params: Additional parameters for the navigation.
        Returns:
            True to allow navigation, False to block it.
        """
        if route in self._blocked_routes:
            logger.warning(f"Route {route} is blocked")
            return False
        
        # check user permissions (if user information is provided)
        user_id = params.get('user_id')
        if user_id and user_id in self._user_permissions:
            required_permission = f"access_{route.replace('.', '_')}"
            if required_permission not in self._user_permissions[user_id]:
                logger.warning(f"User {user_id} lacks permission for {route}")
                return False
        return True
    
    def get_priority(self) -> int:
        return self._priority



class RateLimitInterceptor(INavigationInterceptor):
    """
    rate limiting interceptor
    """
    def __init__(self, max_requests: int = 10, window_seconds: int = 60, priority: int = 150):
        self._priority       = priority
        self._max_requests   = max_requests
        self._window_seconds = window_seconds
        self._requests       = {}
    
    def intercept(self, route: str, params: Dict[str, Any]) -> bool:
        current_time = time.time()
        
        # cleanup expired records
        self._cleanup_expired_requests(current_time)
        
        # check rate limit
        if route not in self._requests:
            self._requests[route] = []
        
        route_requests = self._requests[route]
        if len(route_requests) >= self._max_requests:
            logger.warning(f"Rate limit exceeded for route: {route}")
            return False
        
        # record current request
        route_requests.append(current_time)
        return True
    
    def _cleanup_expired_requests(self, current_time: float):
        """
        cleanup expired request records
        """
        for route in list(self._requests.keys()):
            self._requests[route] = [
                req_time for req_time in self._requests[route]
                if current_time - req_time < self._window_seconds
            ]

            if not self._requests[route]:
                del self._requests[route]
    
    def get_priority(self) -> int:
        return self._priority


# convenient interceptor instances
logging_interceptor     = LoggingInterceptor()
performance_interceptor = PerformanceInterceptor()
security_interceptor    = SecurityInterceptor()
rate_limit_interceptor   = RateLimitInterceptor()
