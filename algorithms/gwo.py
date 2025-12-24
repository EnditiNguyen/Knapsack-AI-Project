import numpy as np
import time
import random
from typing import List
try:
    from algorithms.base import Item, KnapsackResult, KnapsackSolver
except ImportError:
    from base import Item, KnapsackResult, KnapsackSolver

class GWOSolver(KnapsackSolver):
    def __init__(self, pack_size: int = 50, max_iter: int = 200):
        self.pack_size = pack_size
        self.max_iter = max_iter

    def _sigmoid(self, x):
        x = np.clip(x, -10, 10)
        return 1 / (1 + np.exp(-x))

    def solve(self, items: List[Item], capacity: float) -> KnapsackResult:
        n = len(items)
        if n == 0: return KnapsackResult(0, [], 0, 0)
        
        start_time = time.time()
        weights = np.array([it.weight for it in items])
        values = np.array([it.value for it in items])
        # Khởi tạo quần thể sói (vị trí ngẫu nhiên từ -3 đến 3)
        positions = np.random.uniform(-3, 3, (self.pack_size, n))
        
        alpha_pos, alpha_score = np.zeros(n), -float('inf')
        beta_pos, beta_score = np.zeros(n), -float('inf')
        delta_pos, delta_score = np.zeros(n), -float('inf')

        for l in range(self.max_iter):
            for i in range(self.pack_size):
                # 1. Chuyển vị trí liên tục sang nhị phân 0/1
                s_v = self._sigmoid(positions[i])
                binary_sol = (s_v > random.random()).astype(int)
                # 2. Tính toán Fitness kèm Hàm Phạt
                tw = np.dot(binary_sol, weights)
                tv = np.dot(binary_sol, values)
                # Hàm phạt: Trừ điểm nặng nếu vượt sức chứa
                fitness = tv if tw <= capacity else tv - (tw - capacity) * 1000

                # Cập nhật Alpha, Beta, Delta (3 nghiệm tốt nhất)
                if fitness > alpha_score:
                    alpha_score, alpha_pos = fitness, positions[i].copy()
                elif fitness > beta_score:
                    beta_score, beta_pos = fitness, positions[i].copy()
                elif fitness > delta_score:
                    delta_score, delta_pos = fitness, positions[i].copy()
            # Cập nhật vị trí bầy sói theo 3 con đầu đàn
            a = 2 - l * (2 / self.max_iter) # Giảm dần từ 2 về 0
            for i in range(self.pack_size):
                # Tính toán X1, X2, X3 dựa trên Alpha, Beta, Delta
                x_new = np.zeros(n)
                for target_pos in [alpha_pos, beta_pos, delta_pos]:
                    r1, r2 = np.random.random(n), np.random.random(n)
                    A = 2 * a * r1 - a
                    C = 2 * r2
                    D = np.abs(C * target_pos - positions[i])
                    x_new += (target_pos - A * D)
                
                positions[i] = x_new / 3
            positions = np.clip(positions, -3, 3)

        # Trích xuất kết quả và sửa lỗi nếu còn vượt sức chứa
        final_binary = (self._sigmoid(alpha_pos) > 0.5).astype(int)
        selected_items = [items[i] for i in range(n) if final_binary[i] == 1]
        
        total_w = sum(it.weight for it in selected_items)
        if total_w > capacity:
            selected_items.sort(key=lambda x: x.ratio)
            while total_w > capacity and selected_items:
                removed = selected_items.pop(0)
                total_w -= removed.weight

        return KnapsackResult(
            max_value=sum(it.value for it in selected_items),
            selected_items=selected_items,
            total_weight=total_w,
            execution_time=time.time() - start_time
        )