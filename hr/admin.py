from django.contrib import admin

# Register your models here.

from .models import Rule, Rulebook, House, Profile

from django.utils.html import format_html


class HouseAdmin(admin.ModelAdmin):

	fields = ('house_name', 'creator', 'followers', 'hex_id', 'image_tag')
	readonly_fields = ['hex_id','image_tag']

admin.site.register(House, HouseAdmin)
admin.site.register(Rule)
admin.site.register(Rulebook)
admin.site.register(Profile)