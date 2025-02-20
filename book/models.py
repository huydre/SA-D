# models.py
from django.db import models
from datetime import date

class Book(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    publication_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'  # Đảm bảo tên collection là 'books'

    def __str__(self):
        return self.title