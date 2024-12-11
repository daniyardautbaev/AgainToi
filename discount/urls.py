from django.urls import path
from . import views

urlpatterns = [
    path('', views.DiscountListView.as_view(), name='discount_list'),
]
