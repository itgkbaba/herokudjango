from django.contrib import admin
from models import Note

class NoteOptions(admin.ModelAdmin):
    list_display = ('author', 'short_text',)

admin.site.register(Note, NoteOptions)