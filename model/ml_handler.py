# ui/ml_handler.py
import pandas as pd
from connectors.database_connector import connect
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QPushButton, QSpinBox, QTableWidget, QWidget, QHeaderView, QTableWidgetItem
)


class MachineLearningHandler:
    def __init__(self, tab_ml_widget):
        self.tab = tab_ml_widget
        self.data_scaled = None  # Dữ liệu đã chuẩn hóa
        self.data_prepared = None  # Dữ liệu gốc kèm CustomerID
        self.scaler = StandardScaler()

        # --- Giả sử đây là tên các đối tượng (objectName) bạn đặt trong Qt Designer ---
        self.btn_load_data = self.tab.findChild(QPushButton, "btn_load_data")
        self.btn_find_elbow = self.tab.findChild(QPushButton, "btn_find_elbow")
        self.btn_run_cluster = self.tab.findChild(QPushButton, "btn_run_cluster")
        self.spin_box_k = self.tab.findChild(QSpinBox, "spin_box_k")
        self.table_results = self.tab.findChild(QTableWidget, "table_results")
        # self.elbow_chart_widget = self.tab.findChild(QWidget, "elbow_chart_widget")

        self.connect_signals()

    def connect_signals(self):
        if self.btn_load_data:
            self.btn_load_data.clicked.connect(self.prepare_data)
        if self.btn_find_elbow:
            self.btn_find_elbow.clicked.connect(self.find_optimal_k_elbow)
        if self.btn_run_cluster:
            self.btn_run_cluster.clicked.connect(self.run_kmeans_clustering)
        pass

    def prepare_data(self):
        """
        Lấy và chuẩn bị dữ liệu (Feature Engineering) cho K-Means.
        (ĐIỀU CHỈNH) Tính SUM(Quantity * UnitPrice) cho TotalSpent.
        """
        print("Đang chuẩn bị dữ liệu...")

        # Tính TotalSpent = SUM(Quantity * UnitPrice)
        sql = """
            SELECT 
                CustomerID,
                SUM(Quantity * UnitPrice) AS TotalSpent,
                COUNT(DISTINCT InvoiceNo) AS OrderCount
            FROM transactions
            WHERE CustomerID IS NOT NULL
            GROUP BY CustomerID
            HAVING TotalSpent > 0 AND OrderCount > 0 
        """
        df = connect.queryDataset(sql, val=None)

        if df.empty:
            print("Không có dữ liệu để gom cụm.")
            return

        # Chỉ lấy 2 cột 'TotalSpent' và 'OrderCount' để huấn luyện
        features = df[['TotalSpent', 'OrderCount']]

        # Chuẩn hóa dữ liệu
        self.data_scaled = self.scaler.fit_transform(features)
        self.data_prepared = df  # Lưu lại data gốc (gồm cả CustomerID)
        print(f"Chuẩn bị dữ liệu thành công. {len(df)} khách hàng được tìm thấy.")
        if self.btn_find_elbow: self.btn_find_elbow.setEnabled(True)
        if self.btn_run_cluster: self.btn_run_cluster.setEnabled(True)

    def find_optimal_k_elbow(self):
        """
        Câu 4: ...sử dụng thuật toán... Elbow
        """
        if self.data_scaled is None:
            print("Vui lòng chuẩn bị dữ liệu trước (Nhấn nút Load Data).")
            return

        print("Đang tìm K tối ưu bằng Elbow...")
        wcss = []  # Within-Cluster Sum of Squares
        k_range = range(1, 11)  # Chạy từ k=1 đến k=10

        for k in k_range:
            kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
            kmeans.fit(self.data_scaled)
            wcss.append(kmeans.inertia_)

        # Vẽ biểu đồ Elbow (dùng plt.show() đơn giản)
        plt.figure(figsize=(10, 6))
        plt.plot(k_range, wcss, marker='o', linestyle='--')
        plt.title('Phương pháp Elbow (Elbow Method)')
        plt.xlabel('Số lượng cụm (k)')
        plt.ylabel('WCSS (Tổng bình phương trong cụm)')
        plt.xticks(k_range)
        plt.grid(True)
        plt.show()
        print("Đã hiển thị biểu đồ Elbow.")

    def run_kmeans_clustering(self):
        """
        Câu 4: ...gom cụm khách hàng... liệt kê các khách hàng theo cụm.
        """
        if self.data_scaled is None or self.data_prepared is None:
            print("Vui lòng chuẩn bị dữ liệu trước.")
            return

        k = self.spin_box_k.value()  # Lấy K từ UI
        if k <= 0:
            print("Vui lòng chọn số cụm (K) > 0.")
            return

        print(f"Đang chạy K-Means với k={k}...")

        kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
        clusters = kmeans.fit_predict(self.data_scaled)

        # Gán nhãn cụm trở lại DataFrame gốc
        self.data_prepared['Cluster'] = clusters

        print("Gom cụm thành công. Kết quả:")
        # Sắp xếp theo cụm để dễ nhìn
        results_df = self.data_prepared.sort_values(by='Cluster')
        print(results_df[['CustomerID', 'TotalSpent', 'OrderCount', 'Cluster']])

        # Hiển thị kết quả lên QTableWidget
        self.update_table_widget(self.table_results, results_df)

    def update_table_widget(self, table_widget, df):
        """Hàm tiện ích để hiển thị DataFrame trên QTableWidget."""
        table_widget.clear()
        table_widget.setRowCount(len(df))
        table_widget.setColumnCount(len(df.columns))
        table_widget.setHorizontalHeaderLabels(df.columns)

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                # Định dạng số cho dễ đọc
                if isinstance(value, (int, float)):
                    item = QTableWidgetItem(f"{value:,.0f}")
                else:
                    item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)