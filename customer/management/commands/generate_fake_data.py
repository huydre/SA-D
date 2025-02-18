from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from customer.models import Customer, FullName, Contact, Address
from faker import Faker
import random
from django.db import transaction
from datetime import datetime, timedelta

fake = Faker(['vi_VN'])  # Sử dụng locale Việt Nam

class Command(BaseCommand):
    help = 'Generate fake data for customers and users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of customers to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        self.stdout.write('Starting to generate fake data...')

        # List các thành phố phổ biến ở Việt Nam
        cities = ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ',
                 'Biên Hòa', 'Nha Trang', 'Huế', 'Đà Lạt', 'Vũng Tàu']

        # List các tỉnh/thành phố
        states = ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ',
                 'Đồng Nai', 'Khánh Hòa', 'Thừa Thiên-Huế', 'Lâm Đồng', 'Bà Rịa-Vũng Tàu']

        try:
            with transaction.atomic():
                for i in range(count):
                    if i % 100 == 0:
                        self.stdout.write(f'Creating customer {i}/{count}...')

                    # Tạo User
                    username = fake.user_name()
                    while User.objects.filter(username=username).exists():
                        username = fake.user_name()

                    email = fake.email()
                    while User.objects.filter(email=email).exists():
                        email = fake.email()

                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='password123'  # Mật khẩu mặc định
                    )

                    # Tạo FullName
                    full_name = FullName.objects.create(
                        first_name=fake.first_name(),
                        middle_name=fake.first_name() if random.choice([True, False]) else '',
                        last_name=fake.last_name()
                    )

                    # Tạo Contact
                    contact = Contact.objects.create(
                        email=email,
                        phone_primary=fake.phone_number(),
                        phone_secondary=fake.phone_number() if random.choice([True, False]) else '',
                        is_email_verified=random.choice([True, False]),
                        is_phone_verified=random.choice([True, False])
                    )

                    # Tạo Address (1-3 địa chỉ cho mỗi khách hàng)
                    addresses = []
                    for _ in range(random.randint(1, 3)):
                        city_idx = random.randint(0, len(cities) - 1)
                        address = Address.objects.create(
                            street=fake.street_address(),
                            city=cities[city_idx],
                            state=states[city_idx],
                            postal_code=fake.postcode(),
                            country='Việt Nam',
                            is_default=len(addresses) == 0  # Địa chỉ đầu tiên là mặc định
                        )
                        addresses.append(address)

                    # Tạo Customer
                    start_date = datetime(2020, 1, 1)
                    end_date = datetime.now()
                    random_date = start_date + timedelta(
                        days=random.randint(0, (end_date - start_date).days)
                    )

                    customer = Customer.objects.create(
                        user=user,
                        full_name=full_name,
                        contact=contact,
                        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=70)
                    )

                    # Thêm địa chỉ vào customer
                    for address in addresses:
                        customer.addresses.add(address)

                self.stdout.write(self.style.SUCCESS(f'Successfully created {count} customers'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            raise e