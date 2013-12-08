from django.conf.urls import url, patterns
from django.core.urlresolvers import reverse

urlpatterns = patterns('madrona.bookmarks.views',
    url(r'^(?P<bookmark_id>\d+)/$', 'show_bookmark', name="bookmark"),
    url(r'^statejson/(?P<bookmark_id>\d+)$', 'bookmark_state_json', name="bookmark-state-json"),
    url(r'^tool/$', 'save_tool_bookmark', name="bookmark-tool"),
)
