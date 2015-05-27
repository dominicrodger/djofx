from datetime import date, timedelta
from django.views.generic import TemplateView

from djofx.forms import OFXForm
from djofx.utils import (
    get_spending_by_category,
    spending_by_category_to_flot
)
from djofx.views.base import PageTitleMixin, UserRequiredMixin
from djofx import models


class HomePageView(PageTitleMixin, UserRequiredMixin, TemplateView):
    template_name = "djofx/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['accounts'] = models.Account.objects.filter(
            owner=self.request.user
        )

        context['form'] = OFXForm()

        breakdown = get_spending_by_category(
            date.today() - timedelta(days=120),
            date.today()
        )

        context['chart_data'] = spending_by_category_to_flot(
            breakdown
        )
        context['breakdown'] = breakdown

        return context
