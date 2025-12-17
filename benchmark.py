import time
import pandas as pd
import json
from algorithms.backtracking import Item, BranchAndBoundSolver
from algorithms.gwo import GWOSolver

def run_benchmark():
    test_files = ['data/small_10.json', 'data/medium_30.json', 'data/large_100.json']
    results = []

    for file_path in test_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        capacity = data['capacity']
        items = [Item(it['name'], it['weight'], it['value']) for it in data['items']]
        n = len(items)
        
        # --- Chạy Backtracking (B&B) ---
        bnb_solver = BranchAndBoundSolver()
        # Lưu ý: Với n=100, Backtracking có thể rất chậm nếu không có pruning tốt
        # Ta có thể đặt giới hạn thời gian hoặc bỏ qua bộ test lớn cho Backtracking
        if n <= 30:
            res_bnb = bnb_solver.solve(items, capacity)
            results.append({
                "Dataset": f"N={n}",
                "Algorithm": "Branch & Bound",
                "Max Value": res_bnb.max_value,
                "Time (s)": res_bnb.execution_time
            })

        # --- Chạy GWO ---
        gwo_solver = GWOSolver(pack_size=30, max_iter=100)
        res_gwo = gwo_solver.solve(items, capacity)
        results.append({
            "Dataset": f"N={n}",
            "Algorithm": "GWO (AI)",
            "Max Value": res_gwo.max_value,
            "Time (s)": res_gwo.execution_time
        })

    # Xuất file CSV
    df = pd.DataFrame(results)
    df.to_csv("benchmark_results.csv", index=False)
    print("📊 Đã lưu kết quả so sánh vào file benchmark_results.csv")
    print(df)

if __name__ == "__main__":
    run_benchmark()