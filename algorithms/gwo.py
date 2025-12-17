import numpy as np
import time
import random
# Import từ file backtracking cùng thư mục
try:
    from algorithms.backtracking import Item, KnapsackResult
except ImportError:
    from backtracking import Item, KnapsackResult

class GWOSolver:
    def __init__(self, pack_size=20, max_iter=100):
        self.pack_size = pack_size
        self.max_iter = max_iter

    def solve(self, items, capacity) -> KnapsackResult:
        n = len(items)
        if n == 0: return KnapsackResult(0, [], 0, 0)
        
        start_time = time.time()
        weights = np.array([it.weight for it in items])
        values = np.array([it.value for it in items])
        
        # Khởi tạo đàn sói
        positions = np.random.uniform(0, 1, (self.pack_size, n))
        alpha_pos, alpha_score = np.zeros(n), -1

        for l in range(self.max_iter):
            for i in range(self.pack_size):
                # Chuyển đổi nhị phân và tính fitness
                binary_sol = (positions[i] > 0.5).astype(int)
                tw = np.dot(binary_sol, weights)
                tv = np.dot(binary_sol, values)
                
                if tw <= capacity and tv > alpha_score:
                    alpha_score, alpha_pos = tv, positions[i].copy()

            a = 2 - l * (2 / self.max_iter)
            for i in range(self.pack_size):
                r1, r2 = random.random(), random.random()
                A, C = 2 * a * r1 - a, 2 * r2
                D = abs(C * alpha_pos - positions[i])
                positions[i] = alpha_pos - A * D
            
            positions = np.clip(positions, 0, 1)

        exec_time = time.time() - start_time
        selected_indices = np.where(alpha_pos > 0.5)[0]
        selected_items = [items[i] for i in selected_indices]
        
        return KnapsackResult(int(alpha_score), selected_items, sum(it.weight for it in selected_items), exec_time)