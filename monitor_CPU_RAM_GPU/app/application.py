from app.controller import AppController
from view.windows.main_window import MainWindow


def create_app() -> MainWindow:
    """Собирает окно и контроллер, запускает refresh loop."""
    window = MainWindow(controller=None)
    controller = AppController(window)
    window.controller = controller
    if hasattr(controller, "set_page"):
        controller.set_page(0)
    controller.start()
    return window
