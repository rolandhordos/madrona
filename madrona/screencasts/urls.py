from django.conf.urls import url, patterns


urlpatterns = patterns('madrona.screencasts.views',   
    (r'^$', 'listTutorials'),  
    (r'^(\w+)/$', 'showVideo'),
    url(r'^(?P<pk>\d)/show/$', 'showVideoByPk', name='screencasts-show-video'),
    url(r'^(?P<pk>\d+)/show_youtube/$', 'showYoutubeVideo', name='screencasts-show-youtube-video'),
)
