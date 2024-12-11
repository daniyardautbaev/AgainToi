from django.urls import path
from . import views
from .views import update_company_profile

urlpatterns = [
    path('order/accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('register/', views.CompanyRegister, name='venue_register'),
    path('profile/', views.CompanyProfileView, name='venue_profile'),
    path('order/', views.Order, name='order'),
    path('debug/orders/', views.debug_orders, name='debug_orders'),
    path('profile/update/', update_company_profile, name='update_company_profile'),
]
