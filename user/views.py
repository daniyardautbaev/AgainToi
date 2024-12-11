from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from company.models import CompanyOrderAcceptance

from .form import AddressForm
from .serializers import UserSerializer, AddressSerializer
from .models import User, UserProfile, Address, City, Cart
import jwt, datetime
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse


class RegisterView(APIView):
    def get(self, request):
        user_type = request.GET.get('user_type')
        if not user_type:
            return render(request, 'register.html', {'error': 'Please select a user type.'})

        return render(request, 'register.html', {'user_type': user_type})

    def post(self, request):
        user_type = request.GET.get('user_type')
        data = {
            'user_type': user_type,
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            auth_login(request, user)
            return redirect(user_type + '_register')

        return render(request, 'register.html', {'errors': serializer.errors})


class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = redirect('about')  # Убедитесь, что маршрут "about" существует
        response.set_cookie(key='jwt', value=token, httponly=True)
        auth_login(request, user)
        print(f"Generated token: {token}")
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id=payload['id'])

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id=payload['id'])
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = Response({
            "message": "Successfully logged out!"
        })
        response.delete_cookie('jwt')
        return redirect('about')


@login_required
def UserProfileView(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'profile.html', {'user': user, 'user_profile': user_profile})


@login_required
def UserProfileRegister(request):
    if UserProfile.objects.filter(user=request.user).exists():
        return redirect('about')

    if request.method == 'POST':
        addressForm = AddressForm(request.POST, request.FILES)

        if addressForm.is_valid():
            address = addressForm.save()

            phone = request.POST.get('phone')
            image = request.FILES.get('image')

            UserProfile.objects.create(
                user=request.user,
                address=address,
                phone=phone,
                image=image,
            )

            return redirect('about')

    else:
        addressForm = AddressForm()

    return render(request, 'userProfile_register.html', {'addressForm': addressForm})


def get_cities(request, region_id):
    cities = City.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


@login_required
def add_to_cart(request, order_id):
    company_order = get_object_or_404(CompanyOrderAcceptance, pk=order_id)

    if not company_order.accepted:
        return HttpResponse("Order not yet accepted by the company.", status=400)

    user = company_order.order.user
    if not Cart.objects.filter(user=user, order=company_order.order).exists():
        Cart.objects.create(user=user, order=company_order.order, added_date=now())

    return HttpResponse("Order added to the cart successfully.")


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=User.objects.get(id=request.user.id))
    return render(request, 'cart.html', {'cart_items': cart_items})
