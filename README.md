# Bookstore Project

Dự án website bán sách sử dụng Django REST Framework cho backend và React + Vite cho frontend.

## Yêu cầu hệ thống

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- MongoDB 6.0+
- XAMPP (cho MySQL)
- Postgree SQL

## Cấu trúc Database
- MongoDB: Quản lý Books
- MySQL: Quản lý Customers
- SQLite: Các app khác (Cart, Order, etc.)

## Cài đặt

### 1. Backend (Django)

```bash
# Clone dự án
git https://github.com/huydre/SA-D
cd SA-D

# Cài đặt các dependencies
pip install -r requirements.txt

# Tạo file .env theo mẫu .env.example


