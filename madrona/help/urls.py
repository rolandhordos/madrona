from django.conf.urls import url, patterns

urlpatterns = patterns('madrona.help.views',
    url(r'^$', 'help', name="help-main"),
)
