from django.urls import path

from .views import BookMainPageView
app_name = "book"

urlpatterns = [
    path("index/",BookMainPageView.as_view(),name="index")
]
