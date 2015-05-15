from django.contrib import messages
from django.views.generic import RedirectView
from djofx import models
from djofx.utils import get_classifier


class AccountAutoCategoriseView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        account = models.Account.objects.get(
            owner=self.request.user,
            pk=self.kwargs['pk']
        )

        classifier = get_classifier(self.request.user)

        transactions = account.transaction_set.filter(category_verified=False)

        changes = 0

        for transaction in transactions:
            old_category = transaction.transaction_category
            transaction.transaction_category = transaction.guess_category(classifier)
            if old_category != transaction.transaction_category:
                changes += 1

            transaction.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            '%d transactions automatically categorised (%d changed).' % (len(transactions), changes)
        )

        return account.get_absolute_url()
