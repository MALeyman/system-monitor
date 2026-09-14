"""Прогрессбар с подписью внутри (общая обёртка)."""
from tkinter import ttk
import tkinter as tk


class LabeledProgressbar(ttk.Progressbar):
    """ttk.Progressbar с удобным update(value, text, color)."""

    def __init__(self, master, style: str, length: int = 250):
        super().__init__(master, length=length, mode="determinate", style=style)
        self._style = style
        self._style_obj = ttk.Style()

    def update_value(self, value: float, text: str, color: str = "GREEN") -> None:
        self.configure(value=value)
        self._style_obj.configure(self._style, text=text,
                                  font=("Arial", 10, "bold"),
                                  background=color)