import sys
from PyQt6.QtWidgets import QApplication

from ui.login_window import LoginWindow

# THAY THẾ CÁC THÔNG SỐ NÀY BẰNG THÔNG TIN DATABASE CỦA BẠN
# Đây là bước quan trọng, bạn phải mở file `database_connector.py`
# và chỉnh sửa dictionary `DB_CONFIG` ở đầu file đó.
#
# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'your_password', # <-- SỬA LẠI PASSWORD
#     'database': 'your_database_name' # <-- SỬA LẠI TÊN DATABASE
# }
#

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Khởi tạo và hiển thị cửa sổ Đăng nhập
    login_win = LoginWindow()
    login_win.show()

    sys.exit(app.exec())