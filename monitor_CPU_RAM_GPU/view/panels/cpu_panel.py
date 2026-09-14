import tkinter as tk
from tkinter import ttk

from common.metrics import CpuMetrics
from view.panels.base import BasePanel
from view.widgets.labeled_progressbar import LabeledProgressbar
from view.widgets.styles import init_styles


class CpuPanel(BasePanel):
    def __init__(self, master):
        super().__init__(master, "ИНДИКАТОРЫ CPU")
        init_styles()

    def build(self) -> None:
        self.temp_label = ttk.Label(self, text="", anchor=tk.W, padding=(0, 0, 0, 0))
        self.temp_label.pack(fill=tk.X, padx=2, pady=0)

        self.bar = LabeledProgressbar(self, style="Label_CPU")
        self.bar.pack(fill=tk.X, expand=1, padx=2, pady=5)
        super().build()

    def update_data(self, m: CpuMetrics) -> None:
        self.ensure_built()
        self.temp_label.config(text=f"Температура CPU: {m.temperature}°C"
                                     if m.temperature is not None else "Температура CPU: N/A")
        self.bar.update_value(m.usage, f"CPU:  {m.usage}% ", "GREEN")