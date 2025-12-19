import tkinter as tk
from ui.main_ui import KnapsackGUI

if __name__ == "__main__":
    root = tk.Tk()
    # Khởi tạo giao diện từ class trong thư mục ui
    app = KnapsackGUI(root)
    root.mainloop()     