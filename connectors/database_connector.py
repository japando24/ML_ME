import mysql.connector
import traceback
import pandas as pd

# --- CẤU HÌNH DATABASE ---
# Dựa trên code của bạn, tôi đặt cấu hình vào đây để dễ quản lý
# Các file khác không cần biết chi tiết này
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'retails',  # Tên CSDL bạn cung cấp
    'user': 'root',
    'password': '@Dnb24042004'  # Password bạn cung cấp
}


class DatabaseConnector:
    """
    Lớp quản lý kết nối và thực thi các truy vấn nghiệp vụ.
    """

    def __init__(self):
        self.config = DB_CONFIG
        self.conn = None
        # Tự động kết nối khi khởi tạo
        self.connect()

    def connect(self):
        """Kết nối tới MySQL Database."""
        if self.conn and self.conn.is_connected():
            print("Kết nối đã được thiết lập.")
            return self.conn

        try:
            # **self.config sẽ giải nén dict thành các tham số
            self.conn = mysql.connector.connect(**self.config)
            print("Kết nối CSDL mới thành công.")
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

    def _execute_commit(self, sql, val=None):
        """Hàm trợ giúp nội bộ cho C-U-D (Create, Update, Delete)."""
        try:
            if not self.conn or not self.conn.is_connected():
                print("Mất kết nối, đang thử kết nối lại...")
                self.connect()
                if not self.conn:
                    print("Không thể kết nối lại. Hủy bỏ thao tác.")
                    return False

            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            self.conn.commit()  # Commit thay đổi
            cursor.close()
            print("Thao tác C-U-D thành công.")
            return True
        except mysql.connector.Error as e:
            print(f"Lỗi thực thi (commit): {e}")
            traceback.print_exc()
            self.conn.rollback()  # Hoàn tác nếu có lỗi
            return False
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            traceback.print_exc()
            return False

    # --- CÁC HÀM TRUY VẤN (TỪ CODE CỦA BẠN) ---

    def queryDataset(self, sql, val=None):
        """Hàm này trả về một Pandas DataFrame, lý tưởng cho thống kê/ML."""
        try:
            # Đảm bảo kết nối
            if not self.conn or not self.conn.is_connected():
                self.connect()

            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            df = pd.DataFrame(cursor.fetchall())
            if not df.empty:
                df.columns = cursor.column_names  # Gán tên cột cho DataFrame
            cursor.close()
            return df
        except Exception as e:
            print(f"Lỗi queryDataset: {e}")
            traceback.print_exc()
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu lỗi

    def fetchone(self, sql, val):
        """Hàm này dùng để lấy 1 dòng (lý tưởng cho login, lấy chi tiết)."""
        try:
            # Đảm bảo kết nối
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

    def fetchall(self, sql, val):
        """Hàm này dùng để lấy nhiều dòng."""
        try:
            # Đảm bảo kết nối
            if not self.conn or not self.conn.is_connected():
                self.connect()

            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            dataset = cursor.fetchall()
            cursor.close()
            return dataset
        except Exception as e:
            print(f"Lỗi fetchall")