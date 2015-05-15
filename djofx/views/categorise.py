from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import FormView

from djofx.forms import CategoriseTransactionForm
from djofx import models
from djofx.views.base import PageTitleMixin


class CategoriseTransactionView(PageTitleMixin, FormView):
    form_class = CategoriseTransactionForm
    template_name = "djofx/categorise.html"
    page_title = "Categorise payment"

    def get_transaction(self):
        if not hasattr(self, 'transaction_'):
            if 'pk' in self.kwargs:
                self.transaction_ = models.Transaction.objects.get(
                    account__owner=self.request.user,
                    pk=self.kwargs['pk']
                )
            else:
                self.transaction_ = models.Transaction.objects.filter(
                    account__owner=self.request.user,
                    category_verified=False
                ).order_by('?')[0]
        return self.transaction_

    def get_context_data(self, **kwargs):
        ctx = super(CategoriseTransactionView, self).get_context_data(**kwargs)
        ctx['transaction'] = self.get_transaction()
        return ctx

    def get_initial(self):
        transaction = self.get_transaction()

        next_url = None

        if 'keepreferrer' in self.request.GET:
            next_url = self.request.META['HTTP_REFERER']

        return {
            'next_url': next_url,
            'transaction_id': transaction.pk,
            'category': transaction.guess_category()
        }

    def form_valid(self, form):
        transaction = models.Transaction.objects.get(
            pk=form.cleaned_data['transaction_id'],
            account__owner=self.request.user
        )
        transaction.category_verified = False
        transaction.save()

        matching_transactions = models.Transaction.objects.filter(
            account__owner=self.request.user,
            payee=transaction.payee,
            category_verified=False
        ).update(
            transaction_category=form.cleaned_data['category'],
            category_verified=True
        )

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Payment categorisation saved.'
        )

        if form.cleaned_data['next_url']:
            self.success_url = form.cleaned_data['next_url']
        else:
            self.success_url = reverse('djofx_categorise')

        return super(CategoriseTransactionView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url
