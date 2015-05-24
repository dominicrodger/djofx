from datetime import datetime
from django.db import connection
from django.db.models import Sum, Count
from textblob.classifiers import NaiveBayesClassifier


def get_training_data(owner):
    from djofx import models

    categorised = models.Transaction.objects.filter(
        account__owner=owner,
        category_verified=True
    )

    data = [(t.payee, t.transaction_category) for t in categorised]

    # Avoiding .distinct, because SQLite doesn't support it
    seen_payees = set()
    unique_data = []
    for payee, category in data:
        if payee in seen_payees:
            continue

        seen_payees.add(payee)
        unique_data.append((payee, category))

    return unique_data


def get_classifier(owner, training_data=None):
    if not training_data:
        training_data = get_training_data(owner)

    return NaiveBayesClassifier(training_data)


def autocategorise_transaction(transaction, classifier=None):
    training_data = get_training_data(transaction.account.owner)

    for payee, category in training_data:
        if payee == transaction.payee:
            return category

    if not classifier:
        classifier = get_classifier(transaction.account.owner, training_data)

    return classifier.classify(transaction.payee)


def classify_text(text, classifier):
    try:
        return classifier.classify(text)
    except ValueError:
        return None


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
