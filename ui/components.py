import tkinter as tk
from tkinter import ttk

class NavButton(tk.Button):
    """Nút bấm tùy chỉnh cho thanh Sidebar"""
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, text=text, command=command, 
                         bg="#2c3e50", fg="white", relief=tk.FLAT, 
                         font=("Segoe UI", 11), anchor="w", padx=20, pady=15, 
                         activebackground="#34495e", activeforeground="white", **kwargs)
        self.bind("<Enter>", lambda e: self.config(bg="#34495e"))
        self.bind("<Leave>", lambda e: self.config(bg="#2c3e50"))

class ItemForm(tk.LabelFrame):
    """Khung nhập liệu vật phẩm"""
    def __init__(self, parent, on_add, on_update, on_delete):
        super().__init__(parent, text=" 📝 Quản lý vật phẩm ", bg="white", 
                         padx=15, pady=15, font=('Segoe UI', 11, 'bold'))
        
        self.entries = []
        labels = ["Tên:", "Nặng (kg):", "Giá ($):"]
        for i, text in enumerate(labels):
            tk.Label(self, text=text, bg="white").grid(row=0, column=i*2, padx=5, sticky="w")
            ent = tk.Entry(self, width=12, bd=1, relief="solid")
            ent.grid(row=0, column=i*2+1, padx=5)
            self.entries.append(ent)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.grid(row=1, column=0, columnspan=7, pady=(15, 0))
        
        self.btn_add = tk.Button(btn_frame, text="THÊM MỚI", bg="#1a73e8", fg="white", width=12, command=on_add)
        self.btn_add.pack(side=tk.LEFT, padx=5)
        
        self.btn_up = tk.Button(btn_frame, text="CẬP NHẬT", bg="#f4b400", fg="white", width=12, command=on_update, state="disabled")
        self.btn_up.pack(side=tk.LEFT, padx=5)
        
        self.btn_del = tk.Button(btn_frame, text="XÓA CHỌN", bg="#ea4335", fg="white", width=12, command=on_delete)
        self.btn_del.pack(side=tk.LEFT, padx=5)