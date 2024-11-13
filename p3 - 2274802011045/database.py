import psycopg2
from flask import session

def get_db_connection():
    connection = psycopg2.connect(
        host=session.get('db_host', 'localhost'),  # Địa chỉ host với giá trị mặc định
        database=session.get('db_name', 'sach'),  # Tên cơ sở dữ liệu với giá trị mặc định
        user=session.get('db_username', 'postgres'),  # Tên người dùng với giá trị mặc định
        password=session.get('db_password', '1234567890')  # Mật khẩu với giá trị mặc định
    )
    return connection
