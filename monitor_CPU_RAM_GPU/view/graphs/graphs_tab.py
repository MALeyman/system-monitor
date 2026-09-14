from tkinter import ttk

from view.graphs.history_graph import HistoryGraph


class GraphsTab:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill="both", expand=True)

        self.cpu_graph = HistoryGraph(self.frame, title="История загрузки ЦП (%)", color="#FF5722")
        self.ram_graph = HistoryGraph(self.frame, title="История загрузки памяти (%)", color="#00BCD4")
        self.gpu_graph = HistoryGraph(self.frame, title="История загрузки GPU (%)", color="#4CAF50")

    def update_graphs(self, cpu_val: float, ram_val: float, gpu_val: float) -> None:
        self.cpu_graph.append_value(cpu_val)
        self.ram_graph.append_value(ram_val)
        self.gpu_graph.append_value(gpu_val)

    def set_gpu_visible(self, visible: bool) -> None:
        """Скрывает/показывает график GPU."""
        if visible:
            self.gpu_graph.canvas_widget.pack(fill="both", expand=True, padx=5, pady=5)
        else:
            self.gpu_graph.canvas_widget.pack_forget()