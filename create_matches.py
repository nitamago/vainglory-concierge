#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
matchレコードをDBへ登録する
"""

import os
import django
import json
import glob


def get_pick(path):
    ret = {}
    dec = None
    with open(path) as f:
        dec = json.load(f)
    teams = {'1': [], '2': []}
    for event in dec["pick"]:
        action = event['type']
        if action == "HeroSelect":
            team = event['payload']['Team']
            hero = event['payload']['Hero']
            teams[team].append(hero)
    ret["teams"] = teams

    if dec["winner"] == "left/blue":
        ret["winner"] = 1
    else:
        ret["winner"] = -1

    return ret


def pick_list():
    pick_dict = {}
    for path in glob.glob("data/pick/*.json"):
        dic = get_pick(path)
        if dic is not None:
            basename = os.path.basename(path)
            ID = os.path.splitext(basename)[0]
            pick_dict[ID] = dic

    ret_list = []
    for ID, d in pick_dict.items():
        dic = {}
        dic["id"] = ID
        team1 = tuple(sorted(d["teams"]['1']))
        dic["pick"] = team1
        dic["win"] = True if d["winner"] == 1 else False
        ret_list.append(dic)

        dic = {}
        dic["id"] = ID
        team2 = tuple(sorted(d["teams"]['2']))
        dic["pick"] = team2
        dic["win"] = True if d["winner"] == -1 else False
        ret_list.append(dic)

    return ret_list


def main():
    l = pick_list()
    for data in l:
        print(data)
        ID = data["id"]
        heros = data["pick"]
        hero1 = heros[0]
        hero2 = heros[1]
        hero3 = heros[2]
        win = data["win"]
        obj = Match.objects.create(match_id=ID, hero1=hero1,
                           hero2=hero2, hero3=hero3,
                           win=win)
        obj.save()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from vainpick.models import Match

    main()
