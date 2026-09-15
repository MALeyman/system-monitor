import tkinter as tk
from tkinter import ttk

from common.metrics import CpuMetrics
from view.panels.base import BasePanel
from view.widgets.labeled_progressbar import LabeledProgressbar
from view.widgets.styles import init_styles
from view.graphs.mini_graph import MiniGraph


class CpuPanel(BasePanel):
    def __init__(self, master):
        super().__init__(master, "ИНДИКАТОРЫ CPU")
        self._graph = None
        init_styles()

    def build(self) -> None:
        self.temp_label = ttk.Label(self, text="", anchor=tk.W, padding=(0, 0, 0, 0))
        self.temp_label.pack(fill=tk.X, padx=2, pady=0)

        row = ttk.Frame(self)
        row.pack(fill=tk.X, expand=1, padx=2, pady=5)

        self.bar = LabeledProgressbar(row, style="Label_CPU")
        self.bar.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # Мини-график создаётся лениво, когда его включат
        super().build()

    def set_graph_visible(self, visible: bool) -> None:
        if visible and self._graph is None:
            self._graph = MiniGraph(self, color="#FF5722")
            self._graph.pack(fill=tk.X, padx=2, pady=(0, 5))
        elif not visible and self._graph is not None:
            self._graph.destroy()
            self._graph = None

    def update_data(self, m: CpuMetrics) -> None:
        self.ensure_built()
        self.temp_label.config(
            text=f"Температура CPU: {m.temperature}°C"
            if m.temperature is not None else "Температура CPU: N/A"
        )
        self.bar.update_value(m.usage, f"CPU:  {m.usage}% ", "GREEN")
        if self._graph is not None:
            self._graph.append_value(m.usage)