from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Route ĐĂNG NHẬP
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Kiểm tra xem người dùng có tồn tại trong bảng users
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        
        connection.close()
        
        print(f"User: {user}")  # In ra kết quả lấy mật khẩu để kiểm tra

        if user and user[0] == password:  # So sánh mật khẩu trực tiếp mà không cần hash
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.", "error")
            return redirect(url_for('login'))  # Chuyển lại về trang đăng nhập nếu đăng nhập thất bại

    return render_template('login.html')


# Route ĐĂNG KÝ
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Kiểm tra xem username đã tồn tại trong cơ sở dữ liệu hay chưa
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
        
        if existing_user:
            flash("Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.", "error")
            return redirect(url_for('register'))

        # Không mã hóa mật khẩu, lưu trực tiếp mật khẩu vào cơ sở dữ liệu
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        connection.close()
        
        flash("Đăng ký thành công. Vui lòng đăng nhập.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')


# Route HOME
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route TRANG SÁCH (index)
@app.route('/index')
def index():
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập trước khi truy cập trang này.", "error")
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sach")
        books = cursor.fetchall()
    connection.close()
    
    return render_template('index.html', books=books)

@app.route('/search', methods=['POST'])
def search():
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập trước khi tìm kiếm.", "error")
        return redirect(url_for('login'))
    
    search_term = request.form['search_term']
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sach WHERE ten_sach ILIKE %s", ('%' + search_term + '%',))
        books = cursor.fetchall()
    connection.close()
    if not books:
        flash("Không tìm thấy sách nào phù hợp với từ khóa.", "error")
    
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập trước khi thêm sách.", "error")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        ten_sach = request.form['ten_sach']
        tac_gia = request.form['tac_gia']
        nxb = request.form['nxb']
        the_loai = request.form['the_loai']
        
        # Kiểm tra xem năm xuất bản có phải là số không
        if not nxb.isdigit():  # Nếu không phải là số
            flash("Lưu ý: NXB (năm xuất bản) phải là một số.", "error")
            return redirect(url_for('add'))  # Quay lại trang thêm sách
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO sach (ten_sach, tac_gia, nxb, the_loai) VALUES (%s, %s, %s, %s)",
                           (ten_sach, tac_gia, nxb, the_loai))
        connection.commit()
        connection.close()
        
        flash("Thêm sách thành công.", "success")
        return redirect(url_for('add'))  # Reload trang add sau khi thêm


    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sach")
        books = cursor.fetchall()
    connection.close()
    
    return render_template('add.html', books=books)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập trước khi cập nhật sách.", "error")
        return redirect(url_for('login'))
    
    connection = get_db_connection()

    if request.method == 'POST':
        ten_sach = request.form['ten_sach']
        tac_gia = request.form['tac_gia']
        nxb = request.form['nxb']
        the_loai = request.form['the_loai']
        
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE sach
                SET ten_sach = %s, tac_gia = %s, nxb = %s, the_loai = %s
                WHERE id = %s
            """, (ten_sach, tac_gia, nxb, the_loai, id))
            connection.commit()

        connection.close()
        flash("Cập nhật thông tin sách thành công.", "success")
        return redirect(url_for('update', id=id))

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sach WHERE id = %s", (id,))
        book = cursor.fetchone()
        cursor.execute("SELECT * FROM sach")
        all_books = cursor.fetchall()

    connection.close()

    return render_template('update.html', book=book, all_books=all_books)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập trước khi xóa sách.", "error")
        return redirect(url_for('login'))
    
    connection = get_db_connection()

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sach WHERE id=%s", (id,))
        connection.commit()
        connection.close()
        
        flash("Xóa sách thành công.", "success")
        return redirect(url_for('index'))

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sach WHERE id=%s", (id,))
        book = cursor.fetchone()

    connection.close()

    return render_template('delete.html', book=book)

@app.route('/disconnect')
def disconnect():
    session.clear()
    flash("Bạn đã đăng xuất thành công.", "success")
    return redirect(url_for('login'))

@app.route('/reload', methods=['GET'])
def reload():
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập trước khi tải lại trang.", "error")
        return redirect(url_for('login'))
    return redirect(url_for('index'))
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập để chỉnh sửa thông tin.", "error")
        return redirect(url_for('login'))
    
    username = session['username']
    connection = get_db_connection()

    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        # Cập nhật thông tin người dùng
        with connection.cursor() as cursor:
            if new_username != username:  # Nếu người dùng thay đổi tên đăng nhập
                cursor.execute("UPDATE users SET username = %s WHERE username = %s", (new_username, username))
            if new_password:  # Nếu có thay đổi mật khẩu
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            connection.commit()

        session['username'] = new_username  # Cập nhật tên đăng nhập trong session
        connection.close()

        flash("Cập nhật thông tin thành công.", "success")
        return redirect(url_for('index'))

    # Lấy thông tin người dùng từ cơ sở dữ liệu
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

    connection.close()

    return render_template('edit_profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
