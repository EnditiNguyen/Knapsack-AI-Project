import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def draw_charts():
    # Đọc dữ liệu từ CSV
    df = pd.read_csv('benchmark_results.csv')
    
    # Thiết lập giao diện biểu đồ
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 5))

    # Biểu đồ 1: So sánh Thời gian thực thi
    plt.subplot(1, 2, 1)
    sns.barplot(data=df, x='Dataset', y='Time (s)', hue='Algorithm')
    plt.title('So sánh thời gian chạy (Giây)')
    plt.yscale('log') # Dùng thang log vì Backtracking có thể nhanh/chậm cực đoan

    # Biểu đồ 2: So sánh Giá trị tối ưu
    plt.subplot(1, 2, 2)
    sns.barplot(data=df, x='Dataset', y='Max Value', hue='Algorithm')
    plt.title('So sánh Giá trị tối ưu tìm được')

    plt.tight_layout()
    plt.savefig('comparison_chart.png') # Lưu file để dán vào báo cáo
    plt.show()

if __name__ == "__main__":
    draw_charts()