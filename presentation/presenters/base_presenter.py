"""Базовый класс для Presenter."""

from abc import ABC, abstractmethod
from weakref import ref


class BasePresenter(ABC):

    def __init__(self):
        self._view_ref = None

    @property
    def view(self):
        if self._view_ref is not None:
            return self._view_ref()
        return None

    @view.setter
    def view(self, value):
        self._view_ref = ref(value) if value else None

    def is_view_attached(self) -> bool:
        return self.view is not None

    @abstractmethod
    def on_view_ready(self):
        ...