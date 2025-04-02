from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import json
from urllib.parse import urljoin
from dotenv import load_dotenv
import hashlib
import requests

# 加载环境变量
load_dotenv()

app = Flask(__name__, 
           static_url_path='',
           static_folder='static',
           template_folder='templates')

# 基础配置
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
SITE_NAME = os.environ.get('SITE_NAME', '破竹财经导航')
SITE_DESCRIPTION = os.environ.get('SITE_DESCRIPTION', '一站式财经信息导航平台')

# Vercel API 配置
VERCEL_TOKEN = os.environ.get('VERCEL_TOKEN')
VERCEL_PROJECT_ID = os.environ.get('VERCEL_PROJECT_ID')
VERCEL_TEAM_ID = os.environ.get('VERCEL_TEAM_ID')

# 默认配置
DEFAULT_CONFIG = {
    "site_name": SITE_NAME,
    "site_description": SITE_DESCRIPTION,
    "categories": [
        {
            "name": "财经资讯",
            "links": [
                {
                    "name": "东方财富网",
                    "url": "https://www.eastmoney.com/",
                    "description": "中国领先的财经网站"
                }
            ]
        }
    ]
}

def hash_password(password):
    """对密码进行哈希处理"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_admin_password():
    """获取管理员密码"""
    return os.environ.get('ADMIN_PASSWORD', 'admin123')

def update_vercel_env(new_password_hash):
    """更新 Vercel 环境变量"""
    if not VERCEL_TOKEN or not VERCEL_PROJECT_ID:
        return False, "Vercel API 配置缺失"

    headers = {
        'Authorization': f'Bearer {VERCEL_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    url = f'https://api.vercel.com/v9/projects/{VERCEL_PROJECT_ID}/env'
    if VERCEL_TEAM_ID:
        url += f'?teamId={VERCEL_TEAM_ID}'

    data = {
        "key": "ADMIN_PASSWORD",
        "value": new_password_hash,
        "type": "encrypted",
        "target": ["production", "preview", "development"]
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            envs = response.json()
            for env in envs.get('envs', []):
                if env['key'] == 'ADMIN_PASSWORD':
                    delete_url = f"{url}/{env['id']}"
                    requests.delete(delete_url, headers=headers)

        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            return True, "密码更新成功"
        return False, f"更新失败: {response.text}"
    except Exception as e:
        return False, f"更新失败: {str(e)}"

# 环境配置
app.debug = os.environ.get('FLASK_DEBUG', '0') == '1'

def load_config():
    """加载导航配置"""
    try:
        config_json = os.environ.get('NAVIGATION_CONFIG')
        if config_json:
            return json.loads(config_json)
        return DEFAULT_CONFIG
    except (json.JSONDecodeError, TypeError):
        return DEFAULT_CONFIG

def save_config(config):
    """保存导航配置"""
    try:
        config_json = json.dumps(config, ensure_ascii=False)
        if VERCEL_TOKEN and VERCEL_PROJECT_ID:
            headers = {
                'Authorization': f'Bearer {VERCEL_TOKEN}',
                'Content-Type': 'application/json',
            }
            
            url = f'https://api.vercel.com/v9/projects/{VERCEL_PROJECT_ID}/env'
            if VERCEL_TEAM_ID:
                url += f'?teamId={VERCEL_TEAM_ID}'

            data = {
                "key": "NAVIGATION_CONFIG",
                "value": config_json,
                "type": "encrypted",
                "target": ["production", "preview", "development"]
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                envs = response.json()
                for env in envs.get('envs', []):
                    if env['key'] == 'NAVIGATION_CONFIG':
                        delete_url = f"{url}/{env['id']}"
                        requests.delete(delete_url, headers=headers)

            response = requests.post(url, headers=headers, json=data)
            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to save config: {response.text}")
        return True
    except Exception as e:
        print(f"Error saving config: {str(e)}")
        return False

# SEO相关路由
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    """生成网站地图"""
    pages = []
    
    # 添加首页
    pages.append({
        'loc': BASE_URL,
        'lastmod': datetime.now().strftime('%Y-%m-%d'),
        'priority': '1.0'
    })
    
    # 获取所有分类页面
    config = load_config()
    for category in config.get('categories', []):
        # 这里可以根据实际情况添加分类页面的URL
        pass

    # 生成XML
    xml = render_template('sitemap.xml', pages=pages)
    return Response(xml, mimetype='application/xml')

# 路由：前端页面
@app.route('/')
def index():
    try:
        config = load_config()
        return render_template('index.html', 
                            categories=config.get('categories', []),
                            site_name=config.get('site_name', SITE_NAME),
                            site_description=config.get('site_description', SITE_DESCRIPTION))
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        return f"An error occurred: {str(e)}", 500

@app.route('/finance-nav')
def finance_nav():
    return redirect(url_for('index'))

# 静态文件路由
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# 后台管理路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        stored_password = get_admin_password()
        
        if hash_password(password) == stored_password or password == stored_password:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/login.html', 
                             error='密码错误',
                             site_name=SITE_NAME)
    return render_template('admin/login.html', site_name=SITE_NAME)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    config = load_config()
    return render_template('admin/dashboard.html', 
                         config=json.dumps(config, ensure_ascii=False, indent=4),
                         site_name=config.get('site_name', SITE_NAME))

@app.route('/admin/save', methods=['POST'])
def admin_save_config():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    try:
        config = json.loads(request.form.get('config'))
        if save_config(config):
            return render_template('admin/dashboard.html', 
                                config=json.dumps(config, ensure_ascii=False, indent=4),
                                site_name=config.get('site_name', SITE_NAME),
                                success='配置已保存')
        else:
            return render_template('admin/dashboard.html', 
                                config=json.dumps(config, ensure_ascii=False, indent=4),
                                site_name=config.get('site_name', SITE_NAME),
                                error='保存失败')
    except json.JSONDecodeError:
        return render_template('admin/dashboard.html', 
                             config=request.form.get('config'),
                             site_name=SITE_NAME,
                             error='JSON 格式错误')

# API：配置管理
@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/api/config', methods=['POST'])
def update_config():
    config = request.get_json()
    save_config(config)
    return jsonify({"status": "success"})

# API：分类管理
@app.route('/admin/category', methods=['POST'])
@login_required
def add_category():
    name = request.form.get('name')
    category = {'name': name, 'links': []}
    config = load_config()
    config['categories'].append(category)
    save_config(config)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/category/<int:id>', methods=['PUT'])
@login_required
def update_category(id):
    config = load_config()
    category = config['categories'][id]
    data = request.get_json()
    category['name'] = data.get('name', category['name'])
    save_config(config)
    return jsonify({'status': 'success'})

@app.route('/admin/category/<int:id>', methods=['DELETE'])
@login_required
def delete_category(id):
    config = load_config()
    del config['categories'][id]
    save_config(config)
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
    config = load_config()
    category = config['categories'][int(category_id)]
    category['links'].append({
        'title': title,
        'description': description,
        'url': url,
        'icon': icon
    })
    save_config(config)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/link/<int:id>', methods=['PUT'])
@login_required
def update_link(id):
    config = load_config()
    link = config['categories'][id]['links'][id]
    data = request.get_json()
    link['title'] = data.get('title', link['title'])
    link['description'] = data.get('description', link['description'])
    link['url'] = data.get('url', link['url'])
    link['icon'] = data.get('icon', link['icon'])
    save_config(config)
    return jsonify({'status': 'success'})

@app.route('/admin/link/<int:id>', methods=['DELETE'])
@login_required
def delete_link(id):
    config = load_config()
    del config['categories'][id]['links'][id]
    save_config(config)
    return jsonify({'status': 'success'})

# 路由：修改密码
@app.route('/admin/change-password', methods=['GET', 'POST'])
def change_password():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        stored_password = get_admin_password()
        
        # 验证当前密码
        if hash_password(current_password) != stored_password and current_password != stored_password:
            return render_template('admin/change_password.html',
                                error='当前密码错误',
                                site_name=SITE_NAME)
        
        # 验证新密码
        if new_password != confirm_password:
            return render_template('admin/change_password.html',
                                error='两次输入的新密码不一致',
                                site_name=SITE_NAME)
        
        if len(new_password) < 8:
            return render_template('admin/change_password.html',
                                error='新密码长度不能少于8个字符',
                                site_name=SITE_NAME)
        
        # 更新密码
        new_password_hash = hash_password(new_password)
        success, message = update_vercel_env(new_password_hash)
        
        if success:
            return render_template('admin/change_password.html',
                                success='密码修改成功，请在几分钟后重新登录',
                                site_name=SITE_NAME)
        else:
            return render_template('admin/change_password.html',
                                error=f'密码修改失败: {message}',
                                site_name=SITE_NAME)
    
    return render_template('admin/change_password.html', site_name=SITE_NAME)

# 路由：退出登录
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # 确保配置文件存在
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'config', 'navigation.json')):
        save_config({
            "site_name": SITE_NAME,
            "site_description": SITE_DESCRIPTION,
            "categories": []
        })
    app.run(debug=app.debug) 