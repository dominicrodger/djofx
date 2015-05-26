from django.http import HttpResponse

from djofx import models
from djofx.views.xhr.base import XHRBasePostView


class TransactionMarkVerified(XHRBasePostView):
    def render(self, request, *args, **kwargs):
        transaction = models.Transaction.objects.get(
            account__owner=self.request.user,
            pk=self.kwargs['pk']
        )

        models.Transaction.objects.filter(
            account__owner=self.request.user,
            payee=transaction.payee,
            category_verified=False
        ).update(
            transaction_category=transaction.transaction_category,
            category_verified=True
        )

        return HttpResponse('OK')
