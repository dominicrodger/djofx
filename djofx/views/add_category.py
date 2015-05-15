from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView

from djofx.forms import CategoryForm
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class AddCategoryView(PageTitleMixin, UserRequiredMixin, FormView):
    form_class = CategoryForm
    template_name = "djofx/add_category.html"
    page_title = "Add category"
    success_url = reverse_lazy('djofx_home')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.owner = self.request.user
        category.save()

        messages.success(
            self.request,
            'Payment category saved.'
        )

        return super(AddCategoryView, self).form_valid(form)
