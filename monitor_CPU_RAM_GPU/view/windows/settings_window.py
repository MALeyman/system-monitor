import tkinter as tk
from tkinter import ttk

from app.settings import settings


def show_settings(parent: tk.Misc) -> None:
    win = tk.Toplevel(parent)
    win.title("Настройки")
    win.geometry("320x140")
    win.resizable(False, False)

    bar = ttk.Frame(win)
    bar.pack(fill=tk.X)
    ttk.Button(bar, text="<< Назад", command=win.destroy).pack(side=tk.LEFT)

    box = ttk.LabelFrame(win, text="   Отображение")
    box.pack(fill=tk.X, padx=5, pady=5)

    var = tk.BooleanVar(value=settings.show_graphs)

    cb = ttk.Checkbutton(
        box,
        text="Показывать графики рядом с прогрессбарами",
        variable=var,
        command=lambda: _on_toggle(var.get()),
    )
    cb.pack(anchor=tk.W, padx=5, pady=5)

    win.update()
    win.grab_set()
    win.protocol("WM_DELETE_WINDOW", win.destroy)


def _on_toggle(value: bool) -> None:
    settings.show_graphs = value
    settings.save()
    # Сообщаем главному окну, что настройка изменилась
    root = tk._default_root
    if root is not None and hasattr(root, "apply_settings"):
        root.apply_settings()