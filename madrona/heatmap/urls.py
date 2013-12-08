from django.conf.urls import url, patterns
from madrona.heatmap.views import *

urlpatterns = patterns('',
    url(r'^collection/geotiff/(?P<collection_uids>(\w+,?)+)/$', overlap_geotiff_response, name='heatmap-collection-geotiff'),
    url(r'^collection/kmz/(?P<collection_uids>(\w+,?)+)/$', overlap_kmz_response, name='heatmap-collection-kmz'),
)
