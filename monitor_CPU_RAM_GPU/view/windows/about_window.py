import tkinter as tk
from tkinter import ttk


def show_about(parent: tk.Misc) -> None:
    win = tk.Toplevel(parent)
    win.title("О программе")
    win.geometry("330x150")
    win.resizable(False, False)

    bar = ttk.Frame(win)
    bar.pack(fill=tk.X)
    ttk.Button(bar, text="<< Назад", command=win.destroy).pack(side=tk.LEFT)

    box = ttk.LabelFrame(win, text="   Программа мониторинг ресурсов")
    box.pack(fill=tk.X)

    ttk.Label(box, text=(
        "     \n"
        "   Программа реализована на Python 3, с применением\n"
        "   библиотек tkinter, psutil и pynvml.\n"
        " \n"
        "              Накодил  Лейман М.А.\n"
        "              почта: makc.mon@mail.ru \n"
        "                     "
    )).pack(fill=tk.X, side=tk.LEFT)

    win.update()
    win.grab_set()
    win.protocol("WM_DELETE_WINDOW", win.destroy)