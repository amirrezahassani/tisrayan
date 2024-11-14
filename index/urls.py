from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('contact-us/', views.contact_view, name='contact'),

    path('rules/', views.rules, name='rules'),

    path('services/', views.services, name='services'),
    path('services/web-design/', views.web_design, name='web_design'),
    path('services/graphic-design/', views.graphic_design, name='graphic_design'),
    path('services/content-creator/', views.content_creator, name='content_creator'),
    path('services/socialmedia-admin/', views.socialmedia_admin, name='socialmedia_admin'),
    path('services/seo/', views.seo, name='seo'),
]
