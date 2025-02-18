from rest_framework import serializers
from django.contrib.auth.models import User
from customer.models import Customer, FullName, Contact, Address
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                return {
                    'user': user,
                    'username': username
                }
            raise serializers.ValidationError("Incorrect username or password.")
        raise serializers.ValidationError("Must include 'username' and 'password'.")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = ['first_name', 'middle_name', 'last_name']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country', 'is_default']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phone_primary', 'phone_secondary']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = FullNameSerializer()
    contact = ContactSerializer()
    address = AddressSerializer()
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name', 'contact', 'address', 'date_of_birth')

    def create(self, validated_data):
        # Tách dữ liệu
        full_name_data = validated_data.pop('full_name')
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')
        date_of_birth = validated_data.pop('date_of_birth', None)

        # Tạo User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        # Tạo FullName
        full_name = FullName.objects.create(**full_name_data)

        # Tạo Contact
        contact = Contact.objects.create(**contact_data)

        # Tạo Address
        address = Address.objects.create(**address_data)

        # Tạo Customer và liên kết các thành phần
        customer = Customer.objects.create(
            user=user,
            full_name=full_name,
            contact=contact,
            date_of_birth=date_of_birth
        )
        customer.addresses.add(address)

        return user