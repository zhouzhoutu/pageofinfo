from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///navigation.db')
# 设置密码哈希方法
app.config['SECURITY_PASSWORD_HASH'] = 'sha256'
app.config['SECURITY_PASSWORD_SALT'] = 'your-salt-here'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 数据模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    order = db.Column(db.Integer, default=0)
    links = db.relationship('Link', backref='category', lazy=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    url = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50))  # 存储图标emoji或图标类名
    order = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 路由：前端页面
@app.route('/')
def index():
    return redirect(url_for('finance_nav'))

@app.route('/finance-nav')
def finance_nav():
    categories = Category.query.order_by(Category.order).all()
    return render_template('index.html', categories=categories)

# 路由：管理员登录
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password')
    return render_template('admin/login.html')

# 路由：管理后台
@app.route('/admin')
@login_required
def admin_dashboard():
    categories = Category.query.order_by(Category.order).all()
    return render_template('admin/dashboard.html', categories=categories)

# API：分类管理
@app.route('/admin/category', methods=['POST'])
@login_required
def add_category():
    name = request.form.get('name')
    order = request.form.get('order', 0)
    category = Category(name=name, order=order)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/category/<int:id>', methods=['PUT'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    category.name = data.get('name', category.name)
    category.order = data.get('order', category.order)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/admin/category/<int:id>', methods=['DELETE'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'status': 'success'})

# API：链接管理
@app.route('/admin/link', methods=['POST'])
@login_required
def add_link():
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    icon = request.form.get('icon')
    category_id = request.form.get('category_id')
    order = request.form.get('order', 0)
    
    link = Link(
        title=title,
        description=description,
        url=url,
        icon=icon,
        category_id=category_id,
        order=order
    )
    db.session.add(link)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/<int:id>', methods=['PUT'])
@login_required
def update_link(id):
    link = Link.query.get_or_404(id)
    data = request.get_json()
    link.title = data.get('title', link.title)
    link.description = data.get('description', link.description)
    link.url = data.get('url', link.url)
    link.icon = data.get('icon', link.icon)
    link.order = data.get('order', link.order)
    link.category_id = data.get('category_id', link.category_id)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/admin/link/<int:id>', methods=['DELETE'])
@login_required
def delete_link(id):
    link = Link.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    return jsonify({'status': 'success'})

# 路由：修改密码
@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not check_password_hash(current_user.password_hash, current_password):
            flash('当前密码错误')
            return redirect(url_for('change_password'))
            
        if new_password != confirm_password:
            flash('新密码和确认密码不匹配')
            return redirect(url_for('change_password'))
            
        current_user.password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        flash('密码修改成功')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/change_password.html')

# 路由：退出登录
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # 创建默认管理员账户（如果不存在）
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256')
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True) 