from datetime import datetime

from django.db import models
from django.conf import settings
from user.models import UserOrder, Address, Cart
from django.core.exceptions import ValidationError


class CompanyProfile(models.Model):
    VENUE_TYPES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Cafe'),
        ('hall', 'Hall'),
        ('club', 'Club'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.IntegerField()
    venue_type = models.CharField(max_length=50, choices=VENUE_TYPES)

    image = models.ImageField(upload_to='company/profile_images/', blank=True, null=True,
                              default='company/profile_images/information_items_property_13610.jpg')
    video = models.FileField(upload_to='company/videos/', blank=True, null=True, default="company/videos/venue.mp4")
    price = models.IntegerField(null=True, blank=True)
    panorama = models.ImageField(upload_to='company/panoramas/', blank=True, null=True,
                                 help_text="Upload a 360-degree panorama")


class CompanyCalendar(models.Model):
    venue = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)


class CompanyOrderAcceptance(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE)
    venue = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    person_number = models.IntegerField(null=True, blank=True)

    def clean(self):
        if self.person_number and self.venue and self.person_number > self.venue.capacity:
            raise ValidationError({'person_number': 'Person number cannot exceed venue capacity.'})

    def save(self, *args, **kwargs):
        if self.accepted and self.accepted_date is None:
            self.accepted_date = datetime.datetime.now()

            if not Cart.objects.filter(user=self.order.user, order=self.order).exists():
                Cart.objects.create(user=self.order.user, order=self.order)

            self.order.status = "In Cart"
            self.order.save()

        super().save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    venue = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.name} for {self.venue.company_name}"
