import tkinter as tk
from tkinter import ttk
import sys
import os

from app.settings import settings
from view.panels.cpu_panel import CpuPanel
from view.panels.ram_panel import RamPanel
from view.panels.gpu_panel import GpuPanel
from view.panels.disk_panel import DiskPanel
from view.panels.graphs_panel import GraphsPanel
from view.widgets.styles import init_styles


class MainWindow(tk.Tk):
    """Только UI: сборка панелей и роутинг. Никаких данных."""

    PAGES = ("Основное", "Мин", "CPU", "Накопители", "GPU", "Графика")

    def __init__(self, controller):
        # Разные WMClass для разных режимов запуска
        if getattr(sys, 'frozen', False):
            wm_class = "MonitorCpuRamGpu"       # из .deb (PyInstaller)
        else:
            wm_class = "MonitorCpuRamGpuDev"    # из исходников (dev)
    
        super().__init__(className=wm_class)
        self.controller = controller

        try:
            self.iconphoto(True, tk.PhotoImage(file=_resource_path("assets/icon.png")))
        except Exception:
            pass

        self.title("Мониторинг")
                
        self.attributes("-alpha", 0.9)
        self.attributes("-topmost", False)
        self.overrideredirect(False)
        self.resizable(True, True)
        self.minsize(200, 100)
        self.maxsize(600, 1200)

        init_styles()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # панели создаём один раз
        self.cpu_panel = CpuPanel(self)
        self.ram_panel = RamPanel(self)
        self.gpu_panel = GpuPanel(self)
        self.disk_panel = DiskPanel(self)
        self.graphs_panel = GraphsPanel(self)

        # верхняя строка
        self.header = ttk.Frame(self)
        self.header.pack(fill=tk.X)

        self.combo = ttk.Combobox(self.header, values=self.PAGES, width=11, state="readonly")
        self.combo.current(0)
        self.combo.pack(side=tk.LEFT)
        self.combo.bind("<<ComboboxSelected>>", self._on_page)

        # ttk.Button(self.header, text="О программе",
        #            command=self._about).pack(side=tk.LEFT)
        self._build_menu()

        self.show_page(0)
        self._update_graphs_visibility()


    def _on_close(self) -> None:
        if getattr(self, "controller", None):
            self.controller.stop()
        graphs_panel = getattr(self, "graphs_panel", None)
        graphs = getattr(graphs_panel, "graphs", None) if graphs_panel else None
        if graphs:
            try: graphs.close()
            except Exception: pass
        self.destroy()
        self.quit()

    def _resource_path(relative):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), relative)


    def _build_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Настройки", command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="О программе", command=self._about)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self._on_close)

        menubar.add_cascade(label="Меню", menu=file_menu)
        self.config(menu=menubar)

    def _open_settings(self) -> None:
        from view.windows.settings_window import show_settings
        show_settings(self)

    def apply_settings(self) -> None:
        """Вызывается после изменения настроек."""
        self._update_graphs_visibility()

    def _update_graphs_visibility(self) -> None:
        """Показывает/скрывает мини-графики рядом с прогрессбарами."""
        show = settings.show_graphs
        for panel in (self.cpu_panel, self.ram_panel, self.gpu_panel):
            if hasattr(panel, "set_graph_visible"):
                panel.set_graph_visible(show)



    # -------- роутинг --------
    def _on_page(self, event=None) -> None:
        self.show_page(self.combo.current())


    def show_page(self, index: int) -> None:
        for panel in (self.cpu_panel, self.ram_panel, self.gpu_panel,
                    self.disk_panel, self.graphs_panel):
            panel.pack_forget()

        if index == 0:      # Основное
            self.geometry("280x600")
            self.cpu_panel.pack(fill=tk.Y)
            self.ram_panel.pack(fill=tk.Y)
            self.gpu_panel.pack(fill=tk.Y)
            self.disk_panel.pack(fill=tk.Y)
        elif index == 1:    # Мин
            self.geometry("260x130")
            self.cpu_panel.pack(fill=tk.X)
            self.ram_panel.pack(fill=tk.X)
        elif index == 2:    # CPU
            self.geometry("280x160")
            self.cpu_panel.pack(fill=tk.Y)
        elif index == 3:    # Накопители
            self.geometry("320x300")
            self.disk_panel.pack(fill=tk.Y)
        elif index == 4:    # GPU
            self.geometry("280x200")
            self.gpu_panel.pack(fill=tk.Y)
        elif index == 5:    # Графика
            self.geometry("380x600")
            self.graphs_panel.pack(fill=tk.BOTH, expand=True)

        # ВАЖНО: контроллер может быть ещё не привязан при первом показе
        if getattr(self, "controller", None) is not None:
            self.controller.set_page(index)



    def _about(self) -> None:
        from view.windows.about_window import show_about
        show_about(self)

    # -------- хук для контроллера --------
    def render(self, page_index: int,
               cpu, ram, gpu, disks) -> None:
        """Вызывается контроллером каждый тик."""
        if page_index == 5:
            self.graphs_panel.update_data((cpu, ram, gpu))
            return

        # Основное / CPU
        if page_index in (0, 1, 2):
            self.cpu_panel.update_data(cpu)
            self.ram_panel.update_data(ram)
        # Основное / GPU
        if page_index in (0, 1, 4):
            self.gpu_panel.update_data(gpu)
        # Основное / Накопители
        if page_index in (0, 3):
            self.disk_panel.update_data(disks)
