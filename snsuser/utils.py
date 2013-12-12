from django.utils.translation import ugettext as _
from django.core.mail import EmailMessage
from django.template import loader, Context

from django.conf import settings
from django.contrib.sites.models import Site

def send_confirm_mail(email, confirm_url):
    site = Site.objects.get(pk=settings.SITE_ID)
    t = loader.get_template('snsuser/confirm.mail')
    c = Context({'domain': site.name, 'confirm_url': confirm_url })
    mail = EmailMessage('Invite from %s' % site.name, t.render(c), to = (email,) )
    mail.send()

def set_snsuser_message(request, message):
    if hasattr(request, 'session'):
        try:
            request.session['snsuser_messages'].append(message)
        except KeyError:
            request.session['snsuser_messages'] = [message]
        return True
    return False

def get_and_delete_sns_message(request):
    if hasattr(request, 'session'):
        return request.session.pop('snsuser_messages', [])
    return []

class IconCreator(object):
    
    def __init__(self, img):
        self.img = img
    
    def resize(self, resize_to):
        w, h = self.img.size
        tmp_img = self.img.resize(self._calc_thumb_size(w, h, resize_to))
        return tmp_img.crop(self._crop_rect(tmp_img.size[0], tmp_img.size[1]))
    
    def _calc_thumb_size(self, width, height, resize_to) :
        if width > height:
            scale = float(resize_to)/height
        else:
            scale = float(resize_to)/width
        return int(width * scale), int(height * scale)

    def _crop_rect(self, width, height) :
        if width > height :
            w = int( (width - height) / 2)
            h = 0
            max = height
        else :
            w = 0
            h = int( (height - width) / 2)
            max = width
        return (0 + w, 0 + h, max + w, max + h)

