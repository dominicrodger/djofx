class PageTitleMixin(object):
    def get_page_title(self):
        if hasattr(self, 'page_title'):
            return self.page_title

    def get_context_data(self, **kwargs):
        context = super(PageTitleMixin,
                        self).get_context_data(**kwargs)
        title = self.get_page_title()

        if title is not None:
            context['page_title'] = title

        return context
