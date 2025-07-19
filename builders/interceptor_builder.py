"""
Navix Interceptor Builder - Fluent API for interceptor configuration
"""
# standard library imports
import logging
from typing import Callable, Any, TYPE_CHECKING

# qxx libraries
if TYPE_CHECKING:
    from .app_builder import NavixAppBuilder

logger = logging.getLogger(__name__)

class InterceptorBuilder:
    """
    Fluent builder for interceptor configuration
    
    Example:
        .interceptors()
            .logging(priority=100)
            .security(priority=200)
                .block_routes('system.dangerous_operation')
                .user_permissions('admin', {'access_all'})
            .performance(priority=90)
            .rate_limit(max_requests=10, window_seconds=60)
            .custom(my_interceptor)
    """
    
    def __init__(self):
        self._parent: 'NavixAppBuilder' = None
        self._interceptors       = []
        self._security_config    = {}
        self._performance_config = {}
        self._rate_limit_config  = {}
    
    def logging(self, priority: int = 100, logger_name: str = None) -> 'InterceptorBuilder':
        """
        Add logging interceptor
        Args:
            priority: Priority of the interceptor (lower values run first)
            logger_name: Optional custom logger name
        Returns:
            self
        """
        from ..navigation.interceptors import LoggingInterceptor
        interceptor = LoggingInterceptor(priority=priority)
        self._interceptors.append(('logging', interceptor))
        return self
    
    def security(self, priority: int = 200) -> 'SecurityInterceptorBuilder':
        """
        Add security interceptor with sub-configuration
        Args:
            priority: Priority of the security interceptor
        Returns:
            SecurityInterceptorBuilder: Sub-builder for security interceptor configuration
        """
        from ..navigation.interceptors import SecurityInterceptor
        interceptor = SecurityInterceptor(priority=priority)
        self._interceptors.append(('security', interceptor))
        return SecurityInterceptorBuilder(self, interceptor)
    
    def performance(self, priority: int = 90, track_memory: bool = False) -> 'InterceptorBuilder':
        """
        Add performance monitoring interceptor
        Args:
            priority: Priority of the interceptor
            track_memory: Whether to track memory usage
        Returns:
            self
        """
        from ..navigation.interceptors import PerformanceInterceptor
        interceptor = PerformanceInterceptor(priority=priority)
        self._interceptors.append(('performance', interceptor))
        self._performance_config.update({'track_memory': track_memory})
        return self
    
    def rate_limit(self, max_requests: int = 10, window_seconds: int = 60, priority: int = 150) -> 'InterceptorBuilder':
        """
        Add rate limiting interceptor
        Args:
            max_requests: Maximum number of requests allowed in the time window
            window_seconds: Time window in seconds for rate limiting
            priority: Priority of the interceptor   
        Returns:
            self
        """
        from ..navigation.interceptors import RateLimitInterceptor
        interceptor = RateLimitInterceptor(max_requests, window_seconds, priority)
        self._interceptors.append(('rate_limit', interceptor))
        return self
    
    def custom(self, interceptor: Any, name: str = None) -> 'InterceptorBuilder':
        """
        Add custom interceptor
        Args:
            interceptor: Custom interceptor instance or callable
            name: Optional name for the interceptor
        Returns:
            self
        """
        interceptor_name = name or f"custom_{len(self._interceptors)}"
        self._interceptors.append((interceptor_name, interceptor))
        return self
    
    def lambda_interceptor(self, func: Callable[[str, dict], bool], priority: int = 100, name: str = None) -> 'InterceptorBuilder':
        """
        Add lambda-based interceptor
        Args:
            func: Callable function that takes route and parameters, returns True to allow navigation
            priority: Priority of the interceptor
            name: Optional name for the interceptor
        """

        class LambdaInterceptor:
            """ Lambda-based interceptor implementation"""
            def __init__(self, func, priority):
                self._func = func
                self._priority = priority
            
            def intercept(self, route: str, params: dict) -> bool:
                return self._func(route, params)
            
            def get_priority(self) -> int:
                return self._priority
        
        interceptor = LambdaInterceptor(func, priority)
        interceptor_name = name or f"lambda_{len(self._interceptors)}"
        self._interceptors.append((interceptor_name, interceptor))
        return self
    
    # Return to parent builder
    def end(self) -> 'NavixAppBuilder':
        """
        Return to parent app builder
        Returns:
            The parent NavixAppBuilder instance.
        """
        return self._parent
    
    def _apply_to_app(self, app):
        """Apply interceptor configuration to the application"""
        app._interceptor_config = {
            'interceptors': self._interceptors,
            'security_config': self._security_config,
            'performance_config': self._performance_config,
            'rate_limit_config': self._rate_limit_config
        }
        
        logger.debug(f"Applied interceptor config: {len(self._interceptors)} interceptors")


        #Apply security configuration if any
        #if self._security_config:
        #    security_interceptor = next((i for i in self._interceptors if i[0] == 'security'), None)
        #    if security_interceptor:
        #        security_interceptor[1].configure(self._security_config)

class SecurityInterceptorBuilder:
    """
    Sub-builder
    for security interceptor configuration
    Example:
        .security()
            .block_routes('system.dangerous_operation')
            .user_permissions('admin', {'access_all'})
    """
    
    def __init__(self, parent: InterceptorBuilder, security_interceptor):
        self._parent = parent
        self._security_interceptor = security_interceptor
    
    def block_routes(self, *routes: str) -> 'SecurityInterceptorBuilder':
        """
        Block specific routes
        Args:
            routes: List of route names to block
        Returns:
            self
        """
        for route in routes:
            self._security_interceptor.block_route(route)
        return self
    
    def user_permissions(self, user_id: str, permissions: set) -> 'SecurityInterceptorBuilder':
        """
        Set user permissions
        Args:
            user_id: User identifier (e.g., 'admin', 'user')
            permissions: Set of permissions to assign to the user
        Returns:
            self
        """
        self._security_interceptor.set_user_permissions(user_id, permissions)
        return self
    
    def end(self) -> InterceptorBuilder:
        """
        Return to interceptor builder
        """
        return self._parent

# Convenience function
def interceptors() -> InterceptorBuilder:
    """Create standalone interceptor builder"""
    return InterceptorBuilder()
