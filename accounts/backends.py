from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # تلاش برای ورود با ایمیل
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # اگر کاربر با ایمیل وجود ندارد، تلاش برای ورود با نام کاربری
            user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            return user
        return None
