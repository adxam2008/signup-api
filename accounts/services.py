from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .repositories import UserRepository
from .validators import SignupValidator
import logging

logger = logging.getLogger(__name__)


class SignupService:
    def __init__(self):
        self.repository = UserRepository()
        self.validator = SignupValidator()
    
    def register_user(self, name, email, password):
        self._validate_input(name, email, password)
        
        if self.repository.email_exists(email):
            logger.warning(f"Email allaqachon mavjud: {email}")
            raise ConflictError("Bu email allaqachon ro'yxatdan o'tgan")
        
        try:
            user = self.repository.create_user(
                name=name,
                email=email,
                password=password
            )
            
            logger.info(f"Yangi user yaratildi: {user.email}")
            
            return {
                'user_id': user.user_id,
                'email': user.email,
                'success': True
            }
        except Exception as e:
            logger.error(f"User yaratishda xatolik: {str(e)}")
            raise Exception("User yaratishda xatolik yuz berdi")
    
    def _validate_input(self, name, email, password):
        self.validator.validate_name(name)
        self.validator.validate_email(email)
        self.validator.validate_password(password)


class LoginService:
    """Login business logic"""
    
    def __init__(self):
        self.repository = UserRepository()
    
    def login_user(self, email, password):
        """
        User login qilish
        
        Returns:
            dict: {
                'success': bool,
                'access_token': str,
                'refresh_token': str,
                'user_id': str,
                'email': str,
                'name': str
            }
        
        Raises:
            InvalidCredentialsError: Email yoki parol noto'g'ri
        """
        
        # Email orqali user topish
        user = self.repository.get_by_email(email)
        
        if not user:
            raise InvalidCredentialsError("Email yoki parol noto'g'ri")
        
        # Parolni tekshirish
        if not user.check_password(password):
            raise InvalidCredentialsError("Email yoki parol noto'g'ri")
        
        # User aktiv emasligini tekshirish
        if not user.is_active:
            raise InvalidCredentialsError("Akkaunt o'chirilgan yoki bloklangan")
        
        # JWT token yaratish
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"User login qildi: {user.email}")
        
        return {
            'success': True,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.user_id,
            'email': user.email,
            'name': user.name
        }


class ConflictError(Exception):
    pass


class InvalidCredentialsError(Exception):
    """Email yoki parol noto'g'ri"""
    pass