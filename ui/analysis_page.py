import tkinter as tk
import tkinter as tk
from tkinter import messagebox
import threading
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
# Import hàm từ file benchmark
try:
    from benchmark import run_benchmark_on_existing_data
except ImportError:
    # Nếu file nằm trong thư mục gốc
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from benchmark import run_benchmark_on_existing_data

class AnalysisPage(tk.Frame):
    def __init__(self, parent, csv_path):
        super().__init__(parent, bg="#f0f2f5")
        self.csv_path = csv_path
        # Thiết lập style seaborn ngay khi khởi tạo
        sns.set_theme(style="whitegrid", palette="muted")
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#f0f2f5", padx=20, pady=15)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📊 PHÂN TÍCH CHUYÊN SÂU", 
                 font=("Segoe UI", 16, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(side=tk.LEFT)
        
        # Nhóm nút điều khiển
        btn_frame = tk.Frame(header, bg="#f0f2f5")
        btn_frame.pack(side=tk.RIGHT)

        self.btn_run = tk.Button(btn_frame, text="🔥 CHẠY BENCHMARK", command=self.trigger_benchmark, 
                                 bg="#ea4335", fg="white", font=("Segoe UI", 9, "bold"), 
                                 padx=15, pady=5, relief=tk.FLAT)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="🔄 LÀM MỚI", command=self.load_and_plot, 
                  bg="#1a73e8", fg="white", font=("Segoe UI", 9, "bold"),
                  padx=15, pady=5, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        self.fig_container = tk.Frame(self, bg="white")
        self.fig_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    def trigger_benchmark(self):
        self.btn_run.config(state=tk.DISABLED, text="⌛ ĐANG TÍNH TOÁN...")
        threading.Thread(target=self._run_task, daemon=True).start()

    def _run_task(self):
        try:
            run_benchmark_on_existing_data()
            self.after(0, self.load_and_plot)
            self.after(0, lambda: messagebox.showinfo("Thông báo", "Đã cập nhật dữ liệu benchmark mới!"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi", str(e)))
        finally:
            self.after(0, lambda: self.btn_run.config(state=tk.NORMAL, text="🔥 CHẠY BENCHMARK"))

    def load_and_plot(self):
        # Xóa các biểu đồ cũ
        for w in self.fig_container.winfo_children(): w.destroy()
        
        if not os.path.exists(self.csv_path):
            tk.Label(self.fig_container, text="Chưa có dữ liệu. Vui lòng nhấn 'CHẠY BENCHMARK'.", 
                     bg="white", font=("Segoe UI", 12)).pack(pady=100)
            return

        try:
            # 1. Đọc dữ liệu
            df = pd.read_csv(self.csv_path)

            # 2. Tiền xử lý: Chuyển từ Wide sang Long format để dùng được hue của Seaborn
            # Chuyển đổi Thời gian
            df_time = df.melt(id_vars=['Num_Items'], value_vars=['BT_Time', 'GWO_Time'],
                              var_name='Algorithm', value_name='Time (s)')
            df_time['Algorithm'] = df_time['Algorithm'].replace({'BT_Time': 'Backtracking', 'GWO_Time': 'GWO AI'})

            # Chuyển đổi Giá trị (Lọc bỏ các dòng N/A của BT nếu có)
            df_temp = df.copy()
            df_temp['BT_Value'] = pd.to_numeric(df_temp['BT_Value'], errors='coerce')
            df_val = df_temp.melt(id_vars=['Num_Items'], value_vars=['BT_Value', 'GWO_Value'],
                                  var_name='Algorithm', value_name='Max Value')
            df_val['Algorithm'] = df_val['Algorithm'].replace({'BT_Value': 'Backtracking', 'GWO_Value': 'GWO AI'})

            # 3. Vẽ biểu đồ với Seaborn
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

            # Biểu đồ 1: Thời gian thực thi (Sử dụng Log Scale như bạn yêu cầu)
            sns.barplot(data=df_time, x='Num_Items', y='Time (s)', hue='Algorithm', ax=ax1)
            ax1.set_title('So sánh thời gian chạy (Giây)', fontsize=12, fontweight='bold', pad=15)
            ax1.set_yscale('log')
            ax1.set_xlabel('Số lượng vật phẩm')
            ax1.set_ylabel('Thời gian (log scale)')

            # Biểu đồ 2: Giá trị tối ưu
            sns.barplot(data=df_val, x='Num_Items', y='Max Value', hue='Algorithm', ax=ax2)
            ax2.set_title('So sánh Giá trị tối ưu tìm được', fontsize=12, fontweight='bold', pad=15)
            ax2.set_xlabel('Số lượng vật phẩm')
            ax2.set_ylabel('Giá trị ($)')

            # Tối ưu khoảng cách
            fig.tight_layout(pad=3.0)

            # Nhúng vào Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.fig_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            tk.Label(self.fig_container, text=f"Lỗi hiển thị biểu đồ: {e}", bg="white").pack(pady=20)       