from djofx.views.account import AccountTransactionsView
from djofx.views.category import (
    CategoryTransactionsView,
    CategoryListView,
    AddCategoryView,
    UpdateCategoryView
)
from djofx.views.categorise import TransactionCategoriseView
from djofx.views.home import HomePageView
from djofx.views.monthly import MonthlyTransactionsView
from djofx.views.upload import UploadOFXFileView
from djofx.views.xhr import (
    TransactionMarkVerifiedView,
    TransactionListView,
    MonthlySpendingBreakdownView
)


account_detail = AccountTransactionsView.as_view()
category_add = AddCategoryView.as_view()
category_detail = CategoryTransactionsView.as_view()
category_edit = UpdateCategoryView.as_view()
category_list = CategoryListView.as_view()
home_page = HomePageView.as_view()
monthly_breakdown = MonthlyTransactionsView.as_view()
monthly_spending_breakdown = MonthlySpendingBreakdownView.as_view()
transaction_categorise = TransactionCategoriseView.as_view()
transaction_list = TransactionListView.as_view()
transaction_mark_verified = TransactionMarkVerifiedView.as_view()
upload_ofx_file = UploadOFXFileView.as_view()
