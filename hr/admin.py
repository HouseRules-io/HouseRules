from django.contrib import admin

# Register your models here.

from .models import Rule
from .models import Rulebook
from .models import House

admin.site.register(House)
admin.site.register(Rule)
admin.site.register(Rulebook)