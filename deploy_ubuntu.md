# 掌镜AI 手相解读系统 - Ubuntu 部署手册

本手册详细介绍了如何在 Ubuntu 系统上部署“掌镜AI”系统的前后端程序。

---

## 1. 环境准备

### 1.1 系统更新
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 安装基础软件
```bash
# 安装 Python 3.10+, Node.js, Nginx, MySQL, Redis
sudo apt install -y python3-pip python3-venv nodejs npm nginx mysql-server redis-server
```

---

## 2. 后端部署 (FastAPI)

### 2.1 获取代码并创建虚拟环境
```bash
cd /var/www/zhangjing/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.2 配置环境变量
在 `backend` 目录下创建 `.env` 文件：
```bash
cp .env.example .env  # 如果有模板的话
nano .env
```
确保配置了 MySQL 连接、OpenAI API KEY 以及管理后台权限：
```env
MYSQL_USER=root
MYSQL_PASSWORD=你的密码
MYSQL_DB=ai_hand_analysis
ADMIN_USERNAME=admin
ADMIN_PASSWORD=你的后台密码
```

### 2.3 使用 Gunicorn + Uvicorn 运行
创建 Systemd 服务文件 `/etc/systemd/system/zhangjing-backend.service`:
```ini
[Unit]
Description=Zhangjing Backend Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/zhangjing/backend
Environment="PATH=/var/www/zhangjing/backend/venv/bin"
ExecStart=/var/www/zhangjing/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```
启动服务：
```bash
sudo systemctl start zhangjing-backend
sudo systemctl enable zhangjing-backend
```

---

## 3. 前端部署 (Vue 3 + Vite)

### 3.1 编译打包
在本地或服务器的前端目录执行：
```bash
cd /var/www/zhangjing/frontend
npm install
# 确保 .env 文件中的 VITE_API_BASE_URL 指向生产 API 地址
npm run build
```

### 3.2 产物位置
打包后的文件位于 `frontend/dist` 目录下。

---

## 4. Nginx 配置 (反向代理与静态资源)

创建 Nginx 配置文件 `/etc/nginx/sites-available/zhangjing`:
```nginx
server {
    listen 80;
    server_name 你的域名或服务器IP;

    # 前端静态文件
    location / {
        root /var/www/zhangjing/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端接口代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 上传照片静态访问
    location /uploads {
        alias /var/www/zhangjing/backend/app/static/uploads;
    }
}
```
激活配置并重启：
```bash
sudo ln -s /etc/nginx/sites-available/zhangjing /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 5. 数据库维护

执行之前生成的优化脚本：
```bash
mysql -u root -p ai_hand_analysis < /var/www/zhangjing/backend/optimize.sql
```

---

## 6. 权限检查
确保 Web 服务器有权访问上传目录：
```bash
sudo chown -R www-data:www-data /var/www/zhangjing/backend/app/static/uploads
sudo chmod -R 755 /var/www/zhangjing/backend/app/static/uploads
```

---
**部署完成！** 现在可以通过浏览器访问您的服务器 IP 或域名了。
