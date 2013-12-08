from django.conf.urls import url, patterns
from madrona.simplefaq.views import faq

urlpatterns = patterns('',
    url(r'^$', faq, name="simplefaq"),
)
