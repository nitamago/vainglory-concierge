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

    Heros = ['*Vox*', '*Taka*', '*Idris*', '*Gwen*',
             '*Celeste*', '*Grumpjaw*', '*Ringo*',
             '*Phinn*', '*Baron*', '*Fortress*',
             '*Joule*', '*Lyra*', '*Blackfeather*',
             '*Ardan*', '*Skaarf*', '*Glaive*', '*Lance*',
             '*Rona*', '*Churnwalker*', '*Samuel*',
             '*Kestrel*', '*Baptiste*', '*Reza*', '*Petal*',
             '*Koshka*', '*Adagio*', '*SAW*', '*Catherine*',
             '*Skye*', '*Alpha*', '*Reim*', '*Grace*', '*Flicker*',
             '*Ozo*', '*Krul*', '*Lorelai*', '*Varya*', '*Tony*']

    for hero_id in sorted(Heros):
        name = hero_id.replace("*", "")
        hero_obj, created = Hero.objects.get_or_create(hero_id=hero_id,
                                                       name=name, image="no")
        if created:
            hero_obj.save()