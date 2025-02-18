from django.db import models

class Book(models.Model):
    title = models.CharField("Title", max_length=255)
    author = models.CharField("Author", max_length=255)
    description = models.TextField("Description", blank=True)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    publisher = models.CharField("Publisher", max_length=255, blank=True)
    publication_date = models.DateField("Publication Date", blank=True, null=True)
    stock = models.PositiveIntegerField("Stock", default=0)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title