from django.views.generic import ListView

from djofx import models
from djofx.forms import CategoriseTransactionForm
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class AccountTransactions(PageTitleMixin, UserRequiredMixin, ListView):
    model = models.Transaction
    paginate_by = 50

    def get_template_names(self):
        if not self.request.is_ajax():
            return ['djofx/account.html', ]
        else:
            return ['djofx/_transaction_list.html', ]

    def get_context_data(self, **kwargs):
        ctx = super(AccountTransactions, self).get_context_data(**kwargs)
        ctx['account'] = self.get_account()
        ctx['categorise_form'] = CategoriseTransactionForm()

        return ctx

    def get_account(self):
        return models.Account.objects.get(
            owner=self.request.user,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        qs = super(AccountTransactions, self).get_queryset()
        qs = qs.filter(
            account=self.get_account()
        )

        if self.kwargs.get('unverified'):
            qs = qs.filter(
                category_verified=False
            )

        return qs

    def get_page_title(self):
        object = self.get_account()
        return 'Account (%s)' % object.name
account_detail = AccountTransactions.as_view()
