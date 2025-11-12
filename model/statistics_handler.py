# ui/statistics_handler.py
import pandas as pd
from connectors.database_connector import connect  # Import kết nối CSDL
from PyQt6.QtWidgets import (
    QPushButton, QLabel, QDateEdit, QSpinBox, QTableWidget, QHeaderView, QTableWidgetItem
)


# Bạn có thể cần import thêm các thư viện vẽ biểu đồ
# from PyQt6.QtCharts import QChartView
# import matplotlib.pyplot as plt

class StatisticsHandler:
    def __init__(self, tab_statistics_widget):
        self.tab = tab_statistics_widget

        # --- Giả sử đây là tên các đối tượng (objectName) bạn đặt trong Qt Designer ---
        self.btn_find_top_invoice = self.tab.findChild(QPushButton, "btn_find_top_invoice")
        self.lbl_result_top_invoice = self.tab.findChild(QLabel, "lbl_result_top_invoice")

        self.date_edit_from = self.tab.findChild(QDateEdit, "date_edit_from")
        self.date_edit_to = self.tab.findChild(QDateEdit, "date_edit_to")
        self.spin_box_top_n = self.tab.findChild(QSpinBox, "spin_box_top_n")
        self.btn_find_top_customer = self.tab.findChild(QPushButton, "btn_find_top_customer")
        self.table_top_customer = self.tab.findChild(QTableWidget, "table_top_customer")

        # self.btn_run_country_chart = self.tab.findChild(QPushButton, "btn_run_country_chart")
        # self.chart_view_widget = self.tab.findChild(QWidget, "chart_view_widget") # Nơi để vẽ biểu đồ

        self.connect_signals()

    def connect_signals(self):
        # Kết nối nút bấm với hàm (nếu các nút này tồn tại)
        if self.btn_find_top_invoice:
            self.btn_find_top_invoice.clicked.connect(self.handle_top_invoice)
        if self.btn_find_top_customer:
            self.btn_find_top_customer.clicked.connect(self.handle_top_n_customers)
        # if self.btn_run_country_chart:
        #     self.btn_run_country_chart.clicked.connect(self.handle_country_chart)
        pass

    def handle_top_invoice(self):
        """
        Câu 3: +InvoiceNo có trị giá lớn nhất
        (ĐIỀU CHỈNH) Tính (Quantity * UnitPrice)
        """
        print("Đang tìm InvoiceNo có giá trị giao dịch (đơn lẻ) lớn nhất...")

        # TÍNH TOÁN LineTotal = Quantity * UnitPrice
        sql = """
            SELECT InvoiceNo, (Quantity * UnitPrice) AS LineTotal
            FROM transactions
            ORDER BY LineTotal DESC
            LIMIT 1
        """
        result = connect.fetchone(sql, val=None)

        if result and self.lbl_result_top_invoice:
            invoice_no = result[0]
            total_price = result[1]
            self.lbl_result_top_invoice.setText(
                f"Hóa đơn (dòng) giá trị lớn nhất: {invoice_no} (Giá trị: {total_price:,.2f})")
            print(f"Hóa đơn (dòng) giá trị lớn nhất: {invoice_no} (Giá trị: {total_price})")
        elif self.lbl_result_top_invoice:
            self.lbl_result_top_invoice.setText("Không tìm thấy dữ liệu.")
            print("Không tìm thấy dữ liệu.")

    def handle_top_n_customers(self):
        """
        Câu 3: +TOP N CustomerID ... trong khoảng T1 tới T2
        (ĐIỀU CHỈNH) Tính SUM(Quantity * UnitPrice)
        (ĐIỀU CHỈNH) Dùng STR_TO_DATE() để so sánh InvoiceDate (dạng text)
        """
        if not (self.spin_box_top_n and self.date_edit_from and self.date_edit_to and self.table_top_customer):
            print("Thiếu control trên UI (Top N Customer).")
            return

        # 1. Lấy giá trị từ UI
        top_n = self.spin_box_top_n.value()
        # Lấy ngày theo định dạng chuẩn SQL YYYY-MM-DD
        date_from = self.date_edit_from.date().toString("yyyy-MM-dd")
        date_to = self.date_edit_to.date().toString("yyyy-MM-dd")

        print(f"Đang tìm {top_n} khách hàng hàng đầu từ {date_from} đến {date_to}...")

        # 2. Xử lý dữ liệu:
        # Dùng STR_TO_DATE(InvoiceDate, '%d/%m/%Y %H:%i') để chuyển text sang ngày
        # Dùng SUM(Quantity * UnitPrice) để tính tổng chi tiêu
        sql = """
            SELECT 
                CustomerID, 
                SUM(Quantity * UnitPrice) AS TotalSpent
            FROM transactions
            WHERE 
                CustomerID IS NOT NULL 
                AND STR_TO_DATE(InvoiceDate, '%%d/%%m/%%Y %%H:%%i') BETWEEN %s AND %s
            GROUP BY CustomerID
            ORDER BY TotalSpent DESC
            LIMIT %s
        """
        # MySQL Connector yêu cầu truyền 3 tham số cho val
        val = (date_from, date_to, top_n)

        df = connect.queryDataset(sql, val)

        # 3. Hiển thị kết quả lên QTableWidget
        self.update_table_widget(self.table_top_customer, df)
        if df.empty:
            print("Không tìm thấy dữ liệu cho khoảng thời gian này.")

    def handle_country_chart(self):
        """
        Câu 3: +Tích hợp Chart phân bố đơn hàng theo năm ở các quốc gia.
        (ĐIỀU CHỈNH) Dùng YEAR(STR_TO_DATE(...)) để lấy năm
        """
        print("Đang tạo biểu đồ phân bố đơn hàng...")

        # Dùng YEAR(STR_TO_DATE(...)) để trích xuất năm
        sql = """
            SELECT 
                YEAR(STR_TO_DATE(InvoiceDate, '%%d/%%m/%%Y %%H:%%i')) AS OrderYear, 
                Country, 
                COUNT(DISTINCT InvoiceNo) AS OrderCount
            FROM transactions
            WHERE Country IS NOT NULL AND InvoiceDate IS NOT NULL
            GROUP BY OrderYear, Country
            ORDER BY OrderYear, OrderCount DESC
        """
        df = connect.queryDataset(sql, val=None)

        if not df.empty:
            print("Dữ liệu biểu đồ:")
            print(df)
            # 2. Tích hợp Matplotlib/PyQtChart
            # (Bạn cần tự viết code vẽ biểu đồ từ DataFrame 'df' vào self.chart_view_widget)
        else:
            print("Không có dữ liệu để vẽ biểu đồ.")

    def update_table_widget(self, table_widget, df):
        """Hàm tiện ích để hiển thị DataFrame trên QTableWidget."""
        table_widget.clear()
        table_widget.setRowCount(len(df))
        table_widget.setColumnCount(len(df.columns))
        table_widget.setHorizontalHeaderLabels(df.columns)

        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)