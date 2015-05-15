from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View
from django.template import RequestContext
from django.template.loader import render_to_string

from djofx import models


class XHRBaseView(View):
    def handle(self, request, *args, **kwargs):
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

        matching_transactions = models.Transaction.objects.filter(
            account__owner=self.request.user,
            payee=transaction.payee,
            category_verified=False
        ).update(
            transaction_category=transaction.transaction_category,
            category_verified=True
        )

        transaction = models.Transaction.objects.get(pk=transaction.pk)

        return HttpResponse(
            render_to_string(
                "djofx/_transaction_row.html",
                RequestContext(request, {
                    "transaction": transaction
                })
            )
        )


class TransactionReguess(XHRBasePostView):
    def render(self, request, *args, **kwargs):
        transaction = models.Transaction.objects.get(
            account__owner=self.request.user,
            pk=self.kwargs['pk']
        )

        classifier = None
        # classifier = request.session.get('classifier')

        # if classifier is None:
        #     classifier = get_classifier(request.user)
        #     request.session['classifier'] = classifier

        transaction.category_verified = False
        transaction.transaction_category = None
        transaction.transaction_category = transaction.guess_category(classifier)
        transaction.save()

        return HttpResponse(
            render_to_string(
                "djofx/_transaction_row.html",
                RequestContext(request, {
                    "transaction": transaction
                })
            )
        )
