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
    
    email = serializers.EmailField(
        required=True,
        max_length=255,
        error_messages={
            'required': 'Email majburiy maydon',
            'invalid': 'Noto\'g\'ri email formati',
            'blank': 'Email bo\'sh bo\'lmasligi kerak'
        }
    )
    
    password = serializers.CharField(
        required=False,
        min_length=8,
        max_length=128,
        write_only=True,
        style={'input_type': 'password'},
        error_messages={
            'blank': 'Parol bo\'sh bo\'lmasligi kerak',
            'min_length': 'Parol kamida 8 belgidan iborat bo\'lishi kerak',
            'max_length': 'Parol 128 belgidan oshmasligi kerak'
        }
    )


class SignupResponseSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    login = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    success = serializers.BooleanField(read_only=True, default=True)


# Login Serializers
class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email majburiy maydon',
            'invalid': 'Noto\'g\'ri email formati'
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
    email = serializers.EmailField(read_only=True)
    name = serializers.CharField(read_only=True)