from datetime import datetime
from django.db import connection
from django.db.models import Sum, Count


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
