from django.conf.urls import url, patterns
from django.core.urlresolvers import reverse

urlpatterns = patterns('madrona.staticmap.views',
    url(r'^(?P<map_name>\w+)/$', 'show',name="staticmap-show"),
    url(r'^(?P<map_name>\w+)/$', 'staticmap_link',name="staticmap-link"),
    (r'^$', 'show')
)
