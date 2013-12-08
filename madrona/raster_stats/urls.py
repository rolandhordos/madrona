from django.conf.urls import url, patterns

urlpatterns = patterns('madrona.raster_stats.views',
    url(r'^$', 'raster_list', name="raster_list"),
    url(r'^(?P<raster_name>\w+)/$', 'stats_for_geom', name="raster_stats"),
)
