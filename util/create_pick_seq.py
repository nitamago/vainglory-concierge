#! /usr/bin/python3
# -*- coding:utf-8 -*-

"""
pic sequenceレコードをDBへ登録する
"""

import os
import django
import json
import glob


def get_pick_seq(path):
    ret = []
    dec = None
    with open(path) as f:
        dec = json.load(f)

    try:
    	for event in dec["pick"]:
            action = event['type']
            if action == "HeroSelect":
                hero = event['payload']['Hero']
                ret.append(hero)
            elif action == "HeroBan":
                hero = event['payload']['Hero']
                ret.append(hero)
    except KeyError:
        return None

    if dec["winner"] == "left/blue":
        winner = 1
    else:
        winner = -1

    return (ret, winner)


def get_pick_dict():
    pick_dict = {}
    for path in glob.glob("data/pick/3.1/*.json"):
        if __debug__:
            print(path)
        seq, winner = get_pick_seq(path)
        if seq is not None:
            basename = os.path.basename(path)
            ID = os.path.splitext(basename)[0]
            pick_dict[ID] = (seq, winner)

    return pick_dict


def main():
    d = get_pick_dict()
    for ID, data in d.items():
        seq = data[0]
        if len(seq) < 14:
            continue
        if __debug__:
            print(seq)
        winner = data[1]
        if winner == 1:
            left_win = True
            right_win = False
        else:
            left_win = False
            right_win = True

        obj, created = Pick_Seq.objects.get_or_create(
                                    match_id=ID,
                                    pick1=seq[0],
                                    pick2=seq[1],
                                    pick3=seq[2],
                                    pick4=seq[3],
                                    pick5=seq[4],
                                    pick6=seq[5],
                                    pick7=seq[6],
                                    pick8=seq[7],
                                    pick9=seq[8],
                                    pick10=seq[9],
                                    pick11=seq[10],
                                    pick12=seq[11],
                                    pick13=seq[12],
                                    pick14=seq[13],
                                    left_win = left_win,
                                    right_win = right_win)
        if created:
            obj.save()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from banpick.models import Pick_Seq

    main()
