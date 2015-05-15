from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.utils.http import urlquote


class UserRequiredMixin(object):
    redirect_field_name = REDIRECT_FIELD_NAME

    def authorization_check(self, user):
        return not user.is_anonymous()

    def handle_failure(self, request):
        path = urlquote(request.get_full_path())
        login_url = settings.LOGIN_URL
        tup = login_url, self.redirect_field_name, path
        return HttpResponseRedirect("%s?%s=%s" % tup)

    def dispatch(self, request, *args, **kwargs):
        if self.authorization_check(request.user):
            return super(UserRequiredMixin, self).dispatch(
                request,
                *args,
                **kwargs)

        return self.handle_failure(request)


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
