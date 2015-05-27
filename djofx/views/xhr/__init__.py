import calendar
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from djofx import models
from djofx.utils import (
    get_spending_by_category,
    spending_by_category_to_flot
)
from djofx.views.xhr.base import XHRBaseGetView, XHRBasePostView


class TransactionMarkVerifiedView(XHRBasePostView):
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


class TransactionListView(XHRBaseGetView):
    def render(self, request, *args, **kwargs):
        month = int(kwargs['month'])
        year = int(kwargs['year'])
        category_type = dict(
            [(r[1], r[0])
             for r in models.TransactionCategory.TRANSACTION_TYPES]
        )[kwargs['type']]

        transactions = models.Transaction.objects.filter(
            transaction_category__owner=request.user,
            transaction_category__category_type=category_type,
            date__year=year,
            date__month=month
        ).order_by('amount')

        context = {}
        context['object_list'] = transactions
        context['page_obj'] = None

        return render_to_response(
            'djofx/_transaction_list.html',
            context,
            context_instance=RequestContext(request)
        )


class MonthlySpendingBreakdownView(XHRBaseGetView):
    def render(self, request, *args, **kwargs):
        month = int(kwargs['month'])
        year = int(kwargs['year'])
        _, last_of_month = calendar.monthrange(year, month)

        start = date(year, month, 1)
        end = date(year, month, last_of_month)

        breakdown = get_spending_by_category(start, end)
        flot = spending_by_category_to_flot(breakdown)

        return HttpResponse(flot)
