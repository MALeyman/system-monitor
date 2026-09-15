import collections

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MiniGraph:
    """Компактный график-полоска для встраивания в панель."""

    def __init__(self, parent, color="#FF5722", color2=None, max_points=60):
        self.max_points = max_points
        self.data = collections.deque([0.0] * max_points, maxlen=max_points)
        self.data2 = collections.deque([0.0] * max_points, maxlen=max_points) if color2 else None

        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots(figsize=(3, 0.6), dpi=80)
        self.fig.patch.set_facecolor("#1E1E1E")
        self.ax.set_facecolor("#121212")

        self.ax.set_ylim(-5, 105)
        self.ax.set_xlim(-max_points, 0)
        self.ax.axis("off")

        x = list(range(-max_points + 1, 1))
        self.line, = self.ax.plot(x, list(self.data), color=color, linewidth=1.2)

        self.line2 = None
        if self.data2 is not None:
            self.line2, = self.ax.plot(
                x, list(self.data2), color=color2, linewidth=1.2
            )

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.configure(height=40)

    def pack(self, **kwargs):
        self.canvas_widget.pack(**kwargs)

    def destroy(self):
        self.canvas_widget.destroy()

    def append_value(self, value: float) -> None:
        self.data.append(value)
        self.line.set_ydata(list(self.data))
        self.canvas.draw_idle()

    def append_value2(self, value: float) -> None:
        """Вторая линия (например, память GPU)."""
        if self.data2 is None or self.line2 is None:
            return
        self.data2.append(value)
        self.line2.set_ydata(list(self.data2))
        self.canvas.draw_idle()