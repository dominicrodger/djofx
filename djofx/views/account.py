from django.views.generic import ListView

from djofx import models
from djofx.views.base import PageTitleMixin


class AccountTransactions(PageTitleMixin, ListView):
    model = models.Transaction
    template_name = 'djofx/account.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        ctx = super(AccountTransactions, self).get_context_data(**kwargs)
        ctx['account'] = self.get_account()
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
