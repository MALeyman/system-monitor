from tkinter import ttk

from common.formatting import disk_text, temp_text
from common.metrics import DiskMetrics
from view.panels.base import BasePanel
from view.widgets.labeled_progressbar import LabeledProgressbar
from view.widgets.styles import ensure_disk_style


class DiskPanel(BasePanel):
    def __init__(self, master):
        super().__init__(master, "ИНДИКАТОРЫ НАКОПИТЕЛЕЙ")
        self._widgets: dict[str, tuple[ttk.Label, LabeledProgressbar]] = {}

    def build(self) -> None:
        # виджеты создаются динамически в update_data
        super().build()

    def update_data(self, metrics: list[DiskMetrics]) -> None:
        self.ensure_built()

        current = {m.device for m in metrics}

        # удалить исчезнувшие
        for device in set(self._widgets) - current:
            label, bar = self._widgets.pop(device)
            label.destroy()
            bar.destroy()

        for m in metrics:
            if m.device not in self._widgets:
                style_name = ensure_disk_style(m.device)
                label = ttk.Label(self, text="")
                bar = LabeledProgressbar(self, style=style_name)
                label.pack(fill="x", padx=2, pady=0)
                bar.pack(fill="x", padx=2, pady=0)
                self._widgets[m.device] = (label, bar)

            label, bar = self._widgets[m.device]
            label.config(text=f"{m.device} ({m.fstype}) :  {temp_text(m.temperature)}")
            bar.update_value(m.percent, disk_text(m.used_gb, m.total_gb), "GREEN")