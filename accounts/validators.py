import re
from django.core.exceptions import ValidationError


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
    def validate_phone(phone):
        """
        Telefon raqam validatsiyasi
        Format: +998901234567 yoki 998901234567
        """
        # Faqat raqamlar va + belgisini qoldirish
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Uzbekiston raqami tekshirish
        if not re.match(r'^(\+?998)?[0-9]{9}$', cleaned):
            raise ValidationError(
                "Noto'g'ri telefon raqam formati. "
                "To'g'ri format: +998901234567 yoki 998901234567"
            )
        return True
    
    @staticmethod
    def validate_name(name):
        if len(name.strip()) < 2:
            raise ValidationError("Ism kamida 2 belgidan iborat bo'lishi kerak")
        if len(name) > 150:
            raise ValidationError("Ism 150 belgidan oshmasligi kerak")
        return True