from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, FullName, Contact, Address

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = ['first_name', 'middle_name', 'last_name']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phone_primary', 'phone_secondary', 'is_email_verified', 'is_phone_verified']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country', 'is_default']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = FullNameSerializer()
    contact = ContactSerializer()
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = [
            'id', 'user', 'full_name', 'contact', 'addresses',
            'date_of_birth', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        full_name_data = validated_data.pop('full_name')
        contact_data = validated_data.pop('contact')
        addresses_data = validated_data.pop('addresses', [])

        full_name = FullName.objects.create(**full_name_data)
        contact = Contact.objects.create(**contact_data)
        customer = Customer.objects.create(
            full_name=full_name,
            contact=contact,
            **validated_data
        )

        for address_data in addresses_data:
            address = Address.objects.create(**address_data)
            customer.addresses.add(address)

        return customer

    def update(self, instance, validated_data):
        full_name_data = validated_data.pop('full_name', None)
        contact_data = validated_data.pop('contact', None)
        addresses_data = validated_data.pop('addresses', None)

        if full_name_data:
            FullName.objects.filter(id=instance.full_name.id).update(**full_name_data)

        if contact_data:
            Contact.objects.filter(id=instance.contact.id).update(**contact_data)

        if addresses_data is not None:
            instance.addresses.clear()
            for address_data in addresses_data:
                address = Address.objects.create(**address_data)
                instance.addresses.add(address)

        return super().update(instance, validated_data)