import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# === SỬA LỖI IMPORT ===
# 1. Dùng .ui_login vì file ui_login.py nằm CÙNG thư mục 'ui'
from .ui_login import Ui_LoginWindow

# 2. Import db_connector từ thư mục 'connectors' (tính từ gốc project)
from connectors.database_connector import db_connector

# 3. Dùng .main_window vì file main_window.py nằm CÙNG thư mục 'ui'
from .main_window import MainWindow
# === KẾT THÚC SỬA LỖI ===


class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.login_attempts = 0
        self.MAX_ATTEMPTS = 3

        # Biến giữ tham chiếu đến cửa sổ main
        self.main_window = None

        # Kết nối tín hiệu (signal) của nút bấm với hàm (slot)
        self.btn_login.clicked.connect(self.handle_login)

        # Thiết lập style cho thông báo lỗi
        palette = self.lbl_message.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(Qt.GlobalColor.red))
        self.lbl_message.setPalette(palette)

    def handle_login(self):
        email = self.txt_email.text()
        password = self.txt_password.text()

        if not email or not password:
            self.lbl_message.setText("Vui lòng nhập email và password.")
            return

        # Dòng này bây giờ sẽ chạy được vì db_connector đã được import
        success, role = db_connector.verify_employee(email, password)

        if success:
            # Đăng nhập thành công
            self.lbl_message.setText(f"Đăng nhập thành công với vai trò: {role}")
            print(f"Đăng nhập thành công. Role: {role}")

            # Mở màn hình chính và truyền Role qua
            self.open_main_window(role)
        else:
            # Đăng nhập thất bại
            self.login_attempts += 1
            remaining_attempts = self.MAX_ATTEMPTS - self.login_attempts

            if remaining_attempts > 0:
                self.lbl_message.setText(f"Sai email hoặc password. Còn {remaining_attempts} lần thử.")
            else:
                # Khóa chức năng đăng nhập
                self.lbl_message.setText("Bạn đã nhập sai 3 lần. Chức năng đăng nhập bị khóa.")
                self.btn_login.setEnabled(False)
                self.txt_email.setEnabled(False)
                self.txt_password.setEnabled(False)

                # Hiển thị thông báo (thay vì alert)
                QMessageBox.critical(self, "Lỗi Đăng Nhập", "Chức năng đăng nhập đã bị khóa do sai quá 3 lần.")

    def open_main_window(self, role):
        """
        Khởi tạo và hiển thị màn hình chính, truyền role vào.
        """
        # Kiểm tra xem cửa sổ chính đã được tạo chưa
        if self.main_window is None:
            self.main_window = MainWindow(role)  # Truyền role vào constructor

        self.main_window.show()  # Hiển thị cửa sổ chính
        self.close()  # Đóng cửa sổ đăng nhập

    def closeEvent(self, event):
        """Đảm bảo đóng kết nối DB khi tắt cửa sổ."""
        # Nếu cửa sổ chính không được mở (ví dụ: người dùng tắt login)
        # thì chúng ta nên đóng kết nối DB
        if self.main_window is None:
            db_connector.close()
            print("Người dùng đã tắt cửa sổ Login. Đóng kết nối DB.")
        event.accept()