from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from company.models import CompanyProfile
from home.forms import ContactForm, MediaForm
from home.models import Media

# Create your views here.

import json


def about(request):
    companies = CompanyProfile.objects.all().order_by('-capacity')[:5]
    companies2 = CompanyProfile.objects.all().order_by('-price')[:5]

    company_names = [company.company_name for company in companies]
    company_names2 = [company.company_name for company in companies2]

    capacities = [company.capacity for company in companies]
    prices = [company.price for company in companies2]

    venue_types = CompanyProfile.objects.values_list('venue_type', flat=True)



    venue_type_counts = {}

    for vt in venue_types:
        venue_type_counts[vt] = venue_type_counts.get(vt, 0) + 1

    return render(request, "about/about.html", {
        'companies': companies,
        'company_names': json.dumps(company_names),
        'capacities': json.dumps(capacities),
        'venue_type_counts': json.dumps(venue_type_counts),

        'companies2': companies2,
        'company_names2': company_names2,
        'prices': prices
    })


def media(request):
    return render(request, "media/media.html")


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


def thanks_view(request):
    return render(request, 'contact/thanks.html')


# media
def media_list(request):
    medias = Media.objects.all().order_by('-created_at')
    return render(request, 'media/media.html', {'medias': medias})


def media_detail(request, pk):
    media_ = get_object_or_404(Media, pk=pk)
    return render(request, 'media/media-detail.html', {'media': media_})


@login_required
def add_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media_ = form.save(commit=False)
            media_.user = request.user
            media_.save()
            return redirect('media')
    else:
        form = MediaForm()
    return render(request, 'media/media-add.html', {'form': form})
