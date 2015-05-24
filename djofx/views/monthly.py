import json
from datetime import date, timedelta
from django.views.generic import TemplateView

from djofx import models
from djofx.utils import qs_to_monthly_report
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class MonthlyTransactionsView(PageTitleMixin, UserRequiredMixin, TemplateView):
    template_name = 'djofx/monthly.html'
    page_title = 'Monthly Breakdown'

    def get_report_by_type(self, type):
        cutoff = date.today() - timedelta(days=180)
        cutoff = cutoff.replace(day=1)

        qs = models.Transaction.objects.filter(
            account__owner=self.request.user,
            transaction_category__category_type=type,
            date__gte=cutoff
        )

        return json.dumps(qs_to_monthly_report(qs, type))

    def get_context_data(self, **kwargs):
        ctx = super(MonthlyTransactionsView, self).get_context_data(**kwargs)

        ctx['outgoings'] = self.get_report_by_type(
            models.TransactionCategory.OUTGOINGS
        )
        ctx['income'] = self.get_report_by_type(
            models.TransactionCategory.INCOME
        )

        return ctx
