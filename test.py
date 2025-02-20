# management/commands/check_db.py
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from book.models import Book

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # Kiểm tra MongoDB
            books = Book.objects.using('mongodb').all()
            self.stdout.write(f'MongoDB connection successful. Found {books.count()} books')

            # Kiểm tra MySQL
            cursor = connections['customers'].cursor()
            self.stdout.write('MySQL connection successful')

            # Kiểm tra SQLite
            cursor = connections['default'].cursor()
            self.stdout.write('SQLite connection successful')

        except OperationalError as e:
            self.stderr.write(f'Database error: {e}')
        except Exception as e:
            self.stderr.write(f'Error: {e}')