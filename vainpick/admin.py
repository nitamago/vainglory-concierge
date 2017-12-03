from django.contrib import admin

# Register your models here.
from .models import Hero, Match


class HerosAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

class MatchesAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'hero1', 'hero2', 'hero3', 'win')


admin.site.register(Hero, HerosAdmin)
admin.site.register(Match, MatchesAdmin)
