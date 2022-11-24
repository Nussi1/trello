from django.contrib import admin
from .models import Entry, Column, Window, Comment


admin.site.register(Window)
admin.site.register(Entry)
admin.site.register(Column)
admin.site.register(Comment)