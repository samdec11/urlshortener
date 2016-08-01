from django.contrib import admin

from .models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('base_url', 'short_url')
    search_fields = ['base_url']

admin.site.register(Link, LinkAdmin)
