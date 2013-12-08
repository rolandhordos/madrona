from django.conf.urls import patterns

urlpatterns = patterns('madrona.xyquery.views',
        (r'^$', 'query')
)
