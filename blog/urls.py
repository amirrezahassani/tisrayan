from django.urls import path
from . import views
from .views import post_detail_view

urlpatterns = [
    path('', views.post_list_view, name='posts_list'),
    path('<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/', post_detail_view, name='post_detail'),
]
