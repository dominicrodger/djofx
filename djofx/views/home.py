from django.db.models import Sum
from django.views.generic import TemplateView
from djofx.forms import OFXForm
from djofx.views.base import PageTitleMixin
from djofx import models


class HomePageView(PageTitleMixin, TemplateView):
    template_name = "djofx/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['accounts'] = models.Account.objects.filter(
            owner=self.request.user
        )

        context['form'] = OFXForm()

        breakdown = models.Transaction.objects.filter(
            amount__lt=0,
            transaction_category__is_void=False
        ).values(
            'transaction_category__pk',
            'transaction_category__name'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')
        context['breakdown'] = [
            (
                abs(item['total']),
                item['transaction_category__pk'],
                item['transaction_category__name']
            )
            for item in breakdown
        ]

        return context
