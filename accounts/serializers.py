from rest_framework import serializers


class SignupRequestSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        max_length=150,
        min_length=2,
        trim_whitespace=True,
        error_messages={
            'required': 'Ism majburiy maydon',
            'blank': 'Ism bo\'sh bo\'lmasligi kerak',
            'min_length': 'Ism kamida 2 belgidan iborat bo\'lishi kerak',
            'max_length': 'Ism 150 belgidan oshmasligi kerak'
        }
    )
    
    phone = serializers.CharField(
        required=True,
        max_length=20,
        error_messages={
            'required': 'Telefon raqam majburiy maydon',
            'blank': 'Telefon raqam bo\'sh bo\'lmasligi kerak'
        }
    )


class SignupResponseSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(read_only=True)
    phone = serializers.CharField(read_only=True)
    login = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    success = serializers.BooleanField(read_only=True, default=True)


# Login Serializers
class LoginRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Telefon raqam majburiy maydon'
        }
    )
    
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            'required': 'Parol majburiy maydon'
        }
    )


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    phone = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)