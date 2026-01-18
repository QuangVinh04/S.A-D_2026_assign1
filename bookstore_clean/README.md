# Bookstore Clean Architecture Project

Dự án Django bookstore được thiết kế theo Clean Architecture principles.

## Cấu trúc Project

```
bookstore_clean/
├── domain/              # Domain layer - Business entities
│   ├── entities/        # Domain entities (Customer, Book, Cart)
│   └── value_objects/   # Value objects
├── usecases/            # Use cases - Business logic
│   ├── accounts/        # Account-related use cases
│   ├── books/           # Book-related use cases
│   └── cart/            # Cart-related use cases
├── interfaces/          # Interface layer
│   ├── repositories/    # Repository interfaces
│   ├── controllers/     # Controller interfaces
│   └── presenters/      # Presenter interfaces
├── infrastructure/      # Infrastructure layer
│   ├── database/        # Django models
│   └── repositories/    # Repository implementations
├── framework/           # Framework layer (Django)
│   ├── web/             # Django views
│   └── templates/       # HTML templates
└── bookstore_clean/     # Django project config
```

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install django pymysql
```

2. Tạo migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Chạy server:
```bash
python manage.py runserver
```

## Các chức năng

- ✅ Customer registration
- ✅ Customer login
- ✅ View book catalog
- ✅ Add books to shopping cart
- ✅ View shopping cart contents
- ✅ Remove items from cart

## Clean Architecture Layers

### Domain Layer
Chứa các business entities và rules, không phụ thuộc vào framework hay database.

### Use Cases Layer
Chứa business logic và các use cases cụ thể.

### Interfaces Layer
Định nghĩa các contracts/interfaces cho repositories và controllers.

### Infrastructure Layer
Triển khai các interfaces bằng Django ORM và database.

### Framework Layer
Django-specific code (views, URLs, settings).

## Dependency Flow

```
Framework → Interfaces → Use Cases → Domain
     ↓           ↓
Infrastructure (implements Interfaces)
```

Dependencies chỉ đi từ ngoài vào trong, không đi ngược lại.
