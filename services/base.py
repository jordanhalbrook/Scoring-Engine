from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ServiceResult:
    name: str
    success: bool
    message: str
    timestamp: datetime
    evidence: str | None = None

class ServiceCheck(ABC):
    def __init__(self, name: str, points: int):
        self.name = name
        self.points = points

        @abstractmethod
        def run_check(self) -> ServiceResult:
            pass
