from snsuser.models import SnsUser
from microblog.models import Note
from forms import NoteForm
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

def user_home(request, username):
    user = get_object_or_404(SnsUser, username=username, is_active=True)
    friends = [u.id for u in user.friends.all()] + [user.id]
    logined = False
    catch_uped = False
    if request.user.is_authenticated() :
        logined = True
        you = request.user
        your_friends = you.snsuser.friends.all()
        if user.id in [f.id for f in your_friends]:
            catch_uped = True
    query_set = Note.objects.filter(author__in=friends).order_by('-id')
    return object_list(request, queryset=query_set, paginate_by=20, allow_empty=True,template_name='microblog/user_home.html',
                       extra_context=dict(friends=user.friends.all(), user_profile=user, logined=logined, catch_uped=catch_uped))

@login_required
def post_note(request):
    if request.method == 'POST':
        note = Note(author_id=request.user.id)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('microblog_home'))
    return render_to_response('microblog/note_list.html', context_instance=RequestContext(request, {'form': form}))
