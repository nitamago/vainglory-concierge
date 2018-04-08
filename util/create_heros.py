#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
heroレコードをDBへ登録する
"""

import os
import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from vainpick.models import Hero

    Heros = [{"name": '*Adagio*', 'feature': 'cc:heal'},
             {"name": '*Alpha*', 'feature': 'sustain'},
             {"name": '*Ardan*', 'feature': 'cc'},
             {"name": '*Baptiste*', 'feature': 'cc:sustain'},
             {"name": '*Baron*', 'feature': 'brink'},
             {"name": '*Blackfeather*', 'feature': 'brink'},
             {"name": '*Catherine*', 'feature': 'cc'},
             {"name": '*Celeste*', 'feature': 'cc'},
             {"name": '*Churnwalker*', 'feature': 'cc:sustain'},
             {"name": '*Flicker*', 'feature': 'cc:stealth'},
             {"name": '*Fortress*', 'feature': 'brink'},
             {"name": '*Glaive*', 'feature': 'cc:sustain'},
             {"name": '*Grace*', 'feature': 'cc:heal'},
             {"name": '*Grumpjaw*', 'feature': 'brink'},
             {"name": '*Gwen*', 'feature': ''},
             {"name": '*Idris*', 'feature': 'brink'},
             {"name": '*Joule*', 'feature': 'brink'},
             {"name": '*Kestrel*', 'feature': 'stealth'},
             {"name": '*Koshka*', 'feature': 'brink'},
             {"name": '*Krul*', 'feature': 'sustain'},
             {"name": '*Lance*', 'feature': 'cc'},
             {"name": '*Lorelai*', 'feature': 'cc'},
             {"name": '*Lyra*', 'feature': 'cc'},
             {"name": '*Ozo*', 'feature': 'sustain'},
             {"name": '*Petal*', 'feature': 'brink'},
             {"name": '*Phinn*', 'feature': ''},
             {"name": '*Reim*', 'feature': 'sustain'},
             {"name": '*Reza*', 'feature': 'brink'},
             {"name": '*Ringo*', 'feature': ''},
             {"name": '*Rona*', 'feature': 'sustain:brink'},
             {"name": '*SAW*', 'feature': ''},
             {"name": '*Samuel*', 'feature': 'cc'},
             {"name": '*Skaarf*', 'feature': ''},
             {"name": '*Skye*', 'feature': ''},
             {"name": '*Taka*', 'feature': 'brink:stealth'},
             {"name": '*Tony*', 'feature': 'cc'},
             {"name": '*Varya*', 'feature': 'brink'},
             {"name": '*Vox*', 'feature': 'brink'}]


    for hero in Heros:
        hero_id = hero["name"]
        name = hero["name"].replace("*", "")
        feature = hero["feature"]
        hero_obj, created = Hero.objects.get_or_create(hero_id=hero_id,
                                                       feature=feature,
                                                       name=name, image="no")
        if created:
            hero_obj.save()


    from banpick.models import Hero

    for hero in Heros:
        hero_id = hero["name"]
        name = hero["name"].replace("*", "")
        feature = hero["feature"]
        hero_obj, created = Hero.objects.get_or_create(hero_id=hero_id,
                                                       feature=feature,
                                                       name=name, image="no")
        if created:
            hero_obj.save()


