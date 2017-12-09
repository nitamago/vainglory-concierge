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
    for path in glob.glob("data/pick/2.11/*.json"):
        dic = get_pick(path)
        if dic is not None:
            basename = os.path.basename(path)
            ID = os.path.splitext(basename)[0]
            pick_dict[ID] = dic

    ret_list = []
    for ID, d in pick_dict.items():
        _dict = {}
        dic = {}
        dic["id"] = ID
        team1 = tuple(sorted(d["teams"]['1']))
        dic["pick"] = team1
        dic["win"] = True if d["winner"] == 1 else False
        _dict["team1"] = dic

        dic = {}
        dic["id"] = ID
        team2 = tuple(sorted(d["teams"]['2']))
        dic["pick"] = team2
        dic["win"] = True if d["winner"] == -1 else False
        _dict["team2"] = dic

        ret_list.append(_dict)

    return ret_list


def main():
    l = pick_list()
    for data in l:
        ID = data['team1']["id"]
        heros = data['team1']["pick"]
        left_hero1 = heros[0]
        left_hero2 = heros[1]
        left_hero3 = heros[2]
        left_win = data['team1']["win"]

        heros = data['team2']["pick"]
        right_hero1 = heros[0]
        right_hero2 = heros[1]
        right_hero3 = heros[2]
        right_win = data['team2']["win"]

        obj = Match.objects.create(match_id=ID,
                                    left_hero1=left_hero1,
                                    left_hero2=left_hero2,
                                    left_hero3=left_hero3,
                                    left_win=left_win,
                                    right_hero1=right_hero1,
                                    right_hero2=right_hero2,
                                    right_hero3=right_hero3,
                                    right_win=right_win)
        obj.save()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from vainpick.models import Match

    main()
