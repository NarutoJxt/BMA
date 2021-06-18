from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from users.models import User
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

class UserSerializer(ModelSerializer):
    username = serializers.CharField(max_length=16,min_length=8,label="用户名",required=True)
    password = serializers.CharField(max_length=16,min_length=6,label="密码",required=True)

    def create(self, validated_data):
        return User(**validated_data)

    class Meta:
        model = User
        fields = ["username","password"]

class UserRegisterSerializer(ModelSerializer):
    username = serializers.CharField(max_length=16,min_length=8,label="用户名",required=True)
    password1 = serializers.CharField(max_length=120,min_length=8,label="密码",required=True)
    email = serializers.EmailField(max_length=255,required=True,label="邮箱")

    def create(self, validated_data):
        del validated_data["password1"]
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise ValidationError("密码不一致")
        return attrs
    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise ValidationError("用户名已存在")
        else:
            return username
    def validate_email(self,email):
        if User.objects.filter(email=email):
            raise ValidationError("该邮箱已经注册")
        else:
            return email
    class Meta:
        model = User
        fields = ["username","password","password1","email"]

class UserLoginSerializer(JSONWebTokenSerializer):

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("'用户名未激活")

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                raise serializers.ValidationError("用户或密码不对，请重新输入")
        else:

            raise serializers.ValidationError("用户或密码不对，请重新输入")
