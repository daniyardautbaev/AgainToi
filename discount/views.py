from django.views.generic import ListView, DetailView
from .models import Discount

from django.views.generic import ListView
from .models import Discount


class DiscountListView(ListView):
    model = Discount
    template_name = 'discount/discount_list.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        # Добавляем расчет скидочной цены для каждого объекта
        discounts = super().get_queryset()
        for discount in discounts:
            discount.status = discount.get_status()
            if discount.show:
                discount.show_discounted_price = discount.get_discounted_price(discount.show)
            else:
                discount.show_discounted_price = None

            if discount.company:
                discount.company_discounted_price = discount.get_discounted_price(discount.company)
            else:
                discount.company_discounted_price = None
        return discounts
class DiscountDetailView(DetailView):
    model = Discount
    template_name = 'discount/discount_detail.html'
