from django.shortcuts import render
from rest_framework import authentication
from rest_framework.generics import ListAPIView
# Create your views here.
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Book, Category


class BookMainPageView(ListAPIView):
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # 认证

    def list(self, request, *args, **kwargs):
        categories = Category.objects.all()
        data = []
        for category in categories:
            temp = category.book_set()[:2]
            data.extend(temp)

        return Response(data=data,headers={"Access-Control-Allow-Origin":"*"})