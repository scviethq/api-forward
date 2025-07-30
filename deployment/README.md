# Forward API Gateway - Deployment

Hướng dẫn triển khai Forward API Gateway trên máy khác.

## 📋 Yêu cầu

- Docker và Docker Compose đã cài đặt
- Port 8000 available

## 🚀 Cách triển khai

### 1. Tải về và chuẩn bị

```bash
# Tạo thư mục deployment
mkdir forward-api-deployment
cd forward-api-deployment

# Copy các file này vào thư mục
# - docker-compose.yml
# - config.yaml
# - start.sh
# - stop.sh
```

### 2. Cấu hình

Chỉnh sửa file `config.yaml` theo nhu cầu:

```yaml
routes:
  dav:
    path: api/{path}
    target_url: https://duocquocgia.com.vn/api/{path}
    timeout: 30
```

### 3. Khởi động

```bash
# Cấp quyền thực thi
chmod +x start.sh stop.sh

# Khởi động service
./start.sh
```

### 4. Kiểm tra

```bash
# Health check
curl http://localhost:8000/health

# Xem logs
docker-compose logs -f forward-api

# API docs
open http://localhost:8000/docs
```

## 📝 Sử dụng

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Xem routes
curl http://localhost:8000/routes

# Forward request
curl http://localhost:8000/api/forward/dav/api/login
```

### Xem logs

```bash
# Real-time logs
docker-compose logs -f forward-api

# Log files
tail -f logs/forward.log
tail -f logs/error.log
```

## 🛠️ Quản lý

### Dừng service
```bash
./stop.sh
```

### Restart service
```bash
docker-compose restart
```

### Update image
```bash
docker-compose pull
docker-compose up -d
```

### Xem status
```bash
docker-compose ps
```

## 📁 Cấu trúc thư mục

```
forward-api-deployment/
├── docker-compose.yml    # Docker compose config
├── config.yaml          # API config
├── start.sh             # Script khởi động
├── stop.sh              # Script dừng
├── logs/                # Log files (tự động tạo)
└── README.md           # Hướng dẫn này
```

## 🔧 Troubleshooting

### Service không start
```bash
# Kiểm tra logs
docker-compose logs forward-api

# Kiểm tra config
cat config.yaml
```

### Port đã được sử dụng
```bash
# Thay đổi port trong docker-compose.yml
ports:
  - "8001:8000"  # Thay 8000 thành 8001
```

### Permission denied
```bash
# Cấp quyền
chmod +x start.sh stop.sh
```

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Docker đang chạy
2. Port 8000 available
3. File config.yaml đúng format
4. Logs trong `docker-compose logs forward-api` 