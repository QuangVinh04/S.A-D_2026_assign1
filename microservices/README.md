# Bookstore Microservices Architecture

Hệ thống bookstore được phân tách thành các microservices độc lập giao tiếp qua REST APIs.

## Cấu trúc

```
microservices/
├── customer_service/    # Customer management service
│   ├── customers/       # Customer app
│   └── customer_service/ # Django project config
├── book_service/        # Book catalog service
│   ├── books/          # Book app
│   └── book_service/   # Django project config
└── cart_service/        # Shopping cart service
    ├── carts/          # Cart app
    └── cart_service/   # Django project config
```

## Services

### 1. Customer Service (Port: 8001)
Quản lý thông tin khách hàng:
- **API Base URL**: `http://localhost:8001/api/v1/`
- **Endpoints**:
  - `POST /customers/register/` - Đăng ký khách hàng mới
  - `POST /customers/login/` - Đăng nhập
  - `GET /customers/` - Lấy danh sách khách hàng
  - `GET /customers/{id}/` - Lấy thông tin khách hàng theo ID

### 2. Book Service (Port: 8002)
Quản lý danh mục sách:
- **API Base URL**: `http://localhost:8002/api/v1/`
- **Endpoints**:
  - `GET /books/` - Lấy danh sách tất cả sách
  - `GET /books/catalog/` - Lấy catalog sách
  - `GET /books/{id}/` - Lấy thông tin sách theo ID
  - `POST /books/` - Tạo sách mới (admin)

### 3. Cart Service (Port: 8003)
Quản lý giỏ hàng:
- **API Base URL**: `http://localhost:8003/api/v1/`
- **Endpoints**:
  - `GET /carts/customer/{customer_id}/` - Lấy giỏ hàng của khách hàng
  - `POST /carts/customer/{customer_id}/add/` - Thêm sách vào giỏ hàng
  - `DELETE /carts/item/{item_id}/` - Xóa item khỏi giỏ hàng

## Cài đặt

### Requirements
```bash
pip install django djangorestframework pymysql
```

### Database Setup
Tạo các database MySQL:
```sql
CREATE DATABASE customer_service_db;
CREATE DATABASE book_service_db;
CREATE DATABASE cart_service_db;
```

### Migrations
Chạy migrations cho mỗi service:

**Customer Service:**
```bash
cd customer_service
python manage.py makemigrations
python manage.py migrate
```

**Book Service:**
```bash
cd book_service
python manage.py makemigrations
python manage.py migrate
```

**Cart Service:**
```bash
cd cart_service
python manage.py makemigrations
python manage.py migrate
```

### Chạy Services

Mở 3 terminal windows:

**Terminal 1 - Customer Service:**
```bash
cd customer_service
python manage.py runserver 8001
```

**Terminal 2 - Book Service:**
```bash
cd book_service
python manage.py runserver 8002
```

**Terminal 3 - Cart Service:**
```bash
cd cart_service
python manage.py runserver 8003
```

## API Examples

### Register Customer
```bash
POST http://localhost:8001/api/v1/customers/register/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
}
```

### Get Book Catalog
```bash
GET http://localhost:8002/api/v1/books/catalog/
```

### Add to Cart
```bash
POST http://localhost:8003/api/v1/carts/customer/1/add/
Content-Type: application/json

{
    "book_id": 1,
    "quantity": 2
}
```

### Get Cart
```bash
GET http://localhost:8003/api/v1/carts/customer/1/
```

## Communication Between Services

Các services giao tiếp với nhau qua HTTP REST API:
- Cart Service gọi Book Service để lấy thông tin sách
- Cart Service lưu `customer_id` và `book_id` (references, không phải Foreign Keys)
- Mỗi service có database riêng biệt

## Benefits of Microservices

1. **Independence**: Mỗi service có thể phát triển và deploy độc lập
2. **Scalability**: Có thể scale từng service riêng biệt
3. **Technology Diversity**: Có thể sử dụng công nghệ khác nhau cho mỗi service
4. **Fault Isolation**: Lỗi ở một service không ảnh hưởng đến service khác
5. **Team Autonomy**: Mỗi team có thể làm việc độc lập trên service của mình
