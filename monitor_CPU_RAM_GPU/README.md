# Monitor CPU RAM GPU

Приложение для мониторинга ресурсов системы: **CPU**, **RAM**, **GPU**, **диски** и **температуры**.

Написано на Python 3 с использованием Tkinter, psutil, matplotlib, pynvml.

![Скриншот](docs/screenshot.png)

## Возможности

- 📊 Загрузка **CPU** (общая + по ядрам), температура
- 💾 Использование **RAM** (в ГБ и %)
- 🎮 Метрики **NVIDIA GPU** (загрузка, память, температура)
- 💿 Информация о **дисках** (объём, файловая система, температура SMART)
- 📈 **Графики истории** загрузки CPU / RAM / GPU
- 🌙 Тёмная тема, компактный интерфейс
- ⚙️ Настройки отображения графиков

## Установка

### Ubuntu 22.04 / 24.04 / 26.04

```bash
# Скачать .deb
wget https://github.com/USERNAME/monitor-cpu-ram-gpu/releases/latest/download/monitor-cpu-ram-gpu_1.0.0_amd64.deb

# Установить
sudo apt install ./monitor-cpu-ram-gpu_1.0.0_amd64.deb

# Удалить
sudo apt remove monitor-cpu-ram-gpu

# Ручная установка зависимостей (если не установилось автоматически)
sudo apt install lm-sensors smartmontools nvme-cli
sudo sensors-detect --auto
