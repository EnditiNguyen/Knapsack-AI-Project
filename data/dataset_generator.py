import json
import random
import os

def generate_knapsack_data(n_items, capacity_ratio=0.5):
    items = []
    for i in range(n_items):
        weight = random.randint(1, 20)
        value = random.randint(10, 100)
        items.append({"name": f"Item_{i+1}", "weight": weight, "value": value})
    
    # Sức chứa túi thường bằng 50% tổng khối lượng các món đồ
    total_w = sum(it["weight"] for it in items)
    capacity = int(total_w * capacity_ratio)
    
    return {"capacity": capacity, "items": items}

# Tạo thư mục data nếu chưa có
os.makedirs('data', exist_ok=True)

# Tạo 3 bộ test
test_cases = {
    "small_10.json": 10,
    "medium_30.json": 30,
    "large_100.json": 100,
    "sample.json": 6
}

for filename, n in test_cases.items():
    data = generate_knapsack_data(n)
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f, indent=4)
