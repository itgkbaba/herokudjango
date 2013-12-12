from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse

from views import send_activate_key, create_user, add_friend, remove_friend, upload_icon

top_page = reverse('index')

urlpatterns = patterns('',
    url(r'create/$', send_activate_key, name='send_activate_key'),
    url(r'create/(?P<activate_key>\w+)/$', create_user, name='create_user'),
    url(r'login/$', login, name="login"),
    url(r'logout/$', logout, dict(next_page=top_page), name="logout"),
    url(r'add_friend/(?P<username>\w+)/$', add_friend, name='add_friend'),
    url(r'remove_friend/(?P<username>\w+)/$', remove_friend, name='remove_friend'),
    url(r'upload_icon/$', upload_icon, name='upload_icon'),
    #(r'create/$', lambda:None, {}, (), 'send_activate_key'),
    #(r'create/(?P<activate_key>\w+)/$', lambda:None, {}, (), 'create_user'),
)
