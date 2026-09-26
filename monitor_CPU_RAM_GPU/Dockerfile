FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv python3-tk \
    binutils libxcb-cursor0 libgl1 libglib2.0-0 libx11-6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY . .

RUN python3 -m venv buildenv && \
    . buildenv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt pyinstaller && \
    pyinstaller --onefile --windowed \
      --name monitor-cpu-ram-gpu \
      --add-data "assets:assets" \
      --hidden-import=matplotlib.backends.backend_tkagg \
      --hidden-import=matplotlib.backends.backend_agg \
      --hidden-import=PIL \
      --hidden-import=PIL._tkinter_finder \
      --hidden-import=PIL.PngImagePlugin \
      --hidden-import=GPUtil \
      --hidden-import=pynvml \
      --hidden-import=distutils \
      --exclude-module PyQt5 \
      --exclude-module PyQt6 \
      --exclude-module PySide2 \
      --exclude-module PySide6 \
      main.py
