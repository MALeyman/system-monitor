from common.formatting import ram_text
from common.metrics import RamMetrics
from view.panels.base import BasePanel
from view.widgets.labeled_progressbar import LabeledProgressbar
from view.widgets.styles import init_styles
from view.graphs.mini_graph import MiniGraph


class RamPanel(BasePanel):
    def __init__(self, master):
        super().__init__(master, "ИНДИКАТОРЫ RAM")
        self._graph = None
        init_styles()

    def build(self) -> None:
        self.bar = LabeledProgressbar(self, style="Labele_Ram")
        self.bar.pack(fill="x", expand=1, padx=2, pady=5)
        super().build()

    def set_graph_visible(self, visible: bool) -> None:
        if visible and self._graph is None:
            self._graph = MiniGraph(self, color="#00BCD4")
            self._graph.pack(fill="x", padx=2, pady=(0, 5))
        elif not visible and self._graph is not None:
            self._graph.destroy()
            self._graph = None

    def update_data(self, m: RamMetrics) -> None:
        self.ensure_built()
        self.bar.update_value(m.percent, ram_text(m.used_gb, m.total_gb, m.percent), "#00BCD4")
        if self._graph is not None:
            self._graph.append_value(m.percent)