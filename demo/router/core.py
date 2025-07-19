from enum import Enum
class CoreRoutes(Enum):
    MAIN_WINDOW     = "core.main_window"
    ABOUT_DIALOG    = "core.about_dialog"
    SETTINGS_DIALOG = "core.settings_dialog"
    def __str__(self) -> str:
        return self.value