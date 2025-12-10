from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema

from .serializers import (
    SignupRequestSerializer, 
    SignupResponseSerializer,
    LoginRequestSerializer,
    LoginResponseSerializer
)
from .services import (
    SignupService, 
    ConflictError, 
    LoginService, 
    InvalidCredentialsError
)
import logging

logger = logging.getLogger(__name__)


class SignupView(APIView):
    """User ro'yxatdan o'tish API endpoint"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=SignupRequestSerializer,
        responses={201: SignupResponseSerializer},
        description="Yangi user ro'yxatdan o'tkazish"
    )
    def post(self, request):
        serializer = SignupRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Validatsiya xatoligi',
                'message': 'Yuborilgan ma\'lumotlar noto\'g\'ri',
                'details': serializer.errors,
                'status_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        signup_service = SignupService()
        
        try:
            result = signup_service.register_user(
                name=serializer.validated_data['name'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            response_serializer = SignupResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except ConflictError as e:
            return Response({
                'error': 'Conflict',
                'message': str(e),
                'status_code': 409
            }, status=status.HTTP_409_CONFLICT)
        
        except ValidationError as e:
            return Response({
                'error': 'Validatsiya xatoligi',
                'message': str(e),
                'status_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Kutilmagan xatolik: {str(e)}", exc_info=True)
            return Response({
                'error': 'Server xatoligi',
                'message': 'Ichki server xatoligi yuz berdi',
                'status_code': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    """User login API endpoint"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=LoginRequestSerializer,
        responses={200: LoginResponseSerializer},
        description="User tizimga kirish"
    )
    def post(self, request):
        """User login qilish"""
        
        serializer = LoginRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': 'Validatsiya xatoligi',
                'message': 'Yuborilgan ma\'lumotlar noto\'g\'ri',
                'details': serializer.errors,
                'status_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        login_service = LoginService()
        
        try:
            result = login_service.login_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            response_serializer = LoginResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        except InvalidCredentialsError as e:
            return Response({
                'error': 'Unauthorized',
                'message': str(e),
                'status_code': 401
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            logger.error(f"Login xatolik: {str(e)}", exc_info=True)
            return Response({
                'error': 'Server xatoligi',
                'message': 'Ichki server xatoligi yuz berdi',
                'status_code': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)