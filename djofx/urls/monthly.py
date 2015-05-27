from django.conf.urls import url
from djofx import views

urlpatterns = [
    url(r'^$', views.monthly_breakdown, name="djofx_monthly"),
    url(
        r'(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.monthly_spending_breakdown,
        name="djofx_monthly_breakdown"
    )
]
