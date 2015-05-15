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
    return classifier.classify(text)
