from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


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
    OUTGOINGS = 'out'
    INCOME = 'inc'
    INTERNAL_TRANSFER = 'int'

    TRANSACTION_TYPES = (
        (OUTGOINGS, 'Outgoings'),
        (INCOME, 'Income'),
        (INTERNAL_TRANSFER, 'Internal Transfer'),
    )

    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    category_type = models.CharField(
        max_length=3,
        choices=TRANSACTION_TYPES,
        default=OUTGOINGS
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('djofx_category', args=[self.pk, ])

    class Meta:
        verbose_name_plural = 'Transaction categories'
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

    def absolute_amount(self):
        return self.amount.copy_abs()

    def get_categorisation_url(self):
        return reverse('djofx_categorise', args=[self.pk, ])

    class Meta:
        unique_together = ('account', 'transaction_key')
        ordering = ('date', )
