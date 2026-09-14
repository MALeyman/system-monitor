import collections

import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class HistoryGraph:
    def __init__(self, parent_frame, title, color="#FF5722", max_points=60):
        self.max_points = max_points
        self.data = collections.deque([0.0] * max_points, maxlen=max_points)
        self.x_values = list(range(-max_points + 1, 1))

        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots(figsize=(4, 1.3), dpi=100)
        self.fig.patch.set_facecolor("#1E1E1E")
        self.ax.set_facecolor("#121212")

        self.ax.grid(True, color="#2C2C2C", linestyle="-", linewidth=0.5)
        self.ax.set_ylim(-5, 105)
        self.ax.set_xlim(-max_points, 0)
        self.ax.set_title(title, fontsize=10, loc="left", color="#AAAAAA", pad=8)

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.line, = self.ax.plot(self.x_values, list(self.data), color=color, linewidth=1.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def append_value(self, new_value: float) -> None:
        self.data.append(new_value)
        self.line.set_ydata(list(self.data))
        self.canvas.draw_idle()