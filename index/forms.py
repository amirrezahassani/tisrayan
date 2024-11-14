from django import forms
from .models import ContactMessage
import re  # برای استفاده از عبارات منظم


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-bg-color-light-1 border-0'}),
            'email': forms.EmailInput(attrs={'class': 'form-control custom-bg-color-light-1 border-0'}),
            'phone': forms.TextInput(attrs={'class': 'form-control custom-bg-color-light-1 border-0'}),
            'message': forms.Textarea(attrs={'class': 'form-control custom-bg-color-light-1 border-0', 'rows': 6}),
        }
        labels = {
            'name': "نام و نام خانوادگی",
            'email': "ایمیل",
            'phone': "تلفن همراه",
            'message': "پیغام",
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('لطفا نام و نام خانوادگی خود را وارد کنید.')
        # بررسی اینکه نام تنها شامل حروف باشد
        if not re.match(r'^[\u0600-\u06FF\s]+$', name):  # برای نام‌های فارسی
            raise forms.ValidationError('لطفا فقط حروف فارسی و فاصله را وارد کنید.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('لطفا شماره تلفن خود را وارد کنید.')
        # بررسی اینکه شماره تلفن تنها شامل اعداد باشد
        if not re.match(r'^\d+$', phone):  # تنها اعداد
            raise forms.ValidationError('لطفا تنها از اعداد استفاده کنید.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('لطفا آدرس ایمیل خود را وارد کنید.')
        return email
