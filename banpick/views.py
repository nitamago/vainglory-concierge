#-*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from .models import Hero, Pick_Seq, Pick_Info, Seq_Cache
from django.db.models import Q

seq_set = [0, 2, 4, 7, 8, 11, 12]
hero_ids = []

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
             btn_grp = get_btn_grp(hero_dict)

             icon_list = []
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
             current = predict(heros)

        else:
             message = 'データ検証に失敗しました'
             pick_info = Pick_Info()
             hero_dict = get_pick_stat([])
             btn_grp = get_btn_grp(hero_dict)
             icon_list = []
             phase = "ban"
             current = predict([])
    else:
        pick_info = Pick_Info()
        hero_dict = get_pick_stat([])
        btn_grp = get_btn_grp(hero_dict)
        icon_list = None
        phase = "ban"
        current = predict([])
    return render(request, 'banpick/ui.html', {"hero_dict": hero_dict,
                "pick_info": pick_info,
                "icon_list": icon_list,
                "phase": phase,
                "current": current,
                "btn_grps": btn_grp})


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

    # ヒーローの勝率計算
    for hero_id, count in win_count_dict.items():
        pick_count = pick_count_dict[hero_id]
        hero_name = hero_id.replace("*", "")
        if total != 0 and count != 0:
            ret_dict[hero_name]["win_rate"] = "%03.1f" % (count/pick_count*100)
            ret_dict[hero_name]["lose_rate"] = "%03.1f" % ((1-count/pick_count)*100)
        else:
            ret_dict[hero_name]["win_rate"] = "?"
            ret_dict[hero_name]["lose_rate"] = "?"

    # ヒーローの予想勝率計算
    blue_ids = []
    red_ids = []
    for index in range(4, 14):
        if index >= len(heros):
            break
        if index in seq_set:
            blue_ids.append(heros[index])
        else:
            red_ids.append(heros[index])
    left_feature = {}
    for hero_id in blue_ids:
        obj = Hero.objects.get(Q(hero_id=hero_id))
        for f in obj.feature.split(":"):
            if f in left_feature:
                left_feature[f] += 1
            else:
                left_feature[f] = 1
    right_feature = {}
    for hero_id in red_ids:
        obj = Hero.objects.get(Q(hero_id=hero_id))
        for f in obj.feature.split(":"):
            if f in right_feature:
                right_feature[f] += 1
            else:
                right_feature[f] = 1

    # 係数の読み込み
    coef = None
    import os
    import pickle
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'static', 'banpick', 'coef', 'coef.dat')
    with open(file_path, "rb") as f:
        coef =  pickle.load(f)

    for hero_id in win_count_dict.keys():
        target = Hero.objects.get(Q(hero_id=hero_id))
        target_feature = {}
        feature_list = ["brink", "shield", "initiate", "heal", "reflect_block", "stealth", "cc", "poke", "adc", "apc"]
        for f in feature_list:
            if not f in left_feature:
                left_feature[f] = 0
            if not f in right_feature:
                right_feature[f] = 0
            if not f in target_feature:
                target_feature[f] = 0
        for f in target.feature.split(":"):
            if f in target_feature:
                target_feature[f] += 1
            else:
                target_feature[f] = 1
        if len(heros) in seq_set:
            predict_win_rate = coef["b0"]+\
            coef["left_brink"]*(left_feature["brink"]+target_feature["brink"])+\
            coef["right_brink"]*right_feature["brink"]+\
            coef["left_shield"]*(left_feature["shield"]+target_feature["shield"])+\
            coef["right_shield"]*right_feature["shield"]+\
            coef["left_initiate"]*(left_feature["initiate"]+target_feature["initiate"])+\
            coef["right_initiate"]*right_feature["initiate"]+\
            coef["left_heal"]*(left_feature["heal"]+target_feature["heal"])+\
            coef["right_heal"]*right_feature["heal"]+\
            coef["left_reflect_block"]*(left_feature["reflect_block"]+target_feature["reflect_block"])+\
            coef["right_reflect_block"]*right_feature["reflect_block"]+\
            coef["left_stealth"]*(left_feature["stealth"]+target_feature["stealth"])+\
            coef["right_stealth"]*right_feature["stealth"]+\
            coef["left_cc"]*(left_feature["cc"]+target_feature["cc"])+\
            coef["right_cc"]*right_feature["cc"]+\
            coef["left_poke"]*(left_feature["poke"]+target_feature["poke"])+\
            coef["right_poke"]*right_feature["poke"]
            coef["left_adc"]*(left_feature["adc"]+target_feature["adc"])+\
            coef["right_adc"]*right_feature["adc"]
            coef["left_apc"]*(left_feature["apc"]+target_feature["apc"])+\
            coef["right_apc"]*right_feature["apc"]
        else:
            predict_win_rate = coef["b0"]+\
            coef["right_brink"]*(right_feature["brink"]+target_feature["brink"])+\
            coef["left_brink"]*left_feature["brink"]+\
            coef["right_shield"]*(right_feature["shield"]+target_feature["shield"])+\
            coef["left_shield"]*left_feature["shield"]+\
            coef["right_initiate"]*(right_feature["initiate"]+target_feature["initiate"])+\
            coef["left_initiate"]*left_feature["initiate"]+\
            coef["right_heal"]*(right_feature["heal"]+target_feature["heal"])+\
            coef["left_heal"]*left_feature["heal"]+\
            coef["right_reflect_block"]*(right_feature["reflect_block"]+target_feature["reflect_block"])+\
            coef["left_reflect_block"]*left_feature["reflect_block"]+\
            coef["right_stealth"]*(right_feature["stealth"]+target_feature["stealth"])+\
            coef["left_stealth"]*left_feature["stealth"]+\
            coef["right_cc"]*(right_feature["cc"]+target_feature["cc"])+\
            coef["left_cc"]*left_feature["cc"]+\
            coef["right_poke"]*(right_feature["poke"]+target_feature["poke"])+\
            coef["left_poke"]*left_feature["poke"]+\
            coef["right_adc"]*(right_feature["adc"]+target_feature["adc"])+\
            coef["left_adc"]*left_feature["adc"]+\
            coef["right_apc"]*(right_feature["apc"]+target_feature["apc"])+\
            coef["left_apc"]*left_feature["apc"]

        hero_name = hero_id.replace("*", "")
        #ret_dict[hero_name]["predict_win_rate"] = "%03.1f" % (predict_win_rate*100)
        #ret_dict[hero_name]["predict_lose_rate"] = "%03.1f" % ((1-predict_win_rate)*100)
        ret_dict[hero_name]["win_rate"] = "%03.1f" % (predict_win_rate*100)
        ret_dict[hero_name]["lose_rate"] = "%03.1f" % ((1-predict_win_rate)*100)

        if hero_id in heros:
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

