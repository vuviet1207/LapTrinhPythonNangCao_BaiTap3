from flask import render_template, redirect, url_for, request, session, flash
from models import User, Book
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session

def setup_routes(app):
    # Đăng nhập
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.get_user(username)

            if user and check_password_hash(user['password'], password):  # So sánh băm mật khẩu
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash("Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.", "error")
                return redirect(url_for('login'))
        return render_template('login.html')

    # Đăng ký
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Sử dụng phương thức get_user để kiểm tra tên đăng nhập
            existing_user = User.get_user(username)
            if existing_user:
                flash("Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.", "error")
                return render_template('register.html')

            # Nếu không trùng, tiếp tục xử lý đăng ký
            hashed_password = generate_password_hash(password)  # Băm mật khẩu

            # Sử dụng phương thức create_user để thêm người dùng
            User.create_user(username, hashed_password)

            flash("Đăng ký thành công, bạn có thể đăng nhập.", "success")
            return redirect(url_for('login'))

        return render_template('register.html')

    # Trang chính
    @app.route('/')
    def home():
        return redirect(url_for('login'))

    @app.route('/index')
    def index():
        if not session.get('logged_in'):
            flash("Vui lòng đăng nhập trước khi truy cập trang này.", "error")
            return redirect(url_for('login'))

        books = Book.get_all_books()
        return render_template('index.html', books=books)

    # Tìm kiếm sách
    @app.route('/search', methods=['POST'])
    def search():
        if not session.get('logged_in'):
            flash("Vui lòng đăng nhập trước khi tìm kiếm.", "error")
            return redirect(url_for('login'))

        search_term = request.form['search_term']
        books = Book.search_books(search_term)
        if not books:
            flash("Không tìm thấy sách nào phù hợp với từ khóa.", "error")
        return render_template('index.html', books=books)

    # Thêm sách
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

            if not nxb.isdigit():
                flash("Lưu ý: NXB (năm xuất bản) phải là một số.", "error")
                return redirect(url_for('add'))

            Book.add_book(ten_sach, tac_gia, nxb, the_loai)
            flash("Thêm sách thành công.", "success")
            return redirect(url_for('add'))

        books = Book.get_all_books()
        return render_template('add.html', books=books)

    # Sửa sách
    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update(id):
        if not session.get('logged_in'):
            flash("Vui lòng đăng nhập trước khi cập nhật sách.", "error")
            return redirect(url_for('login'))

        if request.method == 'POST':
            ten_sach = request.form['ten_sach']
            tac_gia = request.form['tac_gia']
            nxb = request.form['nxb']
            the_loai = request.form['the_loai']

            Book.update_book(id, ten_sach, tac_gia, nxb, the_loai)
            flash("Cập nhật thông tin sách thành công.", "success")
            return redirect(url_for('update', id=id))

        book = Book.get_book_by_id(id)
        all_books = Book.get_all_books()
        return render_template('update.html', book=book, all_books=all_books)

    # Xóa sách
    @app.route('/delete/<int:id>', methods=['GET', 'POST'])
    def delete(id):
        if not session.get('logged_in'):
            flash("Vui lòng đăng nhập trước khi xóa sách.", "error")
            return redirect(url_for('login'))

        if request.method == 'POST':
            Book.delete_book(id)
            flash("Xóa sách thành công.", "success")
            return redirect(url_for('index'))

        book = Book.get_book_by_id(id)
        return render_template('delete.html', book=book)

    # Đăng xuất
    @app.route('/disconnect')
    def disconnect():
        session.clear()
        flash("Bạn đã đăng xuất thành công.", "success")
        return redirect(url_for('login'))

    # Chỉnh sửa thông tin tài khoản
    @app.route('/edit_profile', methods=['GET', 'POST'])
    def edit_profile():
        if not session.get('logged_in'):
            flash("Vui lòng đăng nhập để chỉnh sửa thông tin.", "error")
            return redirect(url_for('login'))

        # Lấy username từ session
        username = session['username']

        if request.method == 'POST':
            # Lấy dữ liệu từ form
            new_username = request.form['username']
            new_password = request.form['password']  # Có thể để trống nếu không đổi mật khẩu

            # Cập nhật thông tin người dùng
            User.update_user(username, new_username, new_password)

            # Cập nhật session nếu username thay đổi
            if new_username != username:
                session['username'] = new_username

            flash("Cập nhật thông tin thành công.", "success")
            return redirect(url_for('index'))

        # Lấy thông tin người dùng để hiển thị trên form
        user = User.get_user(username)

        return render_template('edit_profile.html', user=user)

    @app.route('/reload', methods=['GET'])
    def reload():
        if not session.get('logged_in'):
            flash("Vui lòng đăng nhập trước khi tải lại trang.", "error")
            return redirect(url_for('login'))
        return redirect(url_for('index'))