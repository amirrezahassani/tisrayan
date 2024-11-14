# from django.shortcuts import redirect
# from django.urls import reverse

# class AdminLoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # اگر درخواست مربوط به admin باشد
#         if request.path.startswith('/admin/'):
#             # بررسی کنیم آیا کاربر وارد شده است
#             if not request.user.is_authenticated:
#                 return redirect(reverse('login'))  # ریدایرکت به صفحه ورود
#             # بررسی کنیم آیا کاربر سوپریوزر است
#             if not request.user.is_superuser:
#                 return redirect(reverse('login'))  # یا به صفحه مورد نظر شما
        
#         return self.get_response(request)

from django.shortcuts import redirect
from django.urls import reverse

class AdminLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اگر درخواست مربوط به admin باشد
        if request.path.startswith('/admin/'):
            # بررسی کنیم آیا کاربر وارد شده است
            if not request.user.is_authenticated:
                return redirect(reverse('login'))  # ریدایرکت به صفحه ورود
            
            # اگر کاربر سوپریوزر است، اجازه دسترسی مستقیم بده
            if request.user.is_superuser:
                return self.get_response(request)

            # اگر کاربر سوپریوزر نیست به صفحه لاگین هدایت شود
            return redirect(reverse('login'))
        
        return self.get_response(request)
