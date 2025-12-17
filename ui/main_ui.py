import tkinter as tk
from tkinter import ttk, messagebox
import json
# Import logic từ thư mục algorithms
from algorithms.backtracking import Item, BranchAndBoundSolver
from algorithms.gwo import GWOSolver

class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dự án AI: Giải bài toán Cái Túi (Knapsack)")
        self.root.geometry("900x700")
        self.items = []
        self.setup_ui()

    def setup_ui(self):
        # Thiết kế bố cục chính bằng PanedWindow để có thể co giãn
        main_pane = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- KHUNG NHẬP LIỆU (TRÊN) ---
        top_frame = ttk.LabelFrame(main_pane, text=" Cấu hình bài toán ")
        main_pane.add(top_frame, weight=1)

        # Nhập Item
        item_input_frame = ttk.Frame(top_frame)
        item_input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(item_input_frame, text="Tên món:").grid(row=0, column=0, padx=5)
        self.ent_name = ttk.Entry(item_input_frame, width=15)
        self.ent_name.grid(row=0, column=1, padx=5)

        ttk.Label(item_input_frame, text="Nặng:").grid(row=0, column=2, padx=5)
        self.ent_weight = ttk.Entry(item_input_frame, width=10)
        self.ent_weight.grid(row=0, column=3, padx=5)

        ttk.Label(item_input_frame, text="Giá trị:").grid(row=0, column=4, padx=5)
        self.ent_value = ttk.Entry(item_input_frame, width=10)
        self.ent_value.grid(row=0, column=5, padx=5)

        btn_add = ttk.Button(item_input_frame, text="Thêm Item", command=self.add_item)
        btn_add.grid(row=0, column=6, padx=10)

        # Nhập Capacity & Chọn Algorithm
        config_line = ttk.Frame(top_frame)
        config_line.pack(fill=tk.X, padx=5, pady=10)

        ttk.Label(config_line, text="Sức chứa túi (W):").pack(side=tk.LEFT, padx=5)
        self.ent_capacity = ttk.Entry(config_line, width=10)
        self.ent_capacity.insert(0, "50")
        self.ent_capacity.pack(side=tk.LEFT, padx=5)

        ttk.Label(config_line, text="Thuật toán:").pack(side=tk.LEFT, padx=20)
        self.algo_var = tk.StringVar(value="Backtracking")
        self.combo_algo = ttk.Combobox(config_line, textvariable=self.algo_var, state="readonly", width=20)
        self.combo_algo['values'] = ("Backtracking", "GWO (Grey Wolf Optimizer)")
        self.combo_algo.pack(side=tk.LEFT, padx=5)

        btn_run = ttk.Button(config_line, text="CHẠY THUẬT TOÁN", command=self.run_solver)
        btn_run.pack(side=tk.LEFT, padx=30)

        btn_sample = ttk.Button(config_line, text="NẠP DỮ LIỆU MẪU", command=self.load_sample_data)
        btn_sample.pack(side=tk.LEFT, padx=5)

        # --- KHUNG DANH SÁCH & KẾT QUẢ (DƯỚI) ---
        bottom_frame = ttk.Frame(main_pane)
        main_pane.add(bottom_frame, weight=3)

        # Bảng hiển thị Items
        self.tree = ttk.Treeview(bottom_frame, columns=("Name", "Weight", "Value", "Ratio"), show='headings', height=8)
        self.tree.heading("Name", text="Tên món")
        self.tree.heading("Weight", text="Khối lượng")
        self.tree.heading("Value", text="Giá trị")
        self.tree.heading("Ratio", text="Tỷ lệ V/W")
        self.tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5)

        # Ô hiển thị kết quả
        self.txt_result = tk.Text(bottom_frame, width=40, font=("Consolas", 10), bg="#f8f9fa")
        self.txt_result.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True, padx=5)

    def add_item(self):
        try:
            name = self.ent_name.get().strip()
            w = int(self.ent_weight.get())
            v = int(self.ent_value.get())
            if not name: raise ValueError
            
            item = Item(name, w, v)
            self.items.append(item)
            self.tree.insert("", "end", values=(name, w, v, f"{item.ratio:.2f}"))
            
            self.ent_name.delete(0, tk.END)
            self.ent_weight.delete(0, tk.END)
            self.ent_value.delete(0, tk.END)
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng dữ liệu!")

    def run_solver(self):
        if not self.items:
            messagebox.showwarning("Cảnh báo", "Hãy thêm item trước!")
            return
        
        try:
            capacity = int(self.ent_capacity.get())
        except:
            messagebox.showerror("Lỗi", "Capacity phải là số nguyên!")
            return

        algo = self.algo_var.get()
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, f"Đang chạy {algo}...\n")
        
        if algo == "Backtracking":
            solver = BranchAndBoundSolver()
        else:
            solver = GWOSolver(pack_size=30, max_iter=100)

        result = solver.solve(self.items, capacity)
        
        # Hiển thị kết quả
        self.txt_result.insert(tk.END, "-"*30 + "\n")
        self.txt_result.insert(tk.END, f"TỔNG GIÁ TRỊ: {result.max_value}\n")
        self.txt_result.insert(tk.END, f"KHỐI LƯỢNG: {result.total_weight}/{capacity}\n")
        self.txt_result.insert(tk.END, f"THỜI GIAN: {result.execution_time:.6f}s\n")
        self.txt_result.insert(tk.END, "VẬT PHẨM CHỌN:\n")
        for i in result.selected_items:
            self.txt_result.insert(tk.END, f" > {i.name}\n")
    
    def load_sample_data(self):
        file_path = 'data/sample.json'
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file: {file_path}")
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Bước 1: Xóa dữ liệu cũ trên bảng và trong bộ nhớ
            self.items = []
            for row in self.tree.get_children():
                self.tree.delete(row)
            
        # Bước 2: Nạp dữ liệu mới từ file JSON
            for it in data['items']:
            # Lấy đúng tên, khối lượng, giá trị từ JSON
                name_from_json = it['name'] 
                w_from_json = it['weight']
                v_from_json = it['value']
            
            # Tạo đối tượng Item và thêm vào danh sách xử lý
                new_item = Item(name_from_json, w_from_json, v_from_json)
                self.items.append(new_item)
            
            # Đưa lên bảng hiển thị (Treeview)
                self.tree.insert("", "end", values=(
                    new_item.name, 
                    new_item.weight, 
                    new_item.value, 
                    f"{new_item.ratio:.2f}"
                ))
            
        # Bước 3: Cập nhật ô Capacity trên giao diện
            self.ent_capacity.delete(0, tk.END)
            self.ent_capacity.insert(0, str(data.get('capacity', 50)))
        
            self.txt_result.insert(tk.END, f"✅ Đã nạp {len(self.items)} món đồ từ kho mẫu.\n")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc dữ liệu: {str(e)}")
import os



    