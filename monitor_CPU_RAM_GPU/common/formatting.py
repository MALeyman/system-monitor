"""Хелперы форматирования текста."""


def gb(value_bytes: float) -> float:
    return round(value_bytes / (1024 ** 3), 2)


def gpu_mem_text(used_gb: float, total_gb: float, percent: float) -> str:
    return f"{used_gb:.1f} ГБ / {total_gb:.1f} ГБ ({percent}%)"


def ram_text(used_gb: float, total_gb: float, percent: float) -> str:
    return f" {used_gb:.1f} ГБ / {total_gb:.1f} ГБ ({percent}%)"


def disk_text(used_gb: float, total_gb: float) -> str:
    return f"{used_gb} / {total_gb} ГБ"


def temp_text(value: int | float | None) -> str:
    return f"{value}°C" if value not in (None, "N/A") else "N/A"