import time
from abc import ABC, abstractmethod
from typing import List

# Lớp Item phải được định nghĩa ở đây
class Item:
    def __init__(self, name: str, weight: int, value: int):
        self.name = name
        self.weight = weight
        self.value = value
        self.ratio = value / weight if weight > 0 else 0

    def __repr__(self):
        return f"Item({self.name}, {self.weight}kg, {self.value}$)"

# Lớp kết quả trả về
class KnapsackResult:
    def __init__(self, max_value: int, selected_items: List[Item], total_weight: int, execution_time: float):
        self.max_value = max_value
        self.selected_items = selected_items
        self.total_weight = total_weight
        self.execution_time = execution_time

# Thuật toán Nhánh cận (Branch and Bound)
class BranchAndBoundSolver:
    def solve(self, items: List[Item], capacity: int) -> KnapsackResult:
        # Sắp xếp theo tỷ lệ giá trị/khối lượng
        self.items = sorted(items, key=lambda x: x.ratio, reverse=True)
        self.capacity = capacity
        self.n = len(self.items)
        self.best_value = 0
        self.best_items = []
        
        start_time = time.time()
        self._bnb(0, 0, 0, [])
        exec_time = time.time() - start_time
        
        return KnapsackResult(
            self.best_value, 
            self.best_items, 
            sum(i.weight for i in self.best_items),
            exec_time
        )

    def _bound(self, index, current_weight, current_value):
        if current_weight >= self.capacity:
            return 0
        bound_val = current_value
        total_w = current_weight
        j = index
        while j < self.n and total_w + self.items[j].weight <= self.capacity:
            total_w += self.items[j].weight
            bound_val += self.items[j].value
            j += 1
        if j < self.n:
            bound_val += (self.capacity - total_w) * self.items[j].ratio
        return bound_val

    def _bnb(self, index, current_weight, current_value, current_items):
        if self._bound(index, current_weight, current_value) <= self.best_value:
            return
        if index == self.n:
            if current_value > self.best_value:
                self.best_value = current_value
                self.best_items = list(current_items)
            return
        item = self.items[index]
        if current_weight + item.weight <= self.capacity:
            current_items.append(item)
            self._bnb(index + 1, current_weight + item.weight, current_value + item.value, current_items)
            current_items.pop()
        self._bnb(index + 1, current_weight, current_value, current_items)