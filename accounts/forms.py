from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')  # اجازه ورود با ایمیل یا نام کاربری


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # ایمیل به‌عنوان فیلد الزامی
    accept_terms = forms.BooleanField(
        label="من قوانین و مقررات را خوانده و موافقم",
        required=True,
        error_messages={'required': 'باید با قوانین و مقررات موافقت کنید.'}
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2', 'accept_terms')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="رمز عبور جدید")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label="تایید رمز عبور")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company_name', 'fixed_phone', 'address',
                  'birth_date', 'password', 'confirm_password']

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if company_name is None or company_name.strip() == "":
            return None
        return company_name

    def clean_fixed_phone(self):
        fixed_phone = self.cleaned_data.get('fixed_phone')
        if fixed_phone is None or fixed_phone.strip() == "":
            return None
        return fixed_phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("لطفا یک آدرس ایمیل معتبر وارد کنید.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not re.match(r'^\+?\d{10,15}$', phone_number):  # شماره تلفن باید عددی باشد
            raise ValidationError("لطفا یک شماره تلفن معتبر وارد کنید.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            self.add_error('confirm_password', "رمز عبور و تایید رمز عبور مطابقت ندارند.")
