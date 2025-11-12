# japando24/ml_me/ML_ME-3c09f051e4b364e1f1378f218bbebd9ff4120b9e/ui/main_window.py

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

# === SỬA LỖI IMPORT ===
# 1. Dùng .ui_main vì file ui_main.py nằm CÙNG thư mục 'ui'
from .ui_main import Ui_MainWindow
# 2. Import 'connect' để có thể gọi connect.close()
from connectors.database_connector import connect
# === KẾT THÚC SỬA LỖI ===

# Import các class xử lý logic (sẽ được tạo sau)
# from statistics_handler import StatisticsHandler
# from ml_handler import MachineLearningHandler
# from crud_employee_handler import CrudEmployeeHandler

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, role):
        super().__init__()
        self.setupUi(self)
        self.user_role = role

        # Khởi tạo các handler
        # self.crud_handler = CrudEmployeeHandler(self.tab_crud_employee)
        # self.stats_handler = StatisticsHandler(self.tab_statistics)
        # self.ml_handler = MachineLearningHandler(self.tab_ml)

        self.setup_ui_for_role()

    def setup_ui_for_role(self):
        """
        Đây là hàm thực hiện Câu 3: Ẩn/hiện các tab dựa trên Role
        """
        print(f"Thiết lập UI cho Role: {self.user_role}")

        # 1. Lấy tất cả các tab
        # Lưu ý: Index của widget có thể thay đổi khi bạn removeTab
        # An toàn hơn là tìm bằng tên đối tượng
        tab_crud = self.tab_crud_employee
        tab_stats = self.tab_statistics
        tab_ml = self.tab_ml

        # 2. Ẩn tất cả các tab đi
        # Xóa theo index từ cao xuống thấp để tránh lỗi dịch chuyển index
        self.main_tabWidget.removeTab(2)  # Index 2 (ML)
        self.main_tabWidget.removeTab(1)  # Index 1 (Stats)
        self.main_tabWidget.removeTab(0)  # Index 0 (CRUD)

        # 3. Thêm lại các tab dựa trên quyền
        if self.user_role == "Admin":
            print("Hiển thị tab: CRUD, Stats, ML")
            self.main_tabWidget.addTab(tab_crud, "Quản lý Employee")
            self.main_tabWidget.addTab(tab_stats, "Thống kê Báo cáo")
            self.main_tabWidget.addTab(tab_ml, "Machine Learning")
            # self.crud_handler.load_employees()

        elif self.user_role == "Technical":
            print("Hiển thị tab: ML")
            self.main_tabWidget.addTab(tab_ml, "Machine Learning")
            # self.ml_handler.connect_signals()

        elif self.user_role == "Reporter":
            print("Hiển thị tab: Stats")
            self.main_tabWidget.addTab(tab_stats, "Thống kê Báo cáo")
            # self.stats_handler.connect_signals()

        else:
            print(f"Role '{self.user_role}' không xác định. Không hiển thị tab nào.")

    def closeEvent(self, event):
        """Đảm bảo đóng kết nối DB khi tắt ứng dụng."""
        # === SỬA LỖI: Đổi 'db_connector' thành 'connect' ===
        connect.close()
        print("Người dùng đã tắt Main Window. Đóng kết nối DB.")
        event.accept()

    # ===================================================================
    # NƠI ĐÂY SẼ LÀ CÁC HÀM GỌI LOGIC CHO TỪNG TAB
    # ===================================================================