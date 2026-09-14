from common.formatting import ram_text
from common.metrics import RamMetrics
from view.panels.base import BasePanel
from view.widgets.labeled_progressbar import LabeledProgressbar
from view.widgets.styles import init_styles


class RamPanel(BasePanel):
    def __init__(self, master):
        super().__init__(master, "ИНДИКАТОРЫ RAM")
        init_styles()

    def build(self) -> None:
        self.bar = LabeledProgressbar(self, style="Labele_Ram")
        self.bar.pack(fill="x", expand=1, padx=2, pady=5)
        super().build()

    def update_data(self, m: RamMetrics) -> None:
        self.ensure_built()
        self.bar.update_value(m.percent, ram_text(m.used_gb, m.total_gb, m.percent), "BLUE")