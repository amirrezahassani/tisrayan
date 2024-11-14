from django.contrib import admin
from .models import Category, Tag, Post, Comment


# تنظیمات ادمین برای مدل Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # نمایش فیلدهای name و slug در لیست دسته‌بندی‌ها
    search_fields = ('name',)  # قابلیت جستجو در فیلد name
    prepopulated_fields = {'slug': ('name',)}  # پر کردن خودکار slug بر اساس نام


# تنظیمات ادمین برای مدل Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # نمایش فیلدهای name و slug در لیست برچسب‌ها
    search_fields = ('name',)  # قابلیت جستجو در فیلد name
    prepopulated_fields = {'slug': ('name',)}  # پر کردن خودکار slug بر اساس نام


# تنظیمات ادمین برای مدل Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')  # نمایش عنوان، نویسنده، تاریخ ایجاد و وضعیت انتشار
    list_filter = (
    'is_published', 'categories', 'tags', 'author')  # فیلتر بر اساس وضعیت انتشار، دسته‌بندی، برچسب و نویسنده
    search_fields = ('title', 'content')  # قابلیت جستجو در عنوان و محتوای پست‌ها
    prepopulated_fields = {'slug': ('title',)}  # پر کردن خودکار slug بر اساس عنوان
    date_hierarchy = 'created_at'  # قابلیت مرتب‌سازی بر اساس تاریخ ایجاد
    filter_horizontal = ('categories', 'tags')  # استفاده از ویجت انتخاب چندگانه برای دسته‌بندی‌ها و برچسب‌ها
    readonly_fields = ('created_at', 'updated_at')  # فیلدهای فقط خواندنی
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'image', 'author', 'is_published')
        }),
        ('Categories & Tags', {
            'fields': ('categories', 'tags'),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


# تنظیمات ادمین برای مدل Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'approved')  # نمایش پست، کاربر، تاریخ و وضعیت تایید کامنت
    list_filter = ('approved', 'created_at')  # فیلتر بر اساس وضعیت تایید و تاریخ ایجاد
    search_fields = ('user__username', 'content')  # قابلیت جستجو بر اساس نام کاربری و متن کامنت
    actions = ['approve_comments']  # افزودن اکشن تایید گروهی کامنت‌ها

    # اکشن برای تایید گروهی کامنت‌ها
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = 'تایید کامنت‌های انتخاب‌شده'
