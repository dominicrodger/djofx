from django.views.generic import ListView

from djofx import models
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class CategoryListView(PageTitleMixin, UserRequiredMixin, ListView):
    model = models.TransactionCategory
    paginate_by = 50
    template_name = 'djofx/categories.html'
    page_title = 'Transaction Categories'

    def get_queryset(self):
        qs = super(CategoryListView, self).get_queryset()
        return qs.filter(owner=self.request.user)
category_list = CategoryListView.as_view()
