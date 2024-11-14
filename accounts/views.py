from django.contrib.auth import login, authenticate
from .forms import CustomAuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import CustomUser
from .tokens import account_activation_token
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from .models import Invoice


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # بررسی اینکه آیا گزینه به خاطر سپاری تیک خورده است یا خیر
                remember_me = request.POST.get('remember_me', None)

                if remember_me:
                    # Session را تا 1 ماه حفظ می‌کند
                    request.session.set_expiry(2592000)  # 30 روز
                else:
                    # Session بعد از بسته شدن مرورگر منقضی می‌شود
                    request.session.set_expiry(0)

                login(request, user)
                return redirect('index')  # صفحه‌ای که بعد از ورود هدایت می‌شود
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # کاربر غیر فعال است تا زمانی که ایمیل تأیید شود
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    return render(request, 'account.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "این ایمیل در سیستم ما وجود ندارد.")
            return render(self.request, self.template_name, {'form': form})
        return super().form_valid(form)


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:  # اگر کاربر رمز جدیدی وارد کرده باشد
                user.set_password(password)
            user.save()
            messages.success(request, 'تغییرات با موفقیت ذخیره شد.')
            return redirect('account')
    else:
        form = CustomUserForm(instance=user)

    invoices = Invoice.objects.filter(user=request.user)

    return render(request, 'account.html', {'form': form, 'invoices': invoices})
