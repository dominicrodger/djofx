import json
from django.views.generic import ListView

from djofx import models
from djofx.forms import CategoriseTransactionForm
from djofx.utils import qs_to_monthly_report
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
        category = self.get_category()
        ctx['category'] = category
        ctx['categorise_form'] = CategoriseTransactionForm()

        qs = models.Transaction.objects.filter(
            transaction_category=category
        )
        report = qs_to_monthly_report(qs, category.category_type)
        ctx['month_breakdown'] = json.dumps(report)

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
