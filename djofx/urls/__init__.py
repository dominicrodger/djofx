from django.conf.urls import include, url
from djofx import views

urlpatterns = [
    url(r'^$', views.home_page, name="djofx_home"),
    url(r'^upload/$', views.upload_ofx_file, name="djofx_upload"),
    url(r'^account/', include('djofx.urls.account')),
    url(r'^categories/', include('djofx.urls.categories')),
    url(r'^monthly/', include('djofx.urls.monthly')),
    url(r'^transaction/', include('djofx.urls.transaction')),
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
]
