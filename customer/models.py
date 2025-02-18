from django.db import models
from django.conf import settings

class FullName(models.Model):
    first_name = models.CharField("First Name", max_length=50)
    middle_name = models.CharField("Middle Name", max_length=50, blank=True)
    last_name = models.CharField("Last Name", max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()
    
    class Meta:
        app_label = 'customer'

class Address(models.Model):
    street = models.CharField("Street Address", max_length=100)
    city = models.CharField("City", max_length=50)
    state = models.CharField("State/Province", max_length=50)
    postal_code = models.CharField("Postal Code", max_length=10)
    country = models.CharField("Country", max_length=50)
    is_default = models.BooleanField("Default Address", default=False)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}"
    
    class Meta:
        app_label = 'customer'

class Contact(models.Model):
    email = models.EmailField("Email", unique=True)
    phone_primary = models.CharField("Primary Phone", max_length=20)
    phone_secondary = models.CharField("Secondary Phone", max_length=20, blank=True)
    is_email_verified = models.BooleanField("Email Verified", default=False)
    is_phone_verified = models.BooleanField("Phone Verified", default=False)

    def __str__(self):
        return self.email
    
    class Meta:
        app_label = 'customer'

class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="User Account",
        db_constraint=False  # Thêm dòng này
    )
    full_name = models.OneToOneField(
        FullName,
        on_delete=models.CASCADE,
        verbose_name="Full Name",
        null=True,  # Thêm null=True
        blank=True,  # Thêm blank=True
        db_constraint=False  # Thêm dòng này
    )
    contact = models.OneToOneField(
        Contact,
        on_delete=models.CASCADE,
        verbose_name="Contact Information",
        null=True,  # Thêm null=True
        blank=True,  # Thêm blank=True
        db_constraint=False  # Thêm dòng này
    )
    addresses = models.ManyToManyField(
        Address,
        verbose_name="Addresses",
        related_name="customers",
        blank=True  # Thêm blank=True
    )
    date_of_birth = models.DateField("Date of Birth", null=True, blank=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        app_label = 'customer'
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return str(self.full_name)

    def get_default_address(self):
        return self.addresses.filter(is_default=True).first()