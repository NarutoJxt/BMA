import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


class UserAuthBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",username):
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user


