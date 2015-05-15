from django.contrib import admin
from djofx import models


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', )
    search_fields = ('name', )
admin.site.register(models.Account, AccountAdmin)


class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_void')
    search_fields = ('name', )
    fields = ('name', 'is_void', )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
admin.site.register(models.TransactionCategory, TransactionCategoryAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'date',
        'payee',
        'transaction_type',
        'amount',
        'transaction_key',
        'transaction_category',
    )
    search_fields = ('payee', )
    date_hierarchy = 'date'
    list_filter = ('account', 'category_verified', )
admin.site.register(models.Transaction, TransactionAdmin)
