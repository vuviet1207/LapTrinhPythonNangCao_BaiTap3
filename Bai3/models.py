from database import get_db_connection

class User:
    @staticmethod
    def get_user(username):
        """
        Truy vấn thông tin người dùng dựa trên tên đăng nhập.
        """
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Lỗi khi truy vấn người dùng: {e}")
            return None
        finally:
            connection.close()


    @staticmethod
    def create_user(username, password):
        """
        Thêm một người dùng mới vào cơ sở dữ liệu.
        """
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(query, (username, password))
            connection.commit()
            print("Người dùng được tạo thành công.")
        except Exception as e:
            print(f"Lỗi khi tạo người dùng: {e}")
        finally:
            connection.close()


    @staticmethod
    def update_user(old_username, new_username, new_password=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Cập nhật username
                cursor.execute(
                    "UPDATE users SET username = %s WHERE username = %s",
                    (new_username, old_username)
                )
                # Cập nhật mật khẩu nếu được cung cấp
                if new_password:
                    cursor.execute(
                        "UPDATE users SET password = %s WHERE username = %s",
                        (new_password, new_username)
                    )
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e  # Có thể log lỗi hoặc hiển thị thông báo phù hợp
        finally:
            connection.close()



class Book:
    @staticmethod
    def get_all_books():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sach ORDER BY id ASC")
            books = cursor.fetchall()
        connection.close()
        return books

    @staticmethod
    def search_books(search_term):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sach WHERE ten_sach ILIKE %s", ('%' + search_term + '%',))
            books = cursor.fetchall()
        connection.close()
        return books

    @staticmethod
    def add_book(ten_sach, tac_gia, nxb, the_loai):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO sach (ten_sach, tac_gia, nxb, the_loai) VALUES (%s, %s, %s, %s)",
                           (ten_sach, tac_gia, nxb, the_loai))
        connection.commit()
        connection.close()

    @staticmethod
    def get_book_by_id(id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sach WHERE id = %s", (id,))
            book = cursor.fetchone()
        connection.close()
        return book

    @staticmethod
    def update_book(id, ten_sach, tac_gia, nxb, the_loai):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE sach SET ten_sach = %s, tac_gia = %s, nxb = %s, the_loai = %s WHERE id = %s
            """, (ten_sach, tac_gia, nxb, the_loai, id))
        connection.commit()
        connection.close()

    @staticmethod
    def delete_book(id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sach WHERE id = %s", (id,))
        connection.commit()
        connection.close()
