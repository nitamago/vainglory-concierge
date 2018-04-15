#-*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from .models import Hero, Pick_Seq, Pick_Info, Seq_Cache
from django.db.models import Q

def index_page(request,seq=""):
    if request.method == 'POST': # フォームが提出された
        pick_info = Pick_Info(request.POST) # POST データの束縛フォーム
        if pick_info.is_valid(): # バリデーションを通った
             message = 'データ検証に成功しました'
             pick_str = pick_info.cleaned_data["pick_str"]
             pick_info.pick_str = pick_str

             heros = pick_str.split(":")

             hero_ids = []
             for hero in heros:
                 if hero == "saw":
                     hero_ids.append("*SAW*")
                 else:
                     hero_ids.append("*"+hero[0].upper()+hero[1:]+"*")

             hero_dict = get_pick_stat(hero_ids)

             icon_list = []
             seq_set = [0, 2, 4, 7, 8, 11, 12]
             for (i, name) in enumerate(heros):
                 if name == "saw":
                     hero_id = "*SAW*"
                 else:
                     hero_id = "*"+name[0].upper()+name[1:]+"*"
                 hero_obj = Hero.objects.all().filter(Q(hero_id = hero_id))
                 paths = []
                 for f in hero_obj[0].feature.split(":"):
                     if f == "":
                         break
                     paths.append("icons/" + f + ".png")
                 icon_list.append({"path": "icons/" + name + ".png",
                                   "team": "blue" if i in seq_set else "red",
                                   "feature": paths})
             phase = "ban" if len(heros) < 4 else "pick"

        else:
             message = 'データ検証に失敗しました'
             pick_info = Pick_Info()
             hero_dict = get_pick_stat([])
             icon_list = []
             phase = "ban"
    else:
        pick_info = Pick_Info()
        hero_dict = get_pick_stat([])
        icon_list = None
        phase = "ban"
    return render(request, 'banpick/ui.html', {"hero_dict": hero_dict,
                "pick_info": pick_info,
                "icon_list": icon_list,
                "phase": phase})


