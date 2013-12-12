from django.conf.urls.defaults import *
from models import Note

from django.views.generic.list_detail import object_list

from forms import NoteForm
from views import post_note, user_home

urlpatterns = patterns('',
    url(r'post_note/$', post_note, name='post_note'),
    url(r'profile/(?p<username>\w+)/$', user_home, name='user_home'),
    (r'$', object_list, dict(queryset=Note.objects.all().order_by('id').select_related(depth=1),
                             paginate_by20, extra_context=dict(form=NoteForm())), 'microblog_home'),
    )