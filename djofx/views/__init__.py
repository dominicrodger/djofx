from djofx.views.account import AccountTransactions
from djofx.views.accuracy import AccuracyView
from djofx.views.auto_categorise import AccountAutoCategoriseView
from djofx.views.category import CategoryTransactions
from djofx.views.categorise import CategoriseTransactionView
from djofx.views.home import HomePageView
from djofx.views.upload import UploadOFXFileView
from djofx.views.xhr import TransactionMarkVerified, TransactionReguess


account_auto_categorise = AccountAutoCategoriseView.as_view()
account_detail = AccountTransactions.as_view()
accuracy = AccuracyView.as_view()
categorise = CategoriseTransactionView.as_view()
category_detail = CategoryTransactions.as_view()
home_page = HomePageView.as_view()
transaction_mark_verified = TransactionMarkVerified.as_view()
transaction_reguess = TransactionReguess.as_view()
upload_ofx_file = UploadOFXFileView.as_view()
