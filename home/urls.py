from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', about, name=''),
    path('about/', about, name='about'),
    path('contact/', contact_view, name='contact'),
    path('thanks/', thanks_view, name='thanks'),
    path('media/', media_list, name='media'),
    path('media-add/', add_media, name='add-media'),
    path('media/<int:pk>/', media_detail, name='media-detail'),

]
