from django.conf import settings
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name


class Media(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        db_index=True
    )
    photo = models.ImageField(upload_to='media/photos/', blank=True, null=True)
    video = models.FileField(upload_to='media/videos/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Media by {self.user.name} - {self.created_at}"

