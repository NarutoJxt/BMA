from datetime import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import authentication, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer


class LoginView(ObtainJSONWebToken):
    serializer_class = UserLoginSerializer



class RegisterView(CreateModelMixin, GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # 认证

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            re_dict = {}
            re_dict["resgister_res"] = True
            payload = jwt_payload_handler(user)
            re_dict["token"] = jwt_encode_handler(payload)
            re_dict["name"] = user.name if user.name else user.username
            return Response(
                re_dict
            ,status=HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,status=HTTP_400_BAD_REQUEST
            )
