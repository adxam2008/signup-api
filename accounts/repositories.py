from django.db import transaction
from .models import User


class UserRepository:
    @staticmethod
    def phone_exists(phone):
        return User.objects.filter(phone__iexact=phone).exists()
    
    @staticmethod
    def username_exists(username):
        return User.objects.filter(username__iexact=username).exists()
    
    @staticmethod
    def get_by_phone(phone):
        try:
            return User.objects.get(phone__iexact=phone)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    @transaction.atomic
    def create_user(name, phone, password, username):
        user = User.objects.create_user(
            phone=phone,
            name=name.strip(),
            password=password,
            username=username
        )
        return user