def get_pick_stat(heros):
    ret_dict = {}
    all_hero = Hero.objects.all()
    for hero in all_hero:
        hero_name = hero.name
        ret_dict[hero_name] = {"pick_rate": "?", "win_rate": "?", "count": "?"}

    # ヒーローのfeature iconを設定
    for hero in all_hero:
        hero_name = hero.name
        features = hero.feature.split(":")
        icon_paths = []
        for f in features:
            if f == "":
                icon_paths = None
                break
            icon_paths.append("icons/"+f+".png")
        ret_dict[hero_name]["feature"] = icon_paths

    # キャッシュの確認
    cache = Seq_Cache.objects.all()
    key_str = ":".join(heros)
    cache = cache.filter(Q(key_str = key_str))

    if len(cache) != 0:
        for record in cache:
            ret_dict[record.target]["pick_rate"] = record.pick_rate
            ret_dict[record.target]["win_rate"] = record.win_rate
            ret_dict[record.target]["lose_rate"] = record.lose_rate
        return ret_dict


    # 選択したヒーローがでた試合を絞り込む
    tmp_pick_seq = Pick_Seq.objects.all()
    if len(heros) > 0 and len(heros) < 5:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick1 = heros[0])|
            Q(pick2 = heros[0])|
            Q(pick3 = heros[0])|
            Q(pick4 = heros[0]))
    if len(heros) > 1 and len(heros) < 5:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick1 = heros[1])|
            Q(pick2 = heros[1])|
            Q(pick3 = heros[1])|
            Q(pick4 = heros[1]))
    if len(heros) > 2 and len(heros) < 5:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick1 = heros[2])|
            Q(pick2 = heros[2])|
            Q(pick3 = heros[2])|
            Q(pick4 = heros[2]))
    if len(heros) > 3:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick1 = heros[3])|
            Q(pick2 = heros[3])|
            Q(pick3 = heros[3])|
            Q(pick4 = heros[3]))
    if len(heros) > 4:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick5 = heros[4]))
    if len(heros) > 5:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick6 = heros[5]))
    if len(heros) > 6:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick7 = heros[6]))
    if len(heros) > 7:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick8 = heros[7]))
    if len(heros) > 8:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick9 = heros[8]))
    if len(heros) > 9:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick10 = heros[9]))
    if len(heros) > 10:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick11 = heros[10]))
    if len(heros) > 11:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick12 = heros[11]))
    if len(heros) > 12:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick13 = heros[12]))
    if len(heros) > 13:
        tmp_pick_seq = tmp_pick_seq.filter(
            Q(pick14 = heros[13]))

    # ピック数を数える
    all_hero = Hero.objects.all()
    pick_count_dict = {}
    win_count_dict = {}
    for hero in all_hero:
        pick_count_dict[hero.hero_id] = 0
        win_count_dict[hero.hero_id] = 0

    for seq in tmp_pick_seq:
        if len(heros) == 0:
            pick_count_dict[seq.pick1] += 1
            if seq.left_win:
                win_count_dict[seq.pick1] += 1
        if len(heros) == 1:
            pick_count_dict[seq.pick2] += 1
            if seq.left_win:
                win_count_dict[seq.pick2] += 1
        if len(heros) == 2:
            pick_count_dict[seq.pick3] += 1
            if seq.left_win:
                win_count_dict[seq.pick3] += 1
        if len(heros) == 3:
            pick_count_dict[seq.pick4] += 1
            if seq.left_win:
                win_count_dict[seq.pick4] += 1
        if len(heros) == 4:
            pick_count_dict[seq.pick5] += 1
            if seq.left_win:
                win_count_dict[seq.pick5] += 1
        if len(heros) == 5:
            pick_count_dict[seq.pick6] += 1
            if seq.left_win:
                win_count_dict[seq.pick6] += 1
        if len(heros) == 6:
            pick_count_dict[seq.pick7] += 1
            if seq.left_win:
                win_count_dict[seq.pick7] += 1
        if len(heros) == 7:
            pick_count_dict[seq.pick8] += 1
            if seq.left_win:
                win_count_dict[seq.pick8] += 1
        if len(heros) == 8:
            pick_count_dict[seq.pick9] += 1
            if seq.left_win:
                win_count_dict[seq.pick9] += 1
        if len(heros) == 9:
            pick_count_dict[seq.pick10] += 1
            if seq.left_win:
                win_count_dict[seq.pick10] += 1
        if len(heros) == 10:
            pick_count_dict[seq.pick11] += 1
            if seq.left_win:
                win_count_dict[seq.pick11] += 1
        if len(heros) == 11:
            pick_count_dict[seq.pick12] += 1
            if seq.left_win:
                win_count_dict[seq.pick12] += 1
        if len(heros) == 12:
            pick_count_dict[seq.pick13] += 1
            if seq.left_win:
                win_count_dict[seq.pick13] += 1
        if len(heros) == 13:
            pick_count_dict[seq.pick14] += 1
            if seq.left_win:
                win_count_dict[seq.pick14] += 1


    # ヒーローのピック率計算
    total = len(tmp_pick_seq)
    for hero_id, count in pick_count_dict.items():
        hero_name = hero_id.replace("*", "")
        ret_dict[hero_name]["count"] = count
        if total != 0 and count != 0:
            ret_dict[hero_name]["pick_rate"] = "%03.1f" % (count/total*100)
        else:
            ret_dict[hero_name]["pick_rate"] = "?"

    for hero_id, count in win_count_dict.items():
        pick_count = pick_count_dict[hero_id]
        hero_name = hero_id.replace("*", "")
        if total != 0 and count != 0:
            ret_dict[hero_name]["win_rate"] = "%03.1f" % (count/pick_count*100)
            ret_dict[hero_name]["lose_rate"] = "%03.1f" % ((1-count/pick_count)*100)
        else:
            ret_dict[hero_name]["win_rate"] = "?"
            ret_dict[hero_name]["lose_rate"] = "?"

    # キャッシュ作成
    key_str = ":".join(heros)
    for hero_name, data in ret_dict.items():
        obj, created = Seq_Cache.objects.get_or_create(
            target = hero_name,
            key_str = key_str,
            index = len(heros),
            pick_rate = data["pick_rate"],
            win_rate = data["win_rate"],
            lose_rate = data["lose_rate"])
        if created:
            obj.save()

    return ret_dict


