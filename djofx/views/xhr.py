from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View

from djofx import models


class XHRBaseView(View):
    def handle(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseForbidden(
                "This page requires a login."
            )

        if not request.is_ajax():
            return HttpResponseForbidden(
                "This page is not directly accessible."
            )

        return self.render(request, *args, **kwargs)


class XHRBasePostView(XHRBaseView):
    def post(self, request, *args, **kwargs):
        return self.handle(request, *args, **kwargs)


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
