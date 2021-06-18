from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    name = models.CharField(verbose_name="用户名",max_length=64,blank=False,null=False)
    email = models.EmailField(verbose_name="邮箱",max_length=255,blank=False,null=False)
    profile = models.ImageField(verbose_name="头像",default="/image/img.png")
    job = models.CharField(verbose_name="工作",max_length=64,blank=True,null=True)



