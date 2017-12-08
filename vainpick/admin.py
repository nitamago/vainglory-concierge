from django.contrib import admin

# Register your models here.
from .models import Hero, Match, HeroPickStat


class HerosAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

class MatchesAdmin(admin.ModelAdmin):
    list_display = ('match_id',
                    'left_hero1', 'left_hero2', 'left_hero3', 'left_win',
                    'right_hero1', 'right_hero2', 'right_hero3', 'right_win')

class PicksAdmin(admin.ModelAdmin):
    list_display = ('sample_count', 'hero1', 'hero2', 'hero3', 'win_rate')


admin.site.register(Hero, HerosAdmin)
admin.site.register(Match, MatchesAdmin)
admin.site.register(HeroPickStat, PicksAdmin)
