"""
Navix Navigation Event Bus - Publish/Subscribe for navigation events
==================================================================
Provides a simple event bus for navigation lifecycle events.
"""

from typing import Callable, Dict, List, Any


class NavigationEventBus:
    """
    widget event bus for navigation events
    This class implements a simple publish/subscribe pattern for navigation events.
    
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[..., None]]] = {}

    def subscribe(self, event: str, handler: Callable[..., None]):
        """
        Subscribe a handler to a navigation event
        Args:
            event: The event name to subscribe to.
            handler: The function to call when the event is published.

        """
        self._subscribers.setdefault(event, []).append(handler)

    def unsubscribe(self, event: str, handler: Callable[..., None]):
        """
        Unsubscribe a handler from a navigation event
        Args:
            event: The event name to unsubscribe from.
            handler: The function to remove from the event's subscribers.
        """
        if event in self._subscribers:
            self._subscribers[event] = [
                h for h in self._subscribers[event] if h != handler
            ]

    def publish(self, event: str, **kwargs):
        """
        Publish a navigation event to all subscribers
        Args:
            event: The event name to publish.
            kwargs: Additional keyword arguments to pass to the handlers.
        
        """
        for handler in self._subscribers.get(event, []):
            try:
                handler(**kwargs)
            except Exception:
                pass

# Global event bus instance
navigation_event_bus = NavigationEventBus()
