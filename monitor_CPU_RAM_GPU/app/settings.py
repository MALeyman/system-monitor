import json
import os
import sys


def _get_settings_path():
    # Если запущено из PyInstaller — пишем в ~/.config
    if getattr(sys, 'frozen', False):
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "monitor-cpu-ram-gpu")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "settings.json")
    # Иначе — рядом с проектом
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "settings.json")


_SETTINGS_PATH = _get_settings_path()


class _Settings:
    def __init__(self) -> None:
        self.show_graphs: bool = False
        self.load()

    def load(self) -> None:
        try:
            with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.show_graphs = bool(data.get("show_graphs", False))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save(self) -> None:
        try:
            with open(_SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump({"show_graphs": self.show_graphs}, f, indent=2)
        except OSError:
            pass


settings = _Settings()
