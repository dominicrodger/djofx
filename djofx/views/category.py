from datetime import datetime
from django.db import connection
from django.db.models import Sum, Count
from django.views.generic import ListView

from djofx import models
from djofx.forms import CategoriseTransactionForm
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class CategoryTransactions(PageTitleMixin, UserRequiredMixin, ListView):
    model = models.Transaction
    paginate_by = 50

    def get_template_names(self):
        if not self.request.is_ajax():
            return ['djofx/category.html', ]
        else:
            return ['djofx/_transaction_list.html', ]

    def get_context_data(self, **kwargs):
        ctx = super(CategoryTransactions, self).get_context_data(**kwargs)
        ctx['category'] = self.get_category()
        ctx['categorise_form'] = CategoriseTransactionForm()

        qs = models.Transaction.objects.filter(
            transaction_category=self.get_category()
        )
        truncate_date = connection.ops.date_trunc_sql('month', 'date')
        qs = qs.extra({'month': truncate_date})
        report = qs.values('month').annotate(
            Sum('amount'),
            Count('pk')
        ).order_by('month')

        report = [
            (
                datetime.strptime(entry['month'], '%Y-%m-%d'),
                -1 * entry['amount__sum']
            )
            for entry in report
        ]
        ctx['month_breakdown'] = report

        return ctx

    def get_category(self):
        return models.TransactionCategory.objects.get(
            owner=self.request.user,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        qs = super(CategoryTransactions, self).get_queryset()
        qs = qs.filter(
            transaction_category=self.get_category()
        )

        return qs

    def get_page_title(self):
        object = self.get_category()
        return 'Category (%s)' % object.name
