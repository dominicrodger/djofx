from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.views.generic import FormView
from ofxparse import OfxParser

from djofx.forms import OFXForm
from djofx import models
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class UploadOFXFileView(PageTitleMixin, UserRequiredMixin, FormView):
    form_class = OFXForm
    template_name = "djofx/upload.html"
    success_url = reverse_lazy("djofx_home")
    page_title = 'Upload OFX File'

    def form_valid(self, form):
        ofx = OfxParser.parse(form.files['file'])

        valid_transactions = 0
        skipped_transactions = 0

        for ofx_account in ofx.accounts:
            account, _ = models.Account.objects.get_or_create(
                owner=self.request.user,
                name=ofx_account.account_id
            )
            transactions = ofx_account.statement.transactions
            for transaction in transactions:
                try:
                    models.Transaction.objects.create(
                        account=account,
                        transaction_key=transaction.id,
                        amount=transaction.amount,
                        date=transaction.date.date(),
                        payee=transaction.payee,
                        transaction_type=transaction.type,
                        transaction_category=None
                    )
                    valid_transactions += 1
                except IntegrityError:
                    # We've seen this transaction before
                    skipped_transactions += 1

        status = messages.SUCCESS

        if skipped_transactions != 0:
            status = messages.WARNING

        messages.add_message(
            self.request,
            status,
            (
                'Uploaded %d transactions successfully, skipped %d '
                'already seen transactions.'
                % (valid_transactions, skipped_transactions)
            )
        )

        return super(UploadOFXFileView, self).form_valid(form)
