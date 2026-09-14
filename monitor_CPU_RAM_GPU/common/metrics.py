"""DTO-метрики: явный интерфейс между providers и view."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CpuMetrics:
    usage: float = 0.0
    temperature: float | None = None
    cores: list[float] = field(default_factory=list)


@dataclass(frozen=True)
class RamMetrics:
    percent: float = 0.0
    used_gb: float = 0.0
    total_gb: float = 0.0


@dataclass(frozen=True)
class GpuMetrics:
    name: str = "N/A"
    usage: float = 0.0
    memory_percent: float = 0.0
    memory_used_gb: float = 0.0
    memory_total_gb: float = 0.0
    temperature: float | None = None


@dataclass(frozen=True)
class DiskMetrics:
    device: str = ""
    fstype: str = ""
    percent: float = 0.0
    used_gb: float = 0.0
    total_gb: float = 0.0
    temperature: int | None = None