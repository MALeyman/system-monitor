#!/home/maksim/myapp/monitor_CPU_RAM_GPU/appvenv/bin/python
import fcntl
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def _get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = _get_base_dir()
sys.path.insert(0, BASE_DIR)

# Логи и lock — в домашнюю папку, если запущено из PyInstaller-бинарника
if getattr(sys, 'frozen', False):
    log_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "monitor-cpu-ram-gpu")
    os.makedirs(log_dir, exist_ok=True)
    LOG_PATH = os.path.join(log_dir, "monitor.log")
    LOCK_PATH = os.path.join(log_dir, ".monitor.lock")
else:
    LOG_PATH = os.path.join(BASE_DIR, "monitor.log")
    LOCK_PATH = os.path.join(BASE_DIR, ".monitor.lock")

_lock_fd = None  # держим ссылку, чтобы GC не закрыл файл


def single_instance_or_die() -> None:
    """Гарантирует, что запущен только один экземпляр приложения."""
    global _lock_fd
    _lock_fd = open(LOCK_PATH, "w")
    try:
        fcntl.flock(_lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Мониторинг уже запущен.", file=sys.stderr)
        sys.exit(0)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            RotatingFileHandler(
                LOG_PATH,
                maxBytes=1_000_000,   # 1 МБ
                backupCount=3,        # monitor.log, .1, .2, .3 — итого ≤ 4 МБ
                encoding="utf-8",
            ),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # matplotlib и PIL слишком болтливы на DEBUG — глушим
    for noisy in (
        "matplotlib",
        "matplotlib.font_manager",
        "matplotlib.pyplot",
        "PIL",
        "PIL.PngImagePlugin",
    ):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def main() -> int:
    setup_logging()
    try:
        from app.application import create_app
        app = create_app()
        app.mainloop()
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception:
        logging.exception("Fatal error")
        return 1


if __name__ == "__main__":
    single_instance_or_die()
    sys.exit(main())
