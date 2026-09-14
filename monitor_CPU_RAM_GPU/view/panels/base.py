"""BasePanel: один раз создаёт виджеты, потом только обновляет."""
from tkinter import ttk
from typing import Any


class BasePanel(ttk.LabelFrame):
    def __init__(self, master, title: str):
        super().__init__(master, text=title)
        self._built = False

    def build(self) -> None:
        """Переопределяется в наследнике. Вызывается ровно один раз."""
        self._built = True

    def update_data(self, metrics: Any) -> None:
        """Переопределяется в наследнике."""
        raise NotImplementedError

    def ensure_built(self) -> None:
        if not self._built:
            self.build()