from datetime import datetime
from django.db import connection
from django.db.models import Sum, Count
from django.views.generic import TemplateView

from djofx import models
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class MonthlyTransactionsView(PageTitleMixin, UserRequiredMixin, TemplateView):
    template_name = 'djofx/monthly.html'
    page_title = 'Monthly Breakdown'

    def qs_to_report(self, qs):
        truncate_date = connection.ops.date_trunc_sql('month', 'date')
        qs = qs.extra({'month': truncate_date})
        report = qs.values('month').annotate(
            Sum('amount'),
            Count('pk')
        ).order_by('month')

        report = [
            (
                datetime.strptime(entry['month'], '%Y-%m-%d'),
                entry['amount__sum']
            )
            for entry in report
        ]

        return report

    def get_outgoings(self):
        qs = models.Transaction.objects.filter(
            account__owner=self.request.user,
            amount__gte=0,
            transaction_category__is_void=False
        )

        return self.qs_to_report(qs)

    def get_context_data(self, **kwargs):
        ctx = super(MonthlyTransactionsView, self).get_context_data(**kwargs)

        ctx['month_breakdown'] = self.get_outgoings()

        return ctx
