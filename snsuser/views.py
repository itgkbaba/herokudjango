import os
from StringIO import StringIO
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from forms import SendKeyForm, CreateUserForm, UploadIconForm
from models import ActivateKey, SnsUser
from utils import send_confirm_mail, set_snsuser_message, IconCreator


def send_activate_key(request):
    if request.method == 'POST':
        form = SendKeyForm(request.POST)
        if form.is_valid():
            key = ActivateKey.objects.next()
            key.belongs_to_email = form.cleaned_data.get('email')
            key.save()
            confirm_url = reverse('create_user', kwargs=dict(activate_key=key.activate_key))
            send_confirm_mail(key.belongs_to_email, confirm_url)
            set_snsuser_message(request,
                _(u'Sent invitation message to %(address)s') % {'address': form.cleaned_data['email']})
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SendKeyForm()
    return render_to_response('snsuser/sendkey_form.html', context_instance=RequestContext(request, {'form': form}))

def create_user(request, activate_key):
    try:
        key = ActivateKey.objects.get(activate_key=activate_key, activated=False)
    except ActivateKey.DoesNotExist:
        raise Http404()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.set_password(form.cleaned_data.get('password'))
            u.save()
            key.activated = True
            key.save()
            set_snsuser_message(request,
                _(u"Create Your account. You can logged in now."))
            return HttpResponseRedirect(reverse('index'))
    else:
        form = CreateUserForm(initial={'email': key.belongs_to_email})
    return render_to_response('snsuser/snsuser_form.html', context_instance=RequestContext(request, {'form': form}))

def add_friend(request, username):
    if request.method == 'POST':
        target_user = get_object_or_404(SnsUser, username=username, is_active=True)
        request.user.snsuser.friends.add(target_user)
        set_snsuser_message(request,
            _(u"Add %s to Your friends.") % target_user.nickname)
        return HttpResponseRedirect(reverse('user_home', kwargs=dict(username=target_user.username)))
    raise Http404()

def remove_friend(request, username):
    if request.method == 'POST':
        target_user = get_object_or_404(SnsUser, username=username, is_active=True)
        request.user.snsuser.friends.remove(target_user)
        set_snsuser_message(request,
            _(u"Remove %s from Your friends.") % target_user.nickname)
        return HttpResponseRedirect(reverse('user_home', kwargs=dict(username=target_user.username)))
    raise Http404()

@login_required
def upload_icon(request):
    from PIL import Image
    if request.method == 'POST':
        form = UploadIconForm(request.POST, request.FILES)
        if form.is_valid():
            icon_file = form.cleaned_data['icon']
            icon = Image.open(StringIO(icon_file.read()))
            iconCreator = IconCreator(icon)
            small_icon = iconCreator.resize(64)
            normal_icon = iconCreator.resize(128)
            path = 'icon/%s.png' % request.user.username
            icon_path = '%s/%s' % (settings.MEDIA_ROOT, path)
            normal_icon.save(icon_path, 'png')  
            request.user.snsuser.icon = path
            request.user.snsuser.save()
    return HttpResponseRedirect(reverse('user_home', kwargs=dict(username=request.user.username)))
