from django.db import transaction
from .models import User


class UserRepository:
    @staticmethod
    def email_exists(email):
        return User.objects.filter(email__iexact=email).exists()
    
    @staticmethod
    def get_by_email(email):
        try:
            return User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    @transaction.atomic
    def create_user(name, email, password):
        user = User.objects.create_user(
            email=email.lower(),
            name=name.strip(),
            password=password
        )
        return user