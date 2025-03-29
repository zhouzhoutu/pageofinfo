# 破竹财经导航

一个专业的财经网址导航平台，基于 Flask 构建，提供优质的网站分类导航服务。

## 功能特点

- 🎯 智能搜索：实时搜索和过滤功能
- 📱 响应式设计：完美适配各种设备
- 🎨 现代化UI：简洁美观的卡片式布局
- 🔒 后台管理：安全的管理员登录和内容管理系统
- 📊 分类管理：灵活的网站分类和排序功能
- 🔗 链接管理：支持添加、编辑、删除网站链接
- 🎯 SEO优化：内置多项搜索引擎优化措施

## 技术栈

- 后端：Python Flask
- 数据库：SQLAlchemy
- 前端：HTML5, CSS3, JavaScript
- UI框架：Noto Sans SC 字体
- 安全：Flask-Login 用户认证

## 项目结构

```
├── app.py              # Flask应用主文件
├── templates/          # HTML模板文件
│   ├── index.html     # 导航首页
│   └── admin/         # 管理后台模板
├── static/            # 静态资源文件
│   ├── styles.css     # 样式表
│   └── script.js      # JavaScript脚本
└── README.md          # 项目说明文档
```

## 安装和运行

1. 克隆项目到本地：
   ```bash
   git clone <repository_url>
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行项目：
   ```bash
   python app.py
   ```

4. 访问网站：
   - 导航首页：http://localhost:5000
   - 管理后台：http://localhost:5000/admin

## 管理员账户

- 默认用户名：admin
- 默认密码：admin123

首次登录后请及时修改默认密码。

## 开发环境要求

- Python 3.6+
- Flask 2.0+
- 现代浏览器（Chrome、Firefox、Safari、Edge等）

## 部署说明

1. 生产环境部署时请修改 `SECRET_KEY` 和数据库配置
2. 建议使用 Gunicorn 或 uWSGI 作为生产环境服务器
3. 配置 Nginx 作为反向代理
4. 使用 HTTPS 确保安全性

## 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交改动：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目维护者：破竹科技
- 官方网站：[破竹财经导航](https://your-domain.com)
- 电子邮件：contact@your-domain.com 