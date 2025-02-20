from django.core.management.base import BaseCommand
from book.models import Book
from decimal import Decimal
from datetime import datetime
import pymongo

class Command(BaseCommand):
    help = 'Create sample books'

    def handle(self, *args, **options):
        # Kết nối trực tiếp với MongoDB
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['bookstore']
        collection = db['books']

        books = [
            {
                "title": "Đắc Nhân Tâm",
                "author": "Dale Carnegie",
                "description": "Một trong những cuốn sách về nghệ thuật đối nhân xử thế nổi tiếng nhất mọi thời đại",
                "price": 150.00,
                "isbn": "9780671027032",
                "publisher": "NXB Trẻ",
                "publication_date": datetime(2020, 1, 1),
                "stock": 50,
                "image": None,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Nhà Giả Kim",
                "author": "Paulo Coelho",
                "description": "Câu chuyện về hành trình khám phá vận mệnh của một người",
                "price": 120.00,
                "isbn": "9780062315007",
                "publisher": "NXB Văn Học",
                "publication_date": datetime(2020, 2, 1),
                "stock": 40,
                "image": None,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]

        for book_data in books:
            try:
                # Kiểm tra xem sách đã tồn tại chưa
                existing_book = collection.find_one({"isbn": book_data["isbn"]})
                if not existing_book:
                    collection.insert_one(book_data)
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created book "{book_data["title"]}"')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Book with ISBN {book_data["isbn"]} already exists')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to create book "{book_data["title"]}": {str(e)}')
                )