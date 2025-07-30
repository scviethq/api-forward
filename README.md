# Forward API Gateway

Hệ thống trung gian forward request từ hệ thống A sang hệ thống B sử dụng FastAPI và loguru.

## Tính năng

- ✅ Forward request từ hệ thống A sang hệ thống B
- ✅ Cấu hình linh hoạt qua file YAML
- ✅ Log rotation với loguru
- ✅ Middleware để log request/response
- ✅ Hỗ trợ path parameters
- ✅ Timeout configuration
- ✅ Error handling
- ✅ Health check endpoint

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd new_foward
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Cấu hình routes trong file `config.yaml`

## Cấu hình

File `config.yaml` chứa cấu hình cho hệ thống:

```yaml
routes:
  salesorder_create:
    path: /api/salesorder
    target_url: https://erp.example.com/api/salesorder
    timeout: 30
  inventory_sync:
    path: /api/inventory
    target_url: https://wms.example.com/api/inventory
    timeout: 30

server:
  host: "0.0.0.0"
  port: 8000
  log_level: "INFO"

logging:
  rotation: "1 day"
  retention: "30 days"
  compression: "zip"
  format: "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
```

## Chạy ứng dụng

```bash
# Chạy với uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Hoặc chạy trực tiếp
python -m app.main
```

## Sử dụng

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Xem danh sách routes
```bash
curl http://localhost:8000/routes
```

### 3. Forward request
```bash
# POST request
curl -X POST http://localhost:8000/api/forward/salesorder_create \
  -H "Content-Type: application/json" \
  -d '{"order_id": "123", "customer": "John Doe"}'

# GET request
curl http://localhost:8000/api/forward/inventory_sync?warehouse=main

# PUT request
curl -X PUT http://localhost:8000/api/forward/product_update/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Product", "price": 150}'

# DELETE request
curl -X DELETE http://localhost:8000/api/forward/product_update/123

# GET với path parameters
curl http://localhost:8000/api/forward/customer_info/123
```

## Cấu trúc dự án

```
new_foward/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration loader
│   ├── logger.py        # Loguru setup
│   ├── middleware.py    # Custom middleware
│   └── forwarder.py     # Request forwarder
├── logs/                # Log files (tự động tạo)
├── config.yaml          # Configuration file
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## API Endpoints

### GET /
Root endpoint - thông tin về API gateway

### GET /health
Health check endpoint

### GET /routes
Lấy danh sách các route có sẵn

### POST/GET/PUT/DELETE /api/forward/{route_name}
Forward request đến hệ thống đích

## Logging

Hệ thống sử dụng loguru với các tính năng:

- **Console logging**: Hiển thị log trên console
- **File logging**: Lưu log vào file `logs/forward.log`
- **Error logging**: Lưu error vào file `logs/error.log`
- **Log rotation**: Tự động rotate log hàng ngày
- **Log retention**: Giữ log trong 30 ngày
- **Log compression**: Nén log file cũ

## Middleware

### LoggingMiddleware
- Log tất cả request và response
- Đo thời gian xử lý request
- Tạo request ID cho mỗi request

### RequestIDMiddleware
- Thêm request ID vào header
- Giúp trace request qua các service

## Error Handling

Hệ thống xử lý các lỗi sau:

- **404**: Route không tồn tại
- **502**: Lỗi kết nối đến hệ thống đích
- **504**: Timeout khi gọi hệ thống đích
- **500**: Lỗi nội bộ

## Ví dụ sử dụng

### 1. Tạo sales order (POST)
```bash
curl -X POST http://localhost:8000/api/forward/salesorder_create \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "SO-001",
    "customer_id": "CUST-123",
    "items": [
      {"product_id": "PROD-001", "quantity": 2, "price": 100}
    ]
  }'
```

### 2. Lấy thông tin inventory (GET)
```bash
curl "http://localhost:8000/api/forward/inventory_sync?warehouse=main&category=electronics"
```

### 3. Cập nhật product (PUT)
```bash
curl -X PUT http://localhost:8000/api/forward/product_update/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Product", "price": 150}'
```

### 4. Xóa product (DELETE)
```bash
curl -X DELETE http://localhost:8000/api/forward/product_update/123
```

### 5. Lấy thông tin customer (GET)
```bash
curl http://localhost:8000/api/forward/customer_info/123
```

## Monitoring

### Log files
- `logs/forward.log`: Tất cả log
- `logs/error.log`: Chỉ error log

### Metrics
- Request count
- Response time
- Error rate
- Status code distribution

## Security

- CORS được cấu hình để cho phép tất cả origins (có thể thay đổi trong production)
- Headers nhạy cảm được loại bỏ khi forward
- Timeout được cấu hình để tránh hanging requests

## Production Deployment

1. Sử dụng Gunicorn với Uvicorn workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Sử dụng Docker:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. Sử dụng systemd service:
```ini
[Unit]
Description=Forward API Gateway
After=network.target

[Service]
Type=simple
User=forward-api
WorkingDirectory=/opt/forward-api
ExecStart=/usr/local/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
``` 