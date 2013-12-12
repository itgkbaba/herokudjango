from django.db import models
from django.contrib.auth import models as auth_models

class Note(models.Model):
    author = models.ForeignKey(auth_models.User)
    text = models.TextField("Note's Text")
    writed_at = models.DateTimeField('Write at', auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Note'
        get_latest_by = 'Writed_at'

    def __unicode__(self):
        return self.short_text()

    def short_text(self):
        return self.text[:30]
