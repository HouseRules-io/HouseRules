from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import Rule
from .models import Rulebook
from .models import House

# admin.site.register(House)


class HouseAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.qr_code.url))

    image_tag.short_description = 'Image'

    list_display = ['image_tag',]



admin.site.register(House, HouseAdmin)
admin.site.register(Rule)
admin.site.register(Rulebook)