from datetime import date

from django.db import models
from django.conf import settings
from show.models import ShowProfile
from company.models import CompanyProfile
class Discount(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    show = models.ForeignKey(ShowProfile, on_delete=models.CASCADE, related_name='discounts', blank=True, null=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='discounts', blank=True, null=True)

    def get_discounted_price(self, profile):
        """
        Calculate the discounted price for a given profile (ShowProfile or CompanyProfile).
        """
        if not profile or profile.price is None:  # Проверка на наличие цены
            return None
        if self.is_active:
            discount_amount = profile.price * (self.percentage / 100)
            return max(profile.price - discount_amount, 0)
        return profile.price

    def get_status(self):
        """
        Возвращает статус скидки: Активна, Истекла или Не началась.
        """
        today = date.today()
        if not self.is_active:
            return "Inactive"
        if self.start_date > today:
            return "Not Started"
        if self.end_date < today:
            return "Expired"
        return "Active"

