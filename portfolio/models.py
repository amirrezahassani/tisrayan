from django.db import models
from khayyam import JalaliDate


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PF(models.Model):
    OPTION_CHOICES = [
        ('site', 'Site'),
        ('design', 'Design'),
        ('content', 'Content'),
        ('seo', 'SEO'),
        ('social', 'Social'),
    ]
    name = models.CharField(max_length=255)  # اسم نمونه کار
    description = models.TextField()  # توضیحات
    published_date = models.DateField()  # تاریخ انتشار
    client_name = models.CharField(max_length=255, blank=True)  # نام مشتری
    url = models.URLField(blank=True)  # آدرس پروژه آنلاین
    slug = models.SlugField(unique=True)  # اسلاگ برای URL دوستانه
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # دسته‌بندی
    technology_used = models.CharField(max_length=255, blank=True)  # تکنولوژی‌های استفاده شده
    testimonial = models.TextField(blank=True)  # نظر مشتری
    tags = models.ManyToManyField(Tag, blank=True)  # برچسب‌ها
    featured = models.BooleanField(default=False)  # پروژه ویژه
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد
    lable_to_show = models.CharField(
        max_length=10,
        choices=OPTION_CHOICES,
        default='site',
        verbose_name="show in portfolio",
    )
    image1 = models.ImageField(upload_to='portfolio_images/', blank=True)
    image2 = models.ImageField(upload_to='portfolio_images/', blank=True)
    image3 = models.ImageField(upload_to='portfolio_images/', blank=True)

    def __str__(self):
        return self.name

    def jalali_created_at(self):
        return JalaliDate(self.created_at).strftime('%Y/%m/%d')
