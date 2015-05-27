from django.conf.urls import url
from djofx import views

urlpatterns = [
    url(r'^$', views.monthly_breakdown, name="djofx_monthly"),
]
