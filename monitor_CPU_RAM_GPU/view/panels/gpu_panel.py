import tkinter as tk
from tkinter import ttk

from common.formatting import gpu_mem_text
from common.metrics import GpuMetrics
from view.panels.base import BasePanel
from view.widgets.labeled_progressbar import LabeledProgressbar
from view.widgets.styles import init_styles


class GpuPanel(BasePanel):
    def __init__(self, master):
        super().__init__(master, "ИНДИКАТОРЫ GPU")
        self._has_gpu = True    # переключается при первом update_data
        init_styles()

    def build(self) -> None:
        self.name_label = ttk.Label(self, text="Температура GPU: ",
                                    anchor=tk.W, padding=(5, 0, 0, 0))
        self.name_label.pack(fill=tk.X, padx=2, pady=0)

        self.temp_label = ttk.Label(self, text="", anchor=tk.W, padding=(5, 0, 0, 0))
        self.temp_label.pack(fill=tk.X, padx=2, pady=0)

        self.usage_bar = LabeledProgressbar(self, style="Label_GPU")
        self.usage_bar.pack(fill=tk.X, expand=1, padx=2, pady=5)

        self.mem_bar = LabeledProgressbar(self, style="Label_Ram_GPU")
        self.mem_bar.pack(fill=tk.X, padx=2, pady=5)

        # Метка для случая «GPU нет» — скрыта по умолчанию
        self.no_gpu_label = ttk.Label(
            self,
            text="NVIDIA GPU не обнаружен",
            anchor=tk.CENTER,
            padding=(5, 10, 5, 10),
        )

        super().build()

    # ------------------------------------------------------------------
    def set_available(self, available: bool) -> None:
        """Переключает вид панели между «есть GPU» и «нет GPU»."""
        if available == self._has_gpu:
            return
        self._has_gpu = available

        if available:
            self.no_gpu_label.pack_forget()
            self.name_label.pack(fill=tk.X, padx=2, pady=0)
            self.temp_label.pack(fill=tk.X, padx=2, pady=0)
            self.usage_bar.pack(fill=tk.X, expand=1, padx=2, pady=5)
            self.mem_bar.pack(fill=tk.X, padx=2, pady=5)
        else:
            self.name_label.pack_forget()
            self.temp_label.pack_forget()
            self.usage_bar.pack_forget()
            self.mem_bar.pack_forget()
            self.no_gpu_label.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    def update_data(self, m: GpuMetrics) -> None:
        self.ensure_built()

        # Если провайдер вернул пустые метрики — считаем, что GPU нет
        is_available = (m.name not in ("N/A", "", None)
                        or m.usage > 0
                        or m.memory_total_gb > 0)

        self.set_available(is_available)
        if not is_available:
            return

        if m.temperature is not None:
            temp_str = f"{m.name}: {m.temperature}°C"
        else:
            temp_str = f"{m.name}: температура недоступна"
        self.temp_label.config(text=temp_str)

        self.usage_bar.update_value(m.usage, f"GPU: {m.usage}%", "GREEN")
        self.mem_bar.update_value(
            m.memory_percent,
            gpu_mem_text(m.memory_used_gb, m.memory_total_gb, m.memory_percent),
            "BLUE",
        )