import json
from datetime import datetime
from django.db import connection
from django.db.models import Sum, Count
from django.views.generic import TemplateView

from djofx import models
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class MonthlyTransactionsView(PageTitleMixin, UserRequiredMixin, TemplateView):
    template_name = 'djofx/monthly.html'
    page_title = 'Monthly Breakdown'

    def qs_to_report(self, qs, type):
        truncate_date = connection.ops.date_trunc_sql('month', 'date')
        qs = qs.extra({'month': truncate_date})
        report = qs.values('month').annotate(
            Sum('amount'),
            Count('pk')
        ).order_by('month')

        def adjust_value(value, type):
            if type == models.TransactionCategory.OUTGOINGS:
                return value * -1
            return value

        report = [
            (
                datetime.strptime(entry['month'], '%Y-%m-%d'),
                adjust_value(float(entry['amount__sum']), type)
            )
            for entry in report
        ]
        report = [((thedate.year, thedate.month), value)
                  for thedate, value in report]

        return json.dumps(report)

    def get_report_by_type(self, type):
        qs = models.Transaction.objects.filter(
            account__owner=self.request.user,
            transaction_category__category_type=type
        )

        return self.qs_to_report(qs, type)

    def get_context_data(self, **kwargs):
        ctx = super(MonthlyTransactionsView, self).get_context_data(**kwargs)

        ctx['outgoings'] = self.get_report_by_type(
            models.TransactionCategory.OUTGOINGS
        )
        ctx['income'] = self.get_report_by_type(
            models.TransactionCategory.INCOME
        )

        return ctx
