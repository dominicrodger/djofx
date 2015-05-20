from datetime import date, timedelta
from django.db.models import Sum
from django.views.generic import TemplateView
from djofx.forms import OFXForm
from djofx.views.base import PageTitleMixin, UserRequiredMixin
from djofx import models
from operator import itemgetter


class HomePageView(PageTitleMixin, UserRequiredMixin, TemplateView):
    template_name = "djofx/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['accounts'] = models.Account.objects.filter(
            owner=self.request.user
        )

        context['form'] = OFXForm()

        cutoff = date.today() - timedelta(days=120)

        uncategorised_breakdown = models.Transaction.objects.filter(
            amount__lt=0,
            transaction_category__isnull=True,
            date__gte=cutoff
        ).aggregate(
            total=Sum('amount')
        )

        breakdown = models.Transaction.objects.filter(
            amount__lt=0,
            transaction_category__is_void=False,
            date__gte=cutoff
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
        context['breakdown'].append(
            (
                uncategorised_breakdown['total'] * -1,
                0,
                'Uncategorised'
            )
        )
        context['breakdown'] = sorted(context['breakdown'],
                                      key=itemgetter(0),
                                      reverse=True)

        return context
