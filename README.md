# 破竹财经导航

一个现代化的财经信息导航网站，基于 Flask 框架开发，支持自定义分类和链接管理。

## 功能特性

- 🎯 响应式布局，支持移动端和桌面端
- 🔍 实时搜索功能，快速定位目标网站
- 👨‍💼 后台管理系统，轻松管理导航内容
- 🔐 安全的密码管理机制
- 🌐 SEO 优化，包含 sitemap 和 robots.txt
- 🎨 美观的界面设计
- 🚀 支持 Vercel 一键部署

## 目录结构

```
.
├── app.py              # 主应用程序文件
├── config/            
│   └── navigation.json # 导航配置文件
├── static/            
│   ├── styles.css     # 样式文件
│   └── script.js      # JavaScript 文件
├── templates/         
│   ├── index.html     # 主页模板
│   └── admin/         # 管理后台模板
│       ├── login.html        # 登录页面
│       ├── dashboard.html    # 管理仪表盘
│       └── change_password.html  # 修改密码页面
├── requirements.txt    # 项目依赖
├── vercel.json        # Vercel 配置文件
└── .env.example       # 环境变量示例文件
```

## 环境要求

- Python 3.8+
- Flask 2.0.1
- 其他依赖见 requirements.txt

## 本地开发

1. 克隆仓库：
```bash
git clone [仓库地址]
cd [项目目录]
```

2. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

5. 运行开发服务器：
```bash
flask run
```

## Vercel 部署

1. Fork 本仓库到你的 GitHub 账号

2. 在 Vercel 中导入项目

3. 配置环境变量：
   - `ADMIN_PASSWORD`: 管理员密码
   - `SECRET_KEY`: 应用密钥
   - `BASE_URL`: 网站域名
   - `SITE_NAME`: 网站名称
   - `SITE_DESCRIPTION`: 网站描述
   - `VERCEL_TOKEN`: Vercel API Token
   - `VERCEL_PROJECT_ID`: 项目 ID
   - `VERCEL_TEAM_ID`: （可选）团队 ID

4. 部署完成后即可访问

## 使用说明

1. 访问网站首页，查看导航内容
2. 通过搜索框快速查找目标网站
3. 访问 `/admin` 进入管理后台
4. 在管理后台可以：
   - 添加/编辑/删除导航分类
   - 添加/编辑/删除导航链接
   - 修改管理员密码
   - 自定义网站信息

## SEO 优化

- 自动生成 sitemap.xml
- 配置 robots.txt
- 优化的 meta 标签
- Open Graph 协议支持
- 结构化数据支持

## 安全特性

- 密码加密存储
- 会话管理
- CSRF 保护
- 环境变量配置
- 安全的密码修改机制

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License

## 联系方式

- 电子邮件：contact@your-domain.com 