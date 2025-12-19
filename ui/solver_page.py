import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
from algorithms.base import Item
from algorithms.backtracking import BranchAndBoundSolver
from algorithms.gwo import GWOSolver
from ui.components import ItemForm

class SolverPage(tk.Frame):
    def __init__(self, parent, data_path):
        super().__init__(parent, bg="#f0f2f5")
        self.data_path = data_path
        self.items = []
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Layout 2 cột
        container = tk.Frame(self, bg="#f0f2f5", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # CỘT TRÁI
        left_f = tk.Frame(container, bg="#f0f2f5")
        left_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.form = ItemForm(left_f, self.add_item, self.update_item, self.delete_item)
        self.form.pack(fill=tk.X, pady=(0, 15))

        # Bảng dữ liệu
        self.tree = ttk.Treeview(left_f, columns=("N", "W", "V", "R"), show="headings")
        for col, head in zip(("N", "W", "V", "R"), ("Tên vật phẩm", "Nặng (kg)", "Giá ($)", "Tỉ lệ")):
            self.tree.heading(col, text=head)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # CỘT PHẢI
        right_f = tk.Frame(container, bg="#f0f2f5", width=350)
        right_f.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_f.pack_propagate(False)

        config_f = tk.LabelFrame(right_f, text=" ⚙️ Cấu hình ", bg="white", padx=15, pady=15, font=('Segoe UI', 11, 'bold'))
        config_f.pack(fill=tk.X)

        tk.Label(config_f, text="Sức chứa túi:", bg="white").pack(anchor="w")
        self.ent_cap = tk.Entry(config_f, font=('Segoe UI', 12, 'bold'), fg="#d93025")
        self.ent_cap.insert(0, "50")
        self.ent_cap.pack(fill=tk.X, pady=5)

        # GWO Params
        gwo_p = tk.Frame(config_f, bg="#f8f9fa", pady=10)
        gwo_p.pack(fill=tk.X, pady=10)
        tk.Label(gwo_p, text="Sói:").grid(row=0, column=0); self.ent_pop = tk.Entry(gwo_p, width=7); self.ent_pop.insert(0, "50"); self.ent_pop.grid(row=0, column=1)
        tk.Label(gwo_p, text=" Lặp:").grid(row=0, column=2); self.ent_iter = tk.Entry(gwo_p, width=7); self.ent_iter.insert(0, "200"); self.ent_iter.grid(row=0, column=3)

        self.btn_gwo = tk.Button(config_f, text="🐺 CHẠY GWO AI", bg="#1e8e3e", fg="white", font=('Segoe UI', 10, 'bold'), command=lambda: self.run_solve("GWO"), pady=8)
        self.btn_gwo.pack(fill=tk.X, pady=2)
        
        self.btn_bt = tk.Button(config_f, text="🌳 CHẠY BACKTRACKING", bg="#a142f4", fg="white", font=('Segoe UI', 10, 'bold'), command=lambda: self.run_solve("BT"), pady=8)
        self.btn_bt.pack(fill=tk.X, pady=2)

        self.txt_res = tk.Text(right_f, bg="#202124", fg="#81c995", font=("Consolas", 10), padx=10, pady=10)
        self.txt_res.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

    # --- LOGIC DỮ LIỆU ---
    def load_data(self):
        if not os.path.exists(self.data_path):
            self.items = [Item("Laptop", 3, 1500), Item("Sách", 1, 20), Item("Điện thoại", 0.5, 1000)]
            self.save_data()
        else:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.ent_cap.delete(0, tk.END); self.ent_cap.insert(0, str(data.get('capacity', 50)))
                self.items = [Item(i['name'], i['weight'], i['value']) for i in data.get('items', [])]
        self.refresh_table()

    def save_data(self):
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        data = {"capacity": float(self.ent_cap.get() or 50), "items": [{"name": i.name, "weight": i.weight, "value": i.value} for i in self.items]}
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def refresh_table(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        for i in self.items: self.tree.insert("", "end", values=(i.name, i.weight, i.value, f"{i.ratio:.2f}"))

    def add_item(self):
        try:
            v = [e.get() for e in self.form.entries]
            self.items.append(Item(v[0], float(v[1]), float(v[2])))
            self.refresh_table(); self.save_data()
        except: messagebox.showerror("Lỗi", "Nhập số hợp lệ")

    def on_select(self, e):
        sel = self.tree.selection()
        if not sel: return
        item = self.items[self.tree.index(sel[0])]
        for i, val in enumerate([item.name, item.weight, item.value]):
            self.form.entries[i].delete(0, tk.END); self.form.entries[i].insert(0, str(val))
        self.form.btn_up.config(state="normal"); self.form.btn_add.config(state="disabled")

    def update_item(self):
        idx = self.tree.index(self.tree.selection()[0])
        v = [e.get() for e in self.form.entries]
        self.items[idx] = Item(v[0], float(v[1]), float(v[2]))
        self.refresh_table(); self.save_data()
        self.form.btn_up.config(state="disabled"); self.form.btn_add.config(state="normal")

    def delete_item(self):
        sel = self.tree.selection()
        if sel:
            self.items.pop(self.tree.index(sel[0]))
            self.refresh_table(); self.save_data()

    def run_solve(self, mode):
        self.txt_res.delete("1.0", tk.END); self.txt_res.insert("1.0", f"⏳ Đang giải {mode}...")
        threading.Thread(target=self._worker, args=(mode,), daemon=True).start()

    def _worker(self, mode):
        cap = float(self.ent_cap.get())
        solver = GWOSolver(int(self.ent_pop.get()), int(self.ent_iter.get())) if mode == "GWO" else BranchAndBoundSolver()
        res = solver.solve(self.items, cap)
        self.after(0, lambda: self._show(res))

    def _show(self, res):
        self.txt_res.delete("1.0", tk.END)
        self.txt_res.insert("1.0", f"✅ KẾT QUẢ:\n💰 Giá trị: {res.max_value}\n⚖️ Nặng: {res.total_weight:.2f}\n⏱️ Time: {res.execution_time:.4f}s")