"""Все ttk.Style и layout'ы в одном месте. Вызывается один раз при старте."""
from tkinter import ttk

_STYLES_DONE = False


def init_styles() -> None:
    global _STYLES_DONE
    if _STYLES_DONE:
        return

    s = ttk.Style()

    for name in ("Label_CPU", "Labele_Ram", "Label_GPU", "Label_Ram_GPU"):
        s.layout(name, [
            (f"{name}.trough", {
                "children": [
                    (f"{name}.pbar", {"side": "left", "sticky": "ns"}),
                    (f"{name}.label", {"sticky": ""}),
                ],
                "sticky": "nswe",
            }),
        ])

    common_cfg = dict(
        thickness=15,
        troughcolor="#E0E0E0",
        bordercolor="#E0E0E0",
        lightcolor="#E0E0E0",
        darkcolor="#E0E0E0",
        troughrelief="flat",
    )

    s.configure("Label_CPU", text="CPU: 0%", font=("Arial", 10, "bold"), background="GREEN", **common_cfg)
    s.configure("Labele_Ram", text="RAM: 0%", font=("Arial", 10, "bold"), background="BLUE", **common_cfg)
    s.configure("Label_GPU", text="GPU: 0%", font=("Arial", 10, "bold"), background="GREEN", **common_cfg)
    s.configure("Label_Ram_GPU", text="0.0 / 0.0 ГБ", font=("Arial", 10, "bold"),
                background="#C5E1A5", **common_cfg)

    _STYLES_DONE = True


def disk_style_name(device: str) -> str:
    return f"Labele_Disk_{device.replace('/', '_')}"


def ensure_disk_style(device: str) -> str:
    name = disk_style_name(device)
    s = ttk.Style()
    s.layout(name, [
        (f"{name}.trough", {
            "children": [
                (f"{name}.pbar", {"side": "left", "sticky": "ns"}),
                (f"{name}.label", {"sticky": ""}),
            ],
            "sticky": "nswe",
        }),
    ])
    return name