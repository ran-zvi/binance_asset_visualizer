from dataclasses import dataclass
from typing import Callable


@dataclass
class DataField:
    name: str
    type: Callable
