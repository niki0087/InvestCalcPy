"""
ServiceLocator - контейнер внедрения зависимостей.
"""

from typing import Any, Dict, Type, Callable
import inspect
import logging

logger = logging.getLogger(__name__)


class ServiceLocator:
    """Простой IoC контейнер для управления зависимостями."""

    def __init__(self):
        self._factories: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}

    def register_singleton(self, interface: Type, implementation: Any = None) -> None:
        if implementation is None:
            implementation = interface
        if inspect.isclass(implementation):
            self._factories[interface] = lambda: implementation()
            self._singletons[interface] = None
            logger.debug(f"Registered singleton factory: {interface.__name__}")
        else:
            self._singletons[interface] = implementation
            logger.debug(f"Registered singleton instance: {interface.__name__}")

    def register_factory(self, interface: Type, factory: Callable) -> None:
        self._factories[interface] = factory
        logger.debug(f"Registered factory: {interface.__name__}")

    def resolve(self, interface: Type) -> Any:
        if interface in self._singletons and self._singletons[interface] is not None:
            return self._singletons[interface]
        if interface in self._factories:
            instance = self._factories[interface]()
            if interface in self._singletons:
                self._singletons[interface] = instance
            return instance
        raise KeyError(f"Service '{interface.__name__}' not registered")

    def clear(self) -> None:
        self._factories.clear()
        self._singletons.clear()
        logger.debug("ServiceLocator cleared")


locator = ServiceLocator()