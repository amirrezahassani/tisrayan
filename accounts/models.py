from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)  # شماره موبایل
    company_name = models.CharField(max_length=100, blank=True, null=True)  # نام شرکت
    fixed_phone = models.CharField(max_length=15, blank=True, null=True)  # شماره تماس ثابت
    address = models.TextField(blank=True, null=True)  # آدرس
    birth_date = models.DateField(blank=True, null=True)  # تاریخ تولد
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # تصویر پروفایل
    is_verified = models.BooleanField(default=False)  # وضعیت تایید شماره یا ایمیل

    def __str__(self):
        return self.username


class Invoice(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=20)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='invoices/')

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.user.username}"
