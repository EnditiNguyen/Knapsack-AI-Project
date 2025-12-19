import time
from abc import ABC, abstractmethod
from typing import List

class Item:
    def __init__(self, name: str, weight: float, value: float):
        self.name = name
        self.weight = weight
        self.value = value
        self.ratio = value / weight if weight > 0 else 0

    def __repr__(self):
        return f"Item({self.name}, {self.weight}kg, {self.value}$)"

class KnapsackResult:
    def __init__(self, max_value: float, selected_items: List[Item], 
                 total_weight: float, execution_time: float):
        self.max_value = max_value
        self.selected_items = selected_items
        self.total_weight = total_weight
        self.execution_time = execution_time

class KnapsackSolver(ABC):
    @abstractmethod
    def solve(self, items: List[Item], capacity: float) -> KnapsackResult:
        pass