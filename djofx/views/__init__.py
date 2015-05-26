from djofx.views.account import AccountTransactions
from djofx.views.add_category import AddCategoryView
from djofx.views.category import CategoryTransactions
from djofx.views.categories import CategoryListView
from djofx.views.categorise import TransactionCategoriseView
from djofx.views.edit_category import UpdateCategoryView
from djofx.views.home import HomePageView
from djofx.views.monthly import MonthlyTransactionsView
from djofx.views.upload import UploadOFXFileView
from djofx.views.xhr import TransactionMarkVerified


account_detail = AccountTransactions.as_view()
add_category = AddCategoryView.as_view()
transaction_categorise = TransactionCategoriseView.as_view()
category_list = CategoryListView.as_view()
category_detail = CategoryTransactions.as_view()
edit_category = UpdateCategoryView.as_view()
home_page = HomePageView.as_view()
monthly_breakdown = MonthlyTransactionsView.as_view()
transaction_mark_verified = TransactionMarkVerified.as_view()
upload_ofx_file = UploadOFXFileView.as_view()