def predict(heros):
    # ヒーローの予想勝率計算
    if len(heros) <= 4:
        return {"win_rate": "?", "lose_rate": "?"}

    hero_ids = []
    for hero in heros:
        if hero == "saw":
            hero_ids.append("*SAW*")
        else:
            hero_ids.append("*"+hero[0].upper()+hero[1:]+"*")
    blue_ids = []
    red_ids = []
    for index in range(4, 14):
        if index >= len(heros):
            break
        if index in seq_set:
            blue_ids.append(hero_ids[index])
        else:
            red_ids.append(hero_ids[index])
    left_feature = {}
    for hero_id in blue_ids:
        obj = Hero.objects.get(Q(hero_id=hero_id))
        for f in obj.feature.split(":"):
            if f in left_feature:
                left_feature[f] += 1
            else:
                left_feature[f] = 1
    right_feature = {}
    for hero_id in red_ids:
        obj = Hero.objects.get(Q(hero_id=hero_id))
        for f in obj.feature.split(":"):
            if f in right_feature:
                right_feature[f] += 1
            else:
                right_feature[f] = 1

    feature_list = ["brink", "shield", "initiate", "heal", "reflect_block", "stealth", "cc", "poke", "adc", "apc"]
    for f in feature_list:
        if not f in left_feature:
            left_feature[f] = 0
        if not f in right_feature:
            right_feature[f] = 0

    # 係数の読み込み
    coef = None
    import os
    import pickle
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'static', 'banpick', 'coef', 'coef.dat')
    with open(file_path, "rb") as f:
        coef =  pickle.load(f)

    predict_win_rate = coef["b0"]+\
            coef["left_brink"]*left_feature["brink"]+\
            coef["right_brink"]*right_feature["brink"]+\
            coef["left_shield"]*left_feature["shield"]+\
            coef["right_shield"]*right_feature["shield"]+\
            coef["left_initiate"]*left_feature["initiate"]+\
            coef["right_initiate"]*right_feature["initiate"]+\
            coef["left_heal"]*left_feature["heal"]+\
            coef["right_heal"]*right_feature["heal"]+\
            coef["left_reflect_block"]*left_feature["reflect_block"]+\
            coef["right_reflect_block"]*right_feature["reflect_block"]+\
            coef["left_stealth"]*left_feature["stealth"]+\
            coef["right_stealth"]*right_feature["stealth"]+\
            coef["left_cc"]*left_feature["cc"]+\
            coef["right_cc"]*right_feature["cc"]+\
            coef["left_poke"]*left_feature["poke"]+\
            coef["right_poke"]*right_feature["poke"]+\
            coef["left_adc"]*left_feature["adc"]+\
            coef["right_adc"]*right_feature["adc"]+\
            coef["left_apc"]*left_feature["apc"]+\
            coef["right_apc"]*right_feature["apc"]

    ret_dict = {"win_rate": "?", "lose_rate": "?"}
    ret_dict["win_rate"] = "%03.1f" % (predict_win_rate*100)
    ret_dict["lose_rate"] = "%03.1f" % ((1-predict_win_rate)*100)

    return ret_dict


def get_btn_grp(hero_dict):
    btn_low = 6
    ret = []
    tmp_list = []
    for hero_id, hero_data in hero_dict.items():
        tmp = {}
        tmp["hero"] = hero_data
        tmp["hero"]["name"] = hero_id.lower()
        tmp["icon_path"] = "icons/" + hero_id.lower() + ".png"
        tmp_list.append(tmp)

        if len(tmp_list) == btn_low:
            ret.append(tmp_list)
            tmp_list = []
    ret.append(tmp_list)

    return ret
