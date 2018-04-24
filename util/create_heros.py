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
             {"name": '*Alpha*', 'feature': 'sustain:initiate'},
             {"name": '*Ardan*', 'feature': 'cc:initiate:shield'},
             {"name": '*Baptiste*', 'feature': 'cc:sustain'},
             {"name": '*Baron*', 'feature': 'brink:poke:adc'},
             {"name": '*Blackfeather*', 'feature': 'brink:initiate:shield'},
             {"name": '*Catherine*', 'feature': 'cc'},
             {"name": '*Celeste*', 'feature': 'cc:poke:apc'},
             {"name": '*Churnwalker*', 'feature': 'cc:sustain'},
             {"name": '*Flicker*', 'feature': 'cc:stealth'},
             {"name": '*Fortress*', 'feature': 'initiate'},
             {"name": '*Glaive*', 'feature': 'brink:cc:sustain'},
             {"name": '*Grace*', 'feature': 'cc:heal:initiate'},
             {"name": '*Grumpjaw*', 'feature': 'brink:cc'},
             {"name": '*Gwen*', 'feature': 'reflect_block:adc'},
             {"name": '*Idris*', 'feature': 'brink:poke'},
             {"name": '*Joule*', 'feature': 'brink'},
             {"name": '*Kestrel*', 'feature': 'stealth:poke:adc'},
             {"name": '*Koshka*', 'feature': 'cc:initiate'},
             {"name": '*Krul*', 'feature': 'cc:sustain'},
             {"name": '*Lance*', 'feature': 'cc'},
             {"name": '*Lorelai*', 'feature': 'cc:shield'},
             {"name": '*Lyra*', 'feature': 'heal:cc'},
             {"name": '*Melene*', 'feature': 'cc'},
             {"name": '*Ozo*', 'feature': 'sustain:initiate'},
             {"name": '*Petal*', 'feature': 'brink'},
             {"name": '*Phinn*', 'feature': 'cc:shield'},
             {"name": '*Reim*', 'feature': 'sustain:cc'},
             {"name": '*Reza*', 'feature': 'brink'},
             {"name": '*Ringo*', 'feature': 'adc'},
             {"name": '*Rona*', 'feature': 'shield:brink'},
             {"name": '*SAW*', 'feature': 'adc'},
             {"name": '*Samuel*', 'feature': 'cc:poke:apc'},
             {"name": '*Skaarf*', 'feature': 'poke:apc'},
             {"name": '*Skye*', 'feature': 'apc'},
             {"name": '*Taka*', 'feature': 'brink:stealth'},
             {"name": '*Tony*', 'feature': 'cc:shield'},
             {"name": '*Varya*', 'feature': 'brink:apc'},
             {"name": '*Vox*', 'feature': 'brink:adc'}]

    s = set()
    for hero in Heros:
        for f in hero["feature"].split(":"):
            s.add(f)
    print(s)


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
                                                       name=name,
                                                       image="no")
        if created:
            hero_obj.save()


