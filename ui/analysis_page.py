import tkinter as tk
from tkinter import messagebox
import threading
import pandas as pd
import matplotlib.pyplot as plt
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
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#f0f2f5", padx=20, pady=10)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📊 PHÂN TÍCH & SO SÁNH", font=("Segoe UI", 14, "bold"), bg="#f0f2f5").pack(side=tk.LEFT)
        
        # Nút Chạy Benchmark
        self.btn_run = tk.Button(header, text="🔥 CHẠY BENCHMARK MỚI", command=self.trigger_benchmark, 
                                 bg="#ea4335", fg="white", font=("Segoe UI", 9, "bold"), padx=10)
        self.btn_run.pack(side=tk.RIGHT, padx=5)

        # Nút Refresh
        tk.Button(header, text="🔄 Làm mới biểu đồ", command=self.load_and_plot, 
                  bg="#1a73e8", fg="white", padx=10).pack(side=tk.RIGHT)

        self.fig_container = tk.Frame(self, bg="white")
        self.fig_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def trigger_benchmark(self):
        self.btn_run.config(state=tk.DISABLED, text="⌛ Đang chạy...")
        threading.Thread(target=self._run_task, daemon=True).start()

    def _run_task(self):
        try:
            run_benchmark_on_existing_data()
            self.after(0, self.load_and_plot)
            self.after(0, lambda: messagebox.showinfo("Thành công", "Đã hoàn thành chạy thử nghiệm trên 3 bộ dữ liệu!"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi", str(e)))
        finally:
            self.after(0, lambda: self.btn_run.config(state=tk.NORMAL, text="🔥 CHẠY BENCHMARK MỚI"))

    def load_and_plot(self):
        for w in self.fig_container.winfo_children(): w.destroy()
        
        if not os.path.exists(self.csv_path):
            tk.Label(self.fig_container, text="Chưa có kết quả. Nhấn nút 'CHẠY BENCHMARK MỚI' để bắt đầu.", 
                     bg="white", font=("Segoe UI", 11)).pack(pady=50)
            return

        try:
            df = pd.read_csv(self.csv_path)
            # Lọc bỏ các giá trị N/A để vẽ biểu đồ thời gian
            df_plot = df[df['BT_Value'] != "N/A (Too large)"].copy()
            df_plot['BT_Time'] = df_plot['BT_Time'].astype(float)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

            # Biểu đồ 1: Thời gian thực thi
            ax1.plot(df_plot['Num_Items'], df_plot['BT_Time'], 'o-', label='Backtracking', color='#a142f4')
            ax1.plot(df['Num_Items'], df['GWO_Time'], 's-', label='GWO AI', color='#1e8e3e')
            ax1.set_title("Thời gian xử lý (giây)")
            ax1.set_xlabel("Số lượng vật phẩm")
            ax1.legend()

            # Biểu đồ 2: So sánh giá trị đạt được
            ax2.bar(df['Num_Items'].astype(str), df['GWO_Value'], color='#81c995', label='GWO Value')
            ax2.set_title("Tổng giá trị tìm thấy (GWO)")
            ax2.set_xlabel("Bộ dữ liệu")

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.fig_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            tk.Label(self.fig_container, text=f"Lỗi hiển thị: {e}").pack()