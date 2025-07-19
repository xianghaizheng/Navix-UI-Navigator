class NavixError(Exception):
    """
    Base exception for all Navix related errors
    """
    
    def __init__(self, message: str, error_code: str = None, context: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__.upper()
        self.context = context or {}
