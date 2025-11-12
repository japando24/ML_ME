from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

# Import giao diện
from ui_main import Ui_MainWindow
# Import class xử lý database


# Import các class xử lý logic (sẽ được tạo sau)
# from statistics_handler import StatisticsHandler
# from ml_handler import MachineLearningHandler
# from crud_employee_handler import CrudEmployeeHandler

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, role):  # Nhận role từ LoginWindow
        super().__init__()
        self.setupUi(self)
        self.user_role = role

        # Khởi tạo các handler (logic nghiệp vụ)
        # self.crud_handler = CrudEmployeeHandler(self.tab_crud_employee) # Truyền tab UI vào
        # self.stats_handler = StatisticsHandler(self.tab_statistics)
        # self.ml_handler = MachineLearningHandler(self.tab_ml)

        # Gọi hàm phân quyền UI
        self.setup_ui_for_role()

    def setup_ui_for_role(self):
        """
        Đây là hàm thực hiện Câu 3: Ẩn/hiện các tab dựa trên Role
        """
        print(f"Thiết lập UI cho Role: {self.user_role}")

        # 1. Lấy tất cả các tab
        tab_crud = self.main_tabWidget.widget(0)
        tab_stats = self.main_tabWidget.widget(1)
        tab_ml = self.main_tabWidget.widget(2)

        # 2. Ẩn tất cả các tab đi
        # Dùng removeTab thay vì setVisible(False) để tab biến mất hoàn toàn
        self.main_tabWidget.removeTab(2)  # Index 2 (ML)
        self.main_tabWidget.removeTab(1)  # Index 1 (Stats)
        self.main_tabWidget.removeTab(0)  # Index 0 (CRUD)

        # 3. Thêm lại các tab dựa trên quyền
        if self.user_role == "Admin":
            print("Hiển thị tab: CRUD, Stats, ML")
            self.main_tabWidget.addTab(tab_crud, "Quản lý Employee")
            self.main_tabWidget.addTab(tab_stats, "Thống kê Báo cáo")
            self.main_tabWidget.addTab(tab_ml, "Machine Learning")
            # Kết nối tín hiệu cho các chức năng của Admin
            # self.crud_handler.load_employees()

        elif self.user_role == "Technical":
            print("Hiển thị tab: ML")
            self.main_tabWidget.addTab(tab_ml, "Machine Learning")
            # Kết nối tín hiệu cho Technical
            # self.ml_handler.connect_signals()

        elif self.user_role == "Reporter":
            print("Hiển thị tab: Stats")
            self.main_tabWidget.addTab(tab_stats, "Thống kê Báo cáo")
            # Kết nối tín hiệu cho Reporter
            # self.stats_handler.connect_signals()

        else:
            # Trường hợp role không xác định (dự phòng)
            print(f"Role '{self.user_role}' không xác định. Không hiển thị tab nào.")

    def closeEvent(self, event):
        """Đảm bảo đóng kết nối DB khi tắt ứng dụng."""
        db_connector.close()
        print("Người dùng đã tắt Main Window. Đóng kết nối DB.")
        event.accept()

    # ===================================================================
    # NƠI ĐÂY SẼ LÀ CÁC HÀM GỌI LOGIC CHO TỪNG TAB
    # Ví dụ:
    #
    # def load_employee_data(self):
    #    self.crud_handler.load_employees()
    #
    # def run_top_n_customer_report(self):
    #    t1 = self.ui.dateEdit_t1.date()
    #    t2 = self.ui.dateEdit_t2.date()
    #    n = self.ui.spinBox_n.value()
    #    self.stats_handler.get_top_n_customers(n, t1, t2)
    #
    # def train_model(self):
    #    self.ml_handler.train_model()
    #
    # ===================================================================