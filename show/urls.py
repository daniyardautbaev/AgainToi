from django.urls import path
from .views import ShowProfileRegisterView, RegisterEntity, ShowProfileView, Order, accept_order_show, EditShowProfile

urlpatterns = [
    path('register/', ShowProfileRegisterView, name='show_register'),
    path('profile/', ShowProfileView, name='show_profile'),
    path('order/', Order, name='order_show'),
    path('register/<str:entity_name>/', RegisterEntity, name='register_entity'),
    path('order/accept/<int:order_id>/', accept_order_show, name='accept_order_show'),
    path('profile/edit/<int:pk>/', EditShowProfile, name='edit_show_profile'),
    path('profile/', ShowProfileView, name='show_profile')
]
