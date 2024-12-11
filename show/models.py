from django.db import models
from django.conf import settings
from user.models import UserOrder, Address


class Host(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='show/host/profile_images/',
        blank=True,
        null=True,
        default='default_images/default.png'
    )
    video = models.FileField(
        upload_to='show/host/videos/',
        blank=True,
        null=True
    )
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Photographer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='show/photographer/profile_images/',
        blank=True,
        null=True,
        default='default_images/default.png'
    )
    video = models.FileField(
        upload_to='show/photographer/videos/',
        blank=True,
        null=True
    )
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class CameraOperator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='show/cameraOperator/profile_images/',
        blank=True,
        null=True,
        default='default_images/default.png'
    )
    video = models.FileField(
        upload_to='show/cameraOperator/videos/',
        blank=True,
        null=True
    )
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Dancer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='show/dancer/profile_images/',
        blank=True,
        null=True,
        default='default_images/default.png'
    )
    video = models.FileField(
        upload_to='show/dancer/videos/',
        blank=True,
        null=True
    )
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Singer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to='show/singer/profile_images/',
        blank=True,
        null=True,
        default='default_images/default.png'
    )
    video = models.FileField(
        upload_to='show/singer/videos/',
        blank=True,
        null=True
    )
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class ShowProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show_name = models.CharField(max_length=100, unique=True)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True, blank=True)
    photographer = models.ForeignKey(Photographer, on_delete=models.SET_NULL, null=True, blank=True)
    camera_operator = models.ForeignKey(CameraOperator, on_delete=models.SET_NULL, null=True, blank=True)

    dancer = models.ManyToManyField(Dancer, blank=True)
    singer = models.ManyToManyField(Singer, blank=True)
    price = models.IntegerField(null=True, blank=True)


class ShowOrderAcceptance(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE)
    show = models.ForeignKey(ShowProfile, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)


class ShowReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show = models.ForeignKey(ShowProfile, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.name} for {self.show.show_name}"
