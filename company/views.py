from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from company.forms import AddressForm, CompanyProfileForm
from company.models import CompanyProfile, CompanyOrderAcceptance
from user.models import Address, UserOrder, Cart
from datetime import datetime
from django.http import HttpResponse
from django.utils.timezone import now
import logging

logger = logging.getLogger('orders')


@login_required
def CompanyRegister(request):
    if CompanyProfile.objects.filter(user=request.user).exists():
        return redirect('about')

    if request.method == 'POST':
        addressForm = AddressForm(request.POST, request.FILES)

        if addressForm.is_valid():
            address = addressForm.save()

            company_name = request.POST.get('company_name')
            capacity = request.POST.get('capacity')
            venue_type = request.POST.get('venue_type')
            image = request.FILES.get('image')
            video = request.FILES.get('video')
            price = request.POST.get('price')

            CompanyProfile.objects.create(
                user=request.user,
                company_name=company_name,
                address=address,
                capacity=capacity,
                venue_type=venue_type,
                image=image,
                video=video,
                price=price
            )

            return redirect('about')
    else:
        addressForm = AddressForm()

    return render(request, 'venue_register.html', {'addressForm': addressForm})


@login_required
def CompanyProfileView(request):
    user = request.user
    company_profile = CompanyProfile.objects.get(user=user)
    return render(request, 'venue_profile.html', {'user': user, 'company_profile': company_profile})


@login_required
def Order(request):
    try:
        company = request.user.companyprofile
        print(f"Компания: {company.company_name}")
    except CompanyProfile.DoesNotExist:
        print("CompanyProfile не найден для текущего пользователя.")
        return render(request, 'order.html', {'orders': [], 'error': 'No company profile found for the user.'})

    orders = CompanyOrderAcceptance.objects.filter(venue=company)
    print(f"Количество заказов: {orders.count()}")
    for order in orders:
        print(
            f"Заказ ID: {order.order.id}, Пользователь: {order.order.user.email}, Принят: {order.accepted}")  # Отладочный вывод

    return render(request, 'order.html', {'orders': orders, 'error': None})


@login_required
def accept_order(request, order_id):
    order = get_object_or_404(CompanyOrderAcceptance, pk=order_id)

    if not order.accepted:
        order.accepted = True
        order.accepted_date = now()
        order.save()

        user = order.order.user
        company_name = order.venue.company_name

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            order=order.order,
            company_name=company_name + " venue",
            defaults={'added_date': now()}
        )

        if created:
            logger.info(f"Order {order.order.id} accepted and added to cart for user {user.username}.")
        else:
            logger.info(f"Order {order.order.id} already exists in the cart for user {user.username}.")

    return redirect('order')


@login_required
def debug_orders(request):
    try:
        company = request.user.companyprofile
    except CompanyProfile.DoesNotExist:
        return HttpResponse("No company profile found for the user.")

    orders = CompanyOrderAcceptance.objects.filter(venue=company)
    output = f"<h2>Количество заказов: {orders.count()}</h2><ul>"
    for order in orders:
        output += f"<li>Order ID: {order.order.id}, User Email: {order.order.user.email}, Accepted: {order.accepted}</li>"
    output += "</ul>"
    return HttpResponse(output)


@login_required
def update_company_profile(request):
    company_profile = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile)
        if form.is_valid():
            form.save()
            return redirect('venue_profile')
    else:
        form = CompanyProfileForm(instance=company_profile)

    return render(request, 'update_company_profile.html', {'form': form})
