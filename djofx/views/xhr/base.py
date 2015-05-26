from django.http import HttpResponseForbidden
from django.views.generic import View


class XHRBaseView(View):
    def handle(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseForbidden(
                "This page requires a login."
            )

        if not request.is_ajax():
            return HttpResponseForbidden(
                "This page is not directly accessible."
            )

        return self.render(request, *args, **kwargs)


class XHRBasePostView(XHRBaseView):
    def post(self, request, *args, **kwargs):
        return self.handle(request, *args, **kwargs)


class XHRBaseGetView(XHRBaseView):
    def get(self, request, *args, **kwargs):
        return self.handle(request, *args, **kwargs)
