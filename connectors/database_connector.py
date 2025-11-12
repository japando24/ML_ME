# japando24/ml_me/ML_ME-3c09f051e4b364e1f1378f218bbebd9ff4120b9e/connectors/database_connector.py

import mysql.connector
import traceback
import pandas as pd

# import bcrypt  <-- ĐÃ XÓA DÒNG NÀY, KHÔNG CẦN NỮA

# --- CẤU HÌNH DATABASE ---
# Cấu hình này đã đúng với thông tin của bạn (database 'um3la')
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'um3la',
    'user': 'root',
    'password': '@Dnb24042004'
}


class DatabaseConnector:
    """
    Lớp quản lý kết nối và thực thi các truy vấn nghiệp vụ.
    """

    def __init__(self):
        self.config = DB_CONFIG
        self.conn = None
        self.connect()

    def connect(self):
        """Kết nối tới MySQL Database."""
        if self.conn and self.conn.is_connected():
            return self.conn

        try:
            self.conn = mysql.connector.connect(**self.config)
            print(f"Kết nối CSDL '{self.config.get('database')}' mới thành công.")
            return self.conn
        except mysql.connector.Error as e:
            self.conn = None
            print(f"Lỗi kết nối CSDL '{self.config.get('database')}': {e}")
            traceback.print_exc()
        return None

    def close(self):
        """Đóng kết nối CSDL."""
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            print(f"Đã đóng kết nối CSDL '{self.config.get('database')}'.")

    # ... (Các hàm _execute_commit, queryDataset, fetchone, fetchall giữ nguyên) ...

    def queryDataset(self, sql, val=None):
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            df = pd.DataFrame(cursor.fetchall())
            if not df.empty:
                df.columns = cursor.column_names
            cursor.close()
            return df
        except Exception as e:
            print(f"Lỗi queryDataset: {e}")
            traceback.print_exc()
        return pd.DataFrame()

    def fetchone(self, sql, val):
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            dataset = cursor.fetchone()
            cursor.close()
            return dataset
        except Exception as e:
            print(f"Lỗi fetchone: {e}")
            traceback.print_exc()
        return None

    def fetchall(self, sql, val=None):
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            dataset = cursor.fetchall()
            cursor.close()
            return dataset
        except Exception as e:
            print(f"Lỗi fetchall: {e}")
            traceback.print_exc()
        return []

    # === HÀM ĐÃ ĐƯỢC SỬA LẠI HOÀN TOÀN ===
    def verify_employee(self, email, password):
        """
        Kiểm tra thông tin đăng nhập của nhân viên
        sử dụng mật khẩu VĂN BẢN THƯỜNG (plaintext)
        """
        try:
            # 1. Câu lệnh SQL so sánh trực tiếp email VÀ password
            # (Vì CSDL của bạn lưu mật khẩu dạng plaintext "123")
            #
            sql = "SELECT role FROM employee WHERE email = %s AND password = %s"
            val = (email, password)

            result = self.fetchone(sql, val)

            if result:
                # result là một tuple, ví dụ ('admin',)
                role_from_db = result[0]  # Lấy ra 'admin'

                # 2. SỬA LỖI KIỂU CHỮ:
                # Chuyển 'admin' -> 'Admin' để khớp với main_window.py
                role_capitalized = role_from_db.capitalize()

                return True, role_capitalized
            else:
                # Không tìm thấy user hoặc sai password
                return False, None

        except Exception as e:
            print(f"Lỗi verify_employee: {e}")
            traceback.print_exc()
            return False, None


# Tạo một đối tượng kết nối duy nhất (singleton) để các module khác import
connect = DatabaseConnector()