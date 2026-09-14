"""Роутинг вкладок. Держим отдельно, чтобы Application не разрастался."""

PAGE_MAIN = 0
PAGE_MIN = 1
PAGE_CPU = 2
PAGE_DISK = 3
PAGE_GPU = 4
PAGE_GRAPHS = 5

# какие данные обновлять на какой странице
PAGE_NEEDS = {
    PAGE_MAIN:   {"cpu", "ram", "gpu", "disk"},
    PAGE_MIN:    {"cpu", "ram"},
    PAGE_CPU:    {"cpu"},
    PAGE_DISK:   {"disk"},
    PAGE_GPU:    {"gpu"},
    PAGE_GRAPHS: {"cpu", "ram", "gpu"},
}