import time
from typing import List
try:
    from algorithms.base import Item, KnapsackResult, KnapsackSolver
except ImportError:
    from base import Item, KnapsackResult, KnapsackSolver

class BranchAndBoundSolver(KnapsackSolver):
    def solve(self, items: List[Item], capacity: float) -> KnapsackResult:
        # Sắp xếp vật phẩm theo tỷ lệ giá trị/khối lượng giảm dần để cắt nhánh hiệu quả
        self.items = sorted(items, key=lambda x: x.ratio, reverse=True)
        self.capacity = capacity
        self.n = len(self.items)
        self.best_value = 0
        self.best_items = []
        
        start_time = time.time()
        self._bnb(0, 0, 0, []) # Bắt đầu quay lui từ vật phẩm đầu tiên
        exec_time = time.time() - start_time
        
        return KnapsackResult(
            max_value=self.best_value,
            selected_items=self.best_items,
            total_weight=sum(i.weight for i in self.best_items),
            execution_time=exec_time
        )

    def _bound(self, index, current_weight, current_value):
        if current_weight >= self.capacity: return 0
        bound_val = current_value
        total_w = current_weight
        # Lấy đầy các vật phẩm còn lại theo kiểu tham lam
        j = index
        while j < self.n and total_w + self.items[j].weight <= self.capacity:
            total_w += self.items[j].weight
            bound_val += self.items[j].value
            j += 1
        # Lấy thêm phần lẻ của vật phẩm tiếp theo (Fractional part)
        if j < self.n:
            bound_val += (self.capacity - total_w) * self.items[j].ratio
        return bound_val

    def _bnb(self, index, current_weight, current_value, current_items):
        # Điều kiện dừng: Duyệt hết vật phẩm
        if index == self.n:
            if current_value > self.best_value:
                self.best_value = current_value
                self.best_items = list(current_items)
            return

        # KỸ THUẬT CẮT NHÁNH: Nếu cận trên không tốt hơn kỷ lục cũ thì bỏ qua
        if self._bound(index, current_weight, current_value) <= self.best_value:
            return

        # Nhánh 1: Chọn vật phẩm hiện tại
        item = self.items[index]
        if current_weight + item.weight <= self.capacity:
            current_items.append(item)
            self._bnb(index + 1, current_weight + item.weight, current_value + item.value, current_items)
            current_items.pop()

        # Nhánh 2: Không chọn vật phẩm hiện tại
        self._bnb(index + 1, current_weight, current_value, current_items)