from django.contrib import admin

# Register your models here.
from .models import Pick_Seq, Hero, Seq_Cache

class PickSeqAdmin(admin.ModelAdmin):
    list_display = ('match_id',
                    'pick1',
                    'pick2',
                    'pick3',
                    'pick4',
                    'pick5',
                    'pick6',
                    'pick7',
                    'pick8',
                    'pick9',
                    'pick10',
                    'pick11',
                    'pick12',
                    'pick13',
                    'pick14',
                    'left_win',
                    'right_win')

class HerosAdmin(admin.ModelAdmin):
    list_display = ('name', 'feature', 'image')

class Seq_Cache_Admin(admin.ModelAdmin):
    list_display = ('key_str', 'pick_rate', 'win_rate')

admin.site.register(Pick_Seq, PickSeqAdmin)
admin.site.register(Hero, HerosAdmin)
admin.site.register(Seq_Cache, Seq_Cache_Admin)
