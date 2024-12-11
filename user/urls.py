from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, UserProfileView, UserProfileRegister, Cart, \
    get_cities, view_cart, add_to_cart

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileRegister, name='user_register'),
    path('user_profile/', UserProfileView, name='user_profile'),
    path('cart/', view_cart, name='view_cart'),
]