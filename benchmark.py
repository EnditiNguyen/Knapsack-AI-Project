import pandas as pd
import time
import json
import os
from algorithms.backtracking import BranchAndBoundSolver
from algorithms.gwo import GWOSolver
from algorithms.base import Item

def run_benchmark_on_existing_data():
    # Danh sách các file dữ liệu mẫu của bạn
    # Bạn có thể đổi tên cho đúng với file thực tế trong thư mục data/
    target_files = ["small_10.json", "medium_30.json", "large_100.json"]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    results = []

    for filename in target_files:
        file_path = os.path.join(data_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"⚠️ Không tìm thấy file: {filename}, bỏ qua...")
            continue

        # 1. Đọc dữ liệu từ JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = [Item(it['name'], it['weight'], it['value']) for it in data['items']]
            capacity = data['capacity']
            num_items = len(items)

        print(f"🚀 Đang benchmark bộ dữ liệu: {filename} ({num_items} items)...")

        # 2. Chạy Backtracking (Lưu ý: 100 items Backtracking có thể rất lâu, nên giới hạn)
        res_bt_value = 0
        res_bt_time = 0
        if num_items <= 30: # Chỉ chạy BT cho các bộ dữ liệu nhỏ để tránh treo máy
            bt_solver = BranchAndBoundSolver()
            start = time.time()
            res_bt = bt_solver.solve(items, capacity)
            res_bt_time = time.time() - start
            res_bt_value = res_bt.max_value
        else:
            res_bt_value = "N/A (Too large)"
            res_bt_time = 0

        # 3. Chạy GWO
        gwo_solver = GWOSolver(pack_size=50, max_iter=200)
        start = time.time()
        res_gwo = gwo_solver.solve(items, capacity)
        res_gwo_time = time.time() - start

        # 4. Lưu kết quả
        accuracy = 100
        if isinstance(res_bt_value, (int, float)) and res_bt_value > 0:
            accuracy = (res_gwo.max_value / res_bt_value) * 100

        results.append({
            "Source_File": filename,
            "Num_Items": num_items,
            "BT_Value": res_bt_value,
            "BT_Time": res_bt_time,
            "GWO_Value": res_gwo.max_value,
            "GWO_Time": res_gwo_time,
            "Accuracy": accuracy
        })

    # Xuất ra file CSV
    df = pd.DataFrame(results)
    output_path = os.path.join(data_dir, "benchmark_results.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Đã lưu kết quả benchmark vào: {output_path}")
    return output_path