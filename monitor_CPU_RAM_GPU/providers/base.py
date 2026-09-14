"""Protocol провайдера метрик."""
from typing import Protocol, Any


class MetricsProvider(Protocol):
    def read(self) -> Any: ...