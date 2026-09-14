import psutil

from common.formatting import gb
from common.metrics import RamMetrics


class RamProvider:
    def read(self) -> RamMetrics:
        vm = psutil.virtual_memory()
        return RamMetrics(
            percent=vm.percent,
            used_gb=gb(vm.used),
            total_gb=gb(vm.total),
        )