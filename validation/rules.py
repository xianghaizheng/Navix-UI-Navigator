"""
Navix UI Navigator - Validation Rules
========================================================
Predefined validation rules and patterns for common use cases
"""

from typing import Dict, List, Callable, Any

# default route naming patterns
DEFAULT_ROUTE_PATTERNS = [
    r'^[a-z_]+\.[a-z_]+$',  # module.component format (core.main_window)
]

# reserved route list
RESERVED_ROUTES = {
    'system.error',
    'system.loading', 
    'system.unauthorized'
}

# common parameter validation rule functions
def validate_user_id(value: Any) -> bool:
    """validate user ID format"""
    return isinstance(value, str) and len(value) > 0

def validate_admin_level(value: Any) -> bool:
    """validate admin level"""
    return isinstance(value, int) and 0 <= value <= 10

def validate_asset_id(value: Any) -> bool:
    """validate asset ID"""
    return isinstance(value, (int, str)) and str(value).isdigit()

def validate_theme(value: Any) -> bool:
    """validate theme name"""
    valid_themes = {'light', 'dark', 'auto'}
    return isinstance(value, str) and value in valid_themes

# predefined validation rule set
COMMON_PARAMETER_RULES: Dict[str, Callable[[Any], bool]] = {
    'user_id': validate_user_id,
    'admin_level': validate_admin_level,
    'asset_id': validate_asset_id,
    'theme': validate_theme,
}

# security-related preset blocking patterns
SECURITY_BLOCKED_PATTERNS = [
    r'.*\.dangerous_.*',
    r'system\.admin\..*',
    r'.*\.debug_.*',
]
