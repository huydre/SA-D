# books/management/commands/check_mongodb.py
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from book.models import Book
import pymongo

class Command(BaseCommand):
    help = 'Checks MongoDB connection and displays database info'

    def handle(self, *args, **options):
        try:
            # Kiểm tra kết nối thông qua Django
            self.stdout.write('Checking Django-MongoDB connection...')
            books = Book.objects.using('mongodb').all()
            count = books.count()
            self.stdout.write(self.style.SUCCESS(
                f'✓ Django-MongoDB connection successful! Found {count} books'
            ))

            # Kiểm tra kết nối trực tiếp qua PyMongo
            self.stdout.write('\nChecking direct MongoDB connection...')
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['bookstore']
            books_collection = db['books']
            doc_count = books_collection.count_documents({})

            self.stdout.write(self.style.SUCCESS(
                f'✓ Direct MongoDB connection successful!'
            ))
            self.stdout.write('Database Info:')
            self.stdout.write(f'- Database name: {db.name}')
            self.stdout.write(f'- Collections: {", ".join(db.list_collection_names())}')
            self.stdout.write(f'- Documents in books collection: {doc_count}')

            # Thử lấy một document mẫu
            sample_book = books_collection.find_one()
            if sample_book:
                self.stdout.write('\nSample book:')
                for key, value in sample_book.items():
                    self.stdout.write(f'- {key}: {value}')

        except OperationalError as e:
            self.stderr.write(self.style.ERROR(f'Database error: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
        finally:
            if 'client' in locals():
                client.close()