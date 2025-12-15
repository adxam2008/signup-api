from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .repositories import UserRepository
from .validators import SignupValidator
import logging
import random
import string

logger = logging.getLogger(__name__)


def generate_username(name):
    """
    Ism asosida unique username yaratish
    Masalan: "Adxam Salimov" -> "adxam7234"
    """
    first_name = name.split()[0].lower()
    clean_name = ''.join(filter(str.isalpha, first_name))
    random_numbers = ''.join(random.choices(string.digits, k=4))
    username = clean_name + random_numbers
    return username


def generate_password(length=10):
    """
    Kuchli random parol yaratish
    Masalan: "aS20081501"
    """
    password = []
    password.append(random.choice(string.ascii_uppercase))
    password.append(random.choice(string.ascii_lowercase))
    remaining = length - 2
    password.extend(random.choices(string.ascii_letters + string.digits, k=remaining))
    random.shuffle(password)
    return ''.join(password)


class SignupService:
    def __init__(self):
        self.repository = UserRepository()
        self.validator = SignupValidator()
    
    def register_user(self, name, phone):
        """
        User ro'yxatdan o'tkazish
        Password avtomatik yaratiladi
        """
        # Username yaratish
        username = generate_username(name)
        
        # Agar username mavjud bo'lsa, yangi yaratish
        while self.repository.username_exists(username):
            username = generate_username(name)
        
        # Parol avtomatik yaratish
        password = generate_password()
        
        self._validate_input(name, phone, password)
        
        if self.repository.phone_exists(phone):
            logger.warning(f"Telefon raqam allaqachon mavjud: {phone}")
            raise ConflictError("Bu telefon raqam allaqachon ro'yxatdan o'tgan")
        
        try:
            user = self.repository.create_user(
                name=name,
                phone=phone,
                password=password,
                username=username
            )
            
            logger.info(f"Yangi user yaratildi: {user.phone}, login: {username}")
            
            return {
                'user_id': user.user_id,
                'phone': user.phone,
                'login': username,
                'password': password,
                'success': True
            }
        except Exception as e:
            logger.error(f"User yaratishda xatolik: {str(e)}")
            raise Exception("User yaratishda xatolik yuz berdi")
    
    def _validate_input(self, name, phone, password):
        self.validator.validate_name(name)
        self.validator.validate_phone(phone)
        self.validator.validate_password(password)


class LoginService:
    """Login business logic"""
    
    def __init__(self):
        self.repository = UserRepository()
    
    def login_user(self, phone, password):
        user = self.repository.get_by_phone(phone)
        
        if not user:
            raise InvalidCredentialsError("Telefon raqam yoki parol noto'g'ri")
        
        if not user.check_password(password):
            raise InvalidCredentialsError("Telefon raqam yoki parol noto'g'ri")
        
        if not user.is_active:
            raise InvalidCredentialsError("Akkaunt o'chirilgan yoki bloklangan")
        
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"User login qildi: {user.phone}")
        
        return {
            'success': True,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.user_id,
            'phone': user.phone,
            'name': user.name
        }


class ConflictError(Exception):
    pass


class InvalidCredentialsError(Exception):
    """Telefon raqam yoki parol noto'g'ri"""
    pass