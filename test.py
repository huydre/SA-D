from bson import ObjectId

# Trong Django shell
from book.models import Book
# Liệt kê tất cả books
books = Book.objects.using('mongodb').all()
for book in books:
    print(f"ID: {book._id}, Title: {book.title}")

# Hoặc tìm một book cụ thể
book_id = ObjectId("65f2c1234567890123456789")  # Thay bằng ID thực
book = Book.objects.using('mongodb').get(_id=book_id)
print(f"Found book: {book.title}")