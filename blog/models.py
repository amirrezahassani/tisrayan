from django.db import models
from django.conf import settings
from khayyam import JalaliDate
from django.urls import reverse


# مدل دسته‌بندی (Category)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# مدل برچسب (Tag)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# مدل پست وبلاگ (Post)
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ارتباط با مدل CustomUser
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def jalali_created_at(self):
        return JalaliDate(self.created_at).strftime('%Y/%m/%d')

    def jalali_updated_at(self):
        return JalaliDate(self.updated_at).strftime('%Y/%m/%d')

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    approved = models.BooleanField(default=False)  # تایید کامنت

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

    @property
    def is_admin_reply(self):
        return self.parent and self.user.is_staff
