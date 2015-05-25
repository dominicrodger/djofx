from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView

from djofx.forms import CategoryForm
from djofx import models
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class UpdateCategoryView(PageTitleMixin, UserRequiredMixin, UpdateView):
    model = models.TransactionCategory
    form_class = CategoryForm
    template_name = "djofx/edit_category.html"
    page_title = "Edit category"
    success_url = reverse_lazy('djofx_categories')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Payment category saved.'
        )

        return super(UpdateCategoryView, self).form_valid(form)
