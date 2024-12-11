import datetime
from pyexpat.errors import messages

from django.views.generic import ListView

from django.http import HttpResponseForbidden

from main.forms import ReviewForm, ReviewShowForm
from main.models import SearchHistory, EventType
from show.models import ShowProfile, ShowOrderAcceptance
from user.models import User, UserProfile
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from user.models import UserOrder
from company.models import CompanyProfile, CompanyOrderAcceptance, Review
from django.db.models import Avg
import logging

logger = logging.getLogger('orders')



class SearchPlacesView(ListView):
    model = CompanyProfile
    template_name = 'search_places.html'
    context_object_name = 'venues'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            if self.request.user.is_authenticated:
                SearchHistory.objects.create(user=self.request.user, search_query=query)
            return CompanyProfile.objects.filter(company_name__icontains=query)
        return CompanyProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        if self.request.user.is_authenticated:
            context['user'] = User.objects.get(id=self.request.user.id)
            context['Avg'] = Avg
        return context


class SearchShowsView(ListView):
    model = ShowProfile
    template_name = 'search_shows.html'
    context_object_name = 'shows'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            if self.request.user.is_authenticated:
                SearchHistory.objects.create(user=self.request.user, search_query=query)
            return ShowProfile.objects.filter(show_name__icontains=query)
        return ShowProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class EventTypeListView(ListView):
    model = EventType
    template_name = 'event_types.html'
    context_object_name = 'event_types'


@login_required
def venue_profile_user(request, pk):
    company_profile = get_object_or_404(CompanyProfile, pk=pk)

    reviews = company_profile.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or "No ratings yet"

    if request.method == "POST" and 'submit_review' in request.POST:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.venue = company_profile
            review.user = request.user
            review.save()
            return redirect('venue_profile_user', pk=company_profile.pk)
    else:
        review_form = ReviewForm()

    if request.method == "POST" and 'create_order' in request.POST:
        person_number = request.POST.get('person_number')
        date = request.POST.get('order_date')

        if person_number and int(person_number) <= company_profile.capacity:
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"Invalid date format for order creation: {date}")
                return redirect('venue_profile_user', pk=company_profile.pk)

            if date < datetime.date.today():
                logger.warning(f"Attempt to create an order with a past date: {date}")
                return redirect('venue_profile_user', pk=company_profile.pk)

            user = User.objects.get(id=request.user.id)
            order = UserOrder.objects.create(
                user=user,
                order_date=datetime.datetime.now(),
                date=date,
                total_price=(int(person_number) * company_profile.price)
            )

            CompanyOrderAcceptance.objects.create(
                order=order,
                venue=company_profile,
            )

            logger.info(f"Order {order.id} created by user {user.username} for venue {company_profile.company_name} on {date}")
            return redirect('about')
        else:
            logger.warning(
                f"Order creation failed: invalid person number {person_number} for venue {company_profile.company_name}")
            return redirect('venue_profile_user', pk=company_profile.pk)

    context = {
        'company_profile': company_profile,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'user': User.objects.get(id=request.user.id)
    }
    return render(request, 'venue_profile_user.html', context)


@login_required
def show_profile_user(request, pk):
    show_profile = get_object_or_404(ShowProfile, pk=pk)

    reviews = show_profile.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or "No ratings yet"

    if request.method == "POST" and 'submit_review' in request.POST:
        review_form = ReviewShowForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.show = show_profile
            review.user = request.user
            review.save()
            return redirect('show_profile_user', pk=show_profile.pk)
    else:
        review_form = ReviewShowForm()

    if request.method == "POST" and 'create_order' in request.POST:
        date = request.POST.get('order_date')
        if date:
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"Invalid date format for order creation: {date}")
                return redirect('show_profile_user', pk=show_profile.pk)

            if date < datetime.date.today():
                logger.warning(f"Attempt to create an order with a past date: {date}")
                return redirect('show_profile_user', pk=show_profile.pk)

            user = request.user
            user = User.objects.get(id=request.user.id)

            order = UserOrder.objects.create(
                user=user,
                order_date=datetime.datetime.now(),
                date=date,
                total_price=show_profile.price
            )

            ShowOrderAcceptance.objects.create(
                order=order,
                show=show_profile
            )

            logger.info(f"Order {order.id} created by user {user.username} for show {show_profile.show_name} on {date}")
            return redirect('about')
        else:
            logger.warning(f"Order creation failed: missing date for show {show_profile.show_name}")
            return redirect('show_profile_user', pk=show_profile.pk)

    context = {
        'show': show_profile,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'user': User.objects.get(id=request.user.id)
    }
    return render(request, 'show_profile_user.html', context)


@login_required
def profile_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    userProfile = UserProfile.objects.get(user=user)
    context = {
        'user': user,
        'user_profile': userProfile,
    }
    return render(request, 'profile_user.html', context)