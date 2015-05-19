from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import FormView

from djofx.forms import CategoriseTransactionForm
from djofx import models
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class CategoriseTransactionView(PageTitleMixin, UserRequiredMixin, FormView):
    form_class = CategoriseTransactionForm
    template_name = "djofx/categorise.html"
    page_title = "Categorise payment"

    def dispatch(self, request, *args, **kwargs):
        try:
            self.get_transaction()
        except IndexError:
            messages.info(
                self.request,
                'No transactions need categorising.'
            )
            return HttpResponseRedirect(reverse('djofx_home'))
        except models.Transaction.DoesNotExist:
            raise Http404("Transaction not found.")

        return super(CategoriseTransactionView, self).dispatch(
            request,
            *args,
            **kwargs
        )

    def get_transaction(self):
        if not hasattr(self, 'transaction_'):
            self.transaction_ = models.Transaction.objects.get(
                account__owner=self.request.user,
                pk=self.kwargs['pk']
            )
        return self.transaction_

    def get_context_data(self, **kwargs):
        ctx = super(CategoriseTransactionView, self).get_context_data(**kwargs)
        ctx['transaction'] = self.get_transaction()
        num_similar = self.get_similar_transactions().count()

        if not self.get_transaction().category_verified:
            num_similar -= 1

        ctx['related_transactions'] = num_similar

        return ctx

    def get_initial(self):
        transaction = self.get_transaction()

        next_url = None

        if 'keepreferrer' in self.request.GET:
            next_url = self.request.META['HTTP_REFERER']

        return {
            'next_url': next_url,
            'category': transaction.guess_category()
        }

    def get_similar_transactions(self):
        transaction = self.get_transaction()
        return models.Transaction.objects.filter(
            account__owner=self.request.user,
            payee=transaction.payee,
            category_verified=False
        )

    def form_valid(self, form):
        transaction = self.get_transaction()
        transaction.category_verified = False
        transaction.save()

        related_transactions = self.get_similar_transactions()
        related_transactions.update(
            transaction_category=form.cleaned_data['category'],
            category_verified=True
        )

        if self.request.is_ajax():
            return HttpResponse('OK')

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Payment categorisation saved.'
        )

        if form.cleaned_data['next_url']:
            self.success_url = form.cleaned_data['next_url']
        else:
            self.success_url = reverse('djofx_home')

        return super(CategoriseTransactionView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url
