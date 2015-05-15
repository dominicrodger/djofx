from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from djofx.utils import autocategorise_transaction


class Account(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('djofx_account', args=[self.pk, ])

    def get_unverified_url(self):
        return reverse('djofx_account_unverified', args=[self.pk, ])

    def get_auto_categorisation_url(self):
        return reverse('djofx_account_autocategorise', args=[self.pk, ])

    def earliest_transaction(self):
        try:
            return self.transaction_set.all().order_by('date')[0].date
        except IndexError:
            return None

    def latest_transaction(self):
        try:
            return self.transaction_set.all().order_by('-date')[0].date
        except IndexError:
            return None

    def unverified_transactions(self):
        return self.transaction_set.filter(category_verified=False)


class TransactionCategory(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    is_void = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('djofx_category', args=[self.pk, ])

    class Meta:
        ordering = ('name', )


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    transaction_key = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    payee = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255)
    transaction_category = models.ForeignKey(
        TransactionCategory,
        blank=True,
        null=True
    )
    category_verified = models.BooleanField(default=False)

    def guess_category(self, classifier=None):
        if self.transaction_category:
            return self.transaction_category

        if not hasattr(self, 'guess_category_'):
            self.guess_category_ = autocategorise_transaction(self, classifier)

        return self.guess_category_

    def absolute_amount(self):
        return self.amount.copy_abs()

    def get_categorisation_url(self):
        return reverse('djofx_categorise', args=[self.pk, ])

    class Meta:
        unique_together = ('account', 'transaction_key')
        ordering = ('date', )
