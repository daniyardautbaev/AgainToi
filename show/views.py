from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import logging
from django.utils.timezone import now
from user.form import AddressForm
from user.models import Cart
from .models import ShowProfile, Host, Photographer, CameraOperator, Dancer, Singer, ShowOrderAcceptance
from .forms import SingerForm, HostForm, CameraOperatorForm, PhotographerForm, DancerForm, ShowProfileForm

logger = logging.getLogger('orders')


@login_required
def ShowProfileRegisterView(request):
    if ShowProfile.objects.filter(user=request.user).exists():
        return redirect('about')

    if request.method == 'POST':
        addressForm = AddressForm(request.POST, request.FILES)
        if addressForm.is_valid():
            show_name = request.POST.get('show_name')
            host_id = request.POST.get('host')
            photographer_id = request.POST.get('photographer')
            camera_operator_id = request.POST.get('camera_operator')
            dancers_ids = request.POST.getlist('dancers')
            singers_ids = request.POST.getlist('singers')
            price = request.POST.get('price')

            host = Host.objects.filter(id=host_id).first()
            photographer = Photographer.objects.filter(id=photographer_id).first()
            camera_operator = CameraOperator.objects.filter(id=camera_operator_id).first()

            show_profile = ShowProfile.objects.create(
                user=request.user,
                show_name=show_name,
                host=host,
                photographer=photographer,
                camera_operator=camera_operator,
                price=price
            )

            show_profile.dancer.set(Dancer.objects.filter(id__in=dancers_ids))
            show_profile.singer.set(Singer.objects.filter(id__in=singers_ids))

            return redirect('about')
    else:
        addressForm = AddressForm()

    context = {
        'hosts': Host.objects.all(),
        'photographers': Photographer.objects.all(),
        'camera_operators': CameraOperator.objects.all(),
        'dancers': Dancer.objects.all(),
        'singers': Singer.objects.all(),
        'addressForm': addressForm,
    }
    return render(request, 'show_register.html', context)


def RegisterEntity(request, entity_name):
    forms_map = {
        'singer': SingerForm,
        'dancer': DancerForm,
        'host': HostForm,
        'photographer': PhotographerForm,
        'camera_operator': CameraOperatorForm,
    }
    form_class = forms_map.get(entity_name)
    if not form_class:
        return render(request, '404.html', {'message': 'Entity not found'})

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'{entity_name.capitalize()} successfully registered!')
            return redirect('/show/register/')
    else:
        form = form_class()

    return render(request, 'register_entity.html', {
        'form': form,
        'title': f'Register {entity_name.capitalize()}',
    })


@login_required
def ShowProfileView(request):
    user = request.user
    showProfile = ShowProfile.objects.get(user=user)
    context = {
        "show": showProfile
    }
    return render(request, 'show_profile.html', context)


@login_required
def Order(request):
    try:
        show = ShowProfile.objects.get(user=request.user)
    except ShowProfile.DoesNotExist:
        return render(request, 'order_show.html', {'orders': [], 'error': 'No company profile found for the user.'})

    orders = ShowOrderAcceptance.objects.filter(show=show)
    for order in orders:
        print(
            f"Заказ ID: {order.order.id}, Пользователь: {order.order.user.email}, Принят: {order.accepted}")

    return render(request, 'order_show.html', {'orders': orders, 'error': None})


@login_required
def accept_order_show(request, order_id):
    order = get_object_or_404(ShowOrderAcceptance, pk=order_id)

    if not order.accepted:
        order.accepted = True
        order.accepted_date = now()
        order.save()

        user = order.order.user
        show_name = order.show.show_name

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            order=order.order,
            company_name=show_name + " show",
            defaults={'added_date': now()}
        )

        if created:
            logger.info(f"Order {order.order.id} accepted and added to cart for user {user.username} ({show_name} show).")
        else:
            logger.info(f"Order {order.order.id} already exists in the cart for user {user.username} ({show_name} show).")
    else:
        logger.warning(f"Order {order.order.id} for user {order.order.user.username} already marked as accepted.")

    return redirect('order_show')


@login_required
def ShowProfileView(request):
    user = request.user
    showProfile = ShowProfile.objects.filter(user=user).first()
    if not showProfile:
        return render(request, '404.html', {'message': 'Show profile not found'})
    context = {
        "show": showProfile
    }
    return render(request, 'show_profile.html', context)


@login_required
def EditShowProfile(request, pk):
    show_profile = get_object_or_404(ShowProfile, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ShowProfileForm(request.POST, request.FILES, instance=show_profile)
        if form.is_valid():
            form.save()
            return redirect('show_profile')
    else:
        form = ShowProfileForm(instance=show_profile)

    context = {
        'form': form
    }
    return render(request, 'edit_show_profile.html', context)
