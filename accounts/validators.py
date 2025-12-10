import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class SignupValidator:
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError("Parol kamida 8 belgidan iborat bo'lishi kerak")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Parol kamida 1 ta katta harf o'z ichiga olishi kerak")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Parol kamida 1 ta kichik harf o'z ichiga olishi kerak")
        if not re.search(r'\d', password):
            raise ValidationError("Parol kamida 1 ta raqam o'z ichiga olishi kerak")
        return True
    
    @staticmethod
    def validate_email(email):
        email_validator = EmailValidator(message="Noto'g'ri email formati")
        try:
            email_validator(email)
            return True
        except ValidationError as e:
            raise ValidationError(str(e))
    
    @staticmethod
    def validate_name(name):
        if len(name.strip()) < 2:
            raise ValidationError("Ism kamida 2 belgidan iborat bo'lishi kerak")
        if len(name) > 150:
            raise ValidationError("Ism 150 belgidan oshmasligi kerak")
        return True