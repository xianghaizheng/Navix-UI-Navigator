# standard library imports
from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class WidgetProtocol(Protocol):
    """
    Widget definition protocol 
    This protocol defines the common methods that any widget should implement.
    It allows for type checking and ensures that the widget can be used with the WidgetWrapper.
    """
    def show(self) -> None: ...
    def close(self) -> None: ...
    def isHidden(self) -> bool: ...
    def setParent(self, parent: Any) -> None: ...
    def raise_(self) -> None: ...
    def activateWindow(self) -> None: ...

class WidgetWrapper:
    """
    This class provides a consistent API for common widget operations
    across different GUI frameworks.
    Waring: This is a simplified version and may not cover all methods
    or properties of the native widget.
    """
    def __init__(self, widget: Any, framework: str):
        self._widget = widget
        self._framework = framework 
    
    def show(self):
        if hasattr(self._widget, 'show'):
            self._widget.show()
        elif hasattr(self._widget, 'Show'):  # wxPython
            self._widget.Show()
    
    def close(self):
        if hasattr(self._widget, 'close'):
            self._widget.close()
        elif hasattr(self._widget, 'Close'):  # wxPython
            self._widget.Close()
        elif hasattr(self._widget, 'destroy'):  # tkinter
            self._widget.destroy()
    
    def is_hidden(self) -> bool:
        if hasattr(self._widget, 'isHidden'):
            return self._widget.isHidden()
        elif hasattr(self._widget, 'IsShown'):  # wxPython
            return not self._widget.IsShown()
        elif hasattr(self._widget, 'winfo_viewable'):  # tkinter
            return not self._widget.winfo_viewable()
        return False
    
    def set_parent(self, parent: Any):
        if hasattr(self._widget, 'setParent'):
            self._widget.setParent(parent)
        elif hasattr(self._widget, 'SetParent'):  # wxPython
            self._widget.SetParent(parent)
    
    def bring_to_front(self):
        if hasattr(self._widget, 'raise_'):
            self._widget.raise_()
        if hasattr(self._widget, 'activateWindow'):
            self._widget.activateWindow()
        elif hasattr(self._widget, 'Raise'):  # wxPython
            self._widget.Raise()
        elif hasattr(self._widget, 'lift'):  # tkinter
            self._widget.lift()
    
    def show_normal(self):
        if hasattr(self._widget, 'showNormal'):
            self._widget.showNormal()
        elif hasattr(self._widget, 'Restore'):  # wxPython
            self._widget.Restore()

    def show_minimized(self):
        if hasattr(self._widget, 'showMinimized'):
            self._widget.showMinimized()
        elif hasattr(self._widget, 'Iconify'):  # wxPython
            self._widget.Iconify()
        elif hasattr(self._widget, 'iconify'):  # tkinter
            self._widget.iconify()
    
    def show_maximized(self):
        if hasattr(self._widget, 'showMaximized'):
            self._widget.showMaximized()
        elif hasattr(self._widget, 'Maximize'):  # wxPython
            self._widget.Maximize()
        elif hasattr(self._widget, 'state'):  # tkinter
            self._widget.state('zoomed')
    
    def hide(self):
        if hasattr(self._widget, 'hide'):
            self._widget.hide()
        elif hasattr(self._widget, 'Hide'):  # wxPython
            self._widget.Hide()
        elif hasattr(self._widget, 'withdraw'):  # tkinter
            self._widget.withdraw()

    def show_full_screen(self):
        if hasattr(self._widget, 'showFullScreen'):
            self._widget.showFullScreen()
        elif hasattr(self._widget, 'ShowFullScreen'):  # wxPython
            self._widget.ShowFullScreen()

    def set_focus(self):
        if hasattr(self._widget, 'setFocus'):
            self._widget.setFocus()
        elif hasattr(self._widget, 'SetFocus'):  # wxPython
            self._widget.SetFocus()
        elif hasattr(self._widget, 'focus_set'):  # tkinter
            self._widget.focus_set()

    def set_enabled(self, enabled: bool):
        if hasattr(self._widget, 'setEnabled'):
            self._widget.setEnabled(enabled)
        elif hasattr(self._widget, 'Enable'):  # wxPython
            self._widget.Enable(enabled)
        elif hasattr(self._widget, 'config'):  # tkinter
            state = 'normal' if enabled else 'disabled'
            self._widget.config(state=state)

    def resize(self, width: int, height: int):
        if hasattr(self._widget, 'resize'):
            self._widget.resize(width, height)
        elif hasattr(self._widget, 'SetSize'):  # wxPython
            self._widget.SetSize(width, height)
        elif hasattr(self._widget, 'geometry'):  # tkinter
            self._widget.geometry(f"{width}x{height}")
    
    @property
    def native_widget(self) -> Any:
        """
        get the native widget object
        Args:
            None
        Returns:
            The native widget object.
        """
        return self._widget
    
    def __getattr__(self, name):
        """
        Proxy other attributes to the native widget
        Args:
            name: The attribute name to access.
        Returns:
            The attribute value from the native widget. 
        """
        return getattr(self._widget, name)

