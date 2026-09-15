import json
import os

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SETTINGS_PATH = os.path.join(_BASE_DIR, "settings.json")


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