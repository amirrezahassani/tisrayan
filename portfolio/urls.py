from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_view, name='portfolio_view'),
    path('<slug:slug>/', views.portfolio_single, name='portfolio_single'),
]
