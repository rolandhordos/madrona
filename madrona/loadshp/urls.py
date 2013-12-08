from django.conf.urls import url, patterns

urlpatterns = patterns('madrona.loadshp.views',
    url(r'^single/$', 'load_single_shp', name='loadshp-single'),
)
