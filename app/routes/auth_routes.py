from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from app.extensions import db
from app.models.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Tên người dùng đã tồn tại!')
            return redirect(url_for('auth.register'))

        new_user = User(username=username)  # ✅ role mặc định là "user"
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Đăng ký thành công!')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role  # ✅ lưu role vào session
            flash('Đăng nhập thành công!')
            return redirect(url_for('room.room_home'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu!')
            return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất!')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return f"Xin chào {session['username']}! Vai trò: {session['role']}"



from app.utils.auth_decorators import login_required, admin_required

@auth_bp.route('/admin')
@admin_required
def admin_panel():
    return "🛠 Đây là trang admin. Chào " + session['username']
