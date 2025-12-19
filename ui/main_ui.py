import tkinter as tk
import os
from ui.components import NavButton
from ui.solver_page import SolverPage
from ui.analysis_page import AnalysisPage

class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎒 OPTIMIZATION SUITE PRO")
        self.root.geometry("1300x850")

        # Đường dẫn dữ liệu
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_json = os.path.join(base_dir, 'data', 'sample.json')
        self.data_csv = os.path.join(base_dir, 'data', 'benchmark_results.csv')

        # SIDEBAR
        self.sidebar = tk.Frame(self.root, bg="#2c3e50", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="MENU CHÍNH", fg="#bdc3c7", bg="#2c3e50", font=("Segoe UI", 9, "bold"), pady=20).pack()

        NavButton(self.sidebar, text="🎯 Giải bài toán", command=self.show_solver).pack(fill=tk.X)
        NavButton(self.sidebar, text="📊 Phân tích kết quả", command=self.show_analysis).pack(fill=tk.X)

        # CONTAINER CHÍNH
        self.container = tk.Frame(self.root, bg="#f0f2f5")
        self.container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # KHỞI TẠO TRANG
        self.pages = {}
        self.pages["Solver"] = SolverPage(self.container, self.data_json)
        self.pages["Analysis"] = AnalysisPage(self.container, self.data_csv)

        for p in self.pages.values(): p.place(relwidth=1, relheight=1)

        self.show_solver()

    def show_solver(self):
        self.pages["Solver"].tkraise()

    def show_analysis(self):
        self.pages["Analysis"].tkraise()
        self.pages["Analysis"].load_and_plot() # Tải lại biểu đồ mỗi khi mở trang