from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from persiantools.jdatetime import JalaliDate
from .models import Invoice


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'phone_number', 'address', 'birth_date', 'profile_image',
                'is_verified', 'company_name', 'fixed_phone'
            )
        }),
    )

    list_display = ('username', 'email', 'is_verified', 'is_active', 'is_staff', 'get_birth_date')
    search_fields = ('username', 'email', 'phone_number')

    def get_birth_date(self, obj):
        """تبدیل تاریخ تولد میلادی به شمسی"""
        if obj.birth_date:
            jalali_date = JalaliDate(obj.birth_date)  # تبدیل تاریخ میلادی به شمسی
            return f"{jalali_date.year}/{jalali_date.month}/{jalali_date.day}"  # فرمت شمسی
        return "تاریخ مشخص نشده"

    get_birth_date.short_description = 'تاریخ تولد'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'date')
    search_fields = ('user__username', 'amount')
    list_filter = ('date',)


# ثبت مدل CustomUser در پنل ادمین
admin.site.register(CustomUser, CustomUserAdmin)
