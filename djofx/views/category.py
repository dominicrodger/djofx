import json
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView

from djofx import models
from djofx.forms import CategoriseTransactionForm, CategoryForm

from djofx.utils import qs_to_monthly_report
from djofx.views.base import PageTitleMixin, UserRequiredMixin


class CategoryTransactionsView(PageTitleMixin, UserRequiredMixin, ListView):
    model = models.Transaction
    paginate_by = 50

    def get_template_names(self):
        if not self.request.is_ajax():
            return ['djofx/category.html', ]
        else:
            return ['djofx/_transaction_list.html', ]

    def get_context_data(self, **kwargs):
        ctx = super(CategoryTransactionsView, self).get_context_data(**kwargs)
        category = self.get_category()
        ctx['category'] = category
        ctx['categorise_form'] = CategoriseTransactionForm()

        qs = models.Transaction.objects.filter(
            transaction_category=category
        )
        report = qs_to_monthly_report(qs, category.category_type)
        ctx['month_breakdown'] = json.dumps(report)

        return ctx

    def get_category(self):
        return models.TransactionCategory.objects.get(
            owner=self.request.user,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        qs = super(CategoryTransactionsView, self).get_queryset()
        qs = qs.filter(
            transaction_category=self.get_category()
        )

        return qs

    def get_page_title(self):
        object = self.get_category()
        return 'Category (%s)' % object.name


class CategoryListView(PageTitleMixin, UserRequiredMixin, ListView):
    model = models.TransactionCategory
    paginate_by = 50
    template_name = 'djofx/categories.html'
    page_title = 'Transaction Categories'

    def get_queryset(self):
        qs = super(CategoryListView, self).get_queryset()
        return qs.filter(owner=self.request.user)


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
