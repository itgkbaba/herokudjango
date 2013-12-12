from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext_lazy as _

from random import choice

class SnsUser(auth_models.User):
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
    nickname = models.CharField(_('NickName'), max_length=10)
    icon = models.ImageField('', upload_to='icons', blank=True, null=True)

class NetProfile(models.Model):
    snsUser = models.ForeignKey(SnsUser)
    name = models.CharField(_('Name'), max_length=50)
    url = models.URLField(_('Original(Link)'), blank=True, verify_exists=False)

class ActivateKeyManager(models.Manager):
    """"""
    def next(self):
        try:
            key = ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(20)])
            ActivateKey.objects.get(activate_key__exact=key)
            return self.next()
        except ActivateKey.DoesNotExist:
            act = ActivateKey(activate_key=key, activated=False)
            return act

class ActivateKey(models.Model):
    activate_key = models.CharField(_('Activation Key'), max_length=50, unique=True)
    belongs_to_email = models.EmailField(_('Email'))
    activated = models.BooleanField(_('Activate Flag'), default=False)
    
    objects = ActivateKeyManager()    

