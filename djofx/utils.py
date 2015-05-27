import json
from datetime import datetime
from django.db import connection
from django.db.models import Sum, Count
from operator import itemgetter

from djofx import models


def get_training_data(owner):
    from djofx import models

    categorised = models.Transaction.objects.filter(
        account__owner=owner,
        category_verified=True
    )

    data = [(t.payee, t.transaction_category) for t in categorised]

    # Avoiding .distinct, because SQLite doesn't support it
    category_mapping = dict()

    for payee, category in data:
        category_mapping[payee] = category

    return category_mapping


def qs_to_monthly_report(qs, type):
    from djofx import models
    truncate_date = connection.ops.date_trunc_sql('month', 'date')
    qs = qs.extra({'month': truncate_date})
    report = qs.values('month').annotate(
        Sum('amount'),
        Count('pk')
    ).order_by('month')

    def adjust_value(value, type):
        if type == models.TransactionCategory.OUTGOINGS:
            return value * -1
        return value

    report = [
        (
            datetime.strptime(entry['month'], '%Y-%m-%d'),
            adjust_value(float(entry['amount__sum']), type)
        )
        for entry in report
    ]
    report = [((thedate.year, thedate.month), value)
              for thedate, value in report]

    return report


def get_spending_by_category(early_date_limit, late_date_limit):
    uncategorised_breakdown = models.Transaction.objects.filter(
        amount__lt=0,
        transaction_category__isnull=True,
        date__gte=early_date_limit,
        date__lte=late_date_limit
    ).aggregate(
        total=Sum('amount')
    )

    out = models.TransactionCategory.OUTGOINGS

    breakdown = models.Transaction.objects.filter(
        amount__lt=0,
        transaction_category__category_type=out,
        date__gte=early_date_limit,
        date__lte=late_date_limit
    ).values(
        'transaction_category__pk',
        'transaction_category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('transaction_category')

    breakdown = [
        (
            abs(item['total']),
            item['transaction_category__pk'],
            item['transaction_category__name']
        )
        for item in breakdown
    ]
    breakdown.append(
        (
            uncategorised_breakdown['total'] * -1,
            0,
            'Uncategorised'
        )
    )

    breakdown = sorted(
        breakdown,
        key=itemgetter(0),
        reverse=True
    )

    return breakdown


def spending_by_category_to_flot(breakdown):
    return json.dumps([
        {
            'label': item[2],
            'data': float(item[0])
        }
        for item in breakdown
    ])
