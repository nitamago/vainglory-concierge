from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from .models import Data, Hero, HeroSelectForm, Match, HeroPickStat, HeroSingleSelectForm
from django.db.models import Q

def index_page(request):
    if request.method == 'POST': # フォームが提出された
        select = HeroSelectForm(request.POST) # POST データの束縛フォーム
        if select.is_valid(): # バリデーションを通った
             message = 'データ検証に成功しました'
             hero1 = select.cleaned_data['hero1']
             hero2 = select.cleaned_data['hero2']
             hero3 = select.cleaned_data['hero3']
             heros = [hero1, hero2, hero3]
             min_sample = select.cleaned_data['min_sample']
             max_sample = select.cleaned_data['max_sample']
             min_win_rate = select.cleaned_data['min_win_rate']
             max_win_rate = select.cleaned_data['max_win_rate']
             pick_stat = get_pick_stat(heros)
             # 推薦情報取得
             recommend = get_recommends(heros,
                                        min_sample, max_sample,
                                        min_win_rate, max_win_rate)
        else:
             message = 'データ検証に失敗しました'
             message = None
             heros = None
             pick_stat = None
    else:
        select = HeroSelectForm() # 非束縛フォーム
        message = None
        heros = None
        pick_stat = None
        recommend = None
    return render(request, 'vainpick/index.html', {
                  'select': select,
                  'message': message,
                  'pick': pick_stat,
                  'recommend': recommend,
                  })


def get_pick_stat(heros):
    tmp_matches = Match.objects.all()

    # 選択したヒーローがでた試合を絞り込む
    tmp_left_matches = tmp_matches
    for hero in heros:
        if hero is not None:
            hero_id = hero.hero_id
            tmp_left_matches = tmp_left_matches.filter(Q(left_hero1 = hero_id) |
                                           Q(left_hero2 = hero_id) |
                                           Q(left_hero3 = hero_id))
    tmp_right_matches = tmp_matches
    for hero in heros:
        if hero is not None:
            hero_id = hero.hero_id
            tmp_right_matches = tmp_right_matches.filter(Q(right_hero1 = hero_id) |
                                           Q(right_hero2 = hero_id) |
                                           Q(right_hero3 = hero_id))
    win_count = 0
    sample_count = 0
    for m in tmp_left_matches:
        if m.left_win:
            win_count += 1
        sample_count += 1
    for m in tmp_right_matches:
        if m.right_win:
            win_count += 1
        sample_count += 1

    if sample_count == 0:
        win_rate = 0.0
    else:
        win_rate = win_count / sample_count

    hero1 = heros[0].hero_id if heros[0] is not None else "None"
    hero2 = heros[1].hero_id if heros[1] is not None else "None"
    hero3 = heros[2].hero_id if heros[2] is not None else "None"
    sorted_hero = sorted([hero1, hero2, hero3])
    for i, x in enumerate(sorted_hero):
        if x is "None":
            sorted_hero[i] = None
    obj, created = HeroPickStat.objects.get_or_create(sample_count=sample_count,
                                             hero1=sorted_hero[0],
                                             hero2=sorted_hero[1],
                                             hero3=sorted_hero[2],
                                             win_rate=win_rate,
                                             win_rate_str="{0:.1f}".format(win_rate*100))
    if created:
        obj.save()
    return obj


def get_recommends(heros, min_sample, max_sample, min_win_rate, max_win_rate):
    tmp_matches = Match.objects.all()
    tmp_left_matches = None
    tmp_right_matches = None

    # 選択したヒーローがでた試合を絞り込む
    tmp_left_matches = tmp_matches
    for hero in heros:
        if hero is not None:
            hero_id = hero.hero_id
            tmp_left_matches = tmp_left_matches.filter(Q(left_hero1 = hero_id) |
                                           Q(left_hero2 = hero_id) |
                                           Q(left_hero3 = hero_id))
    tmp_right_matches = tmp_matches
    for hero in heros:
        if hero is not None:
            hero_id = hero.hero_id
            tmp_right_matches = tmp_right_matches.filter(Q(right_hero1 = hero_id) |
                                           Q(right_hero2 = hero_id) |
                                           Q(right_hero3 = hero_id))

    # 選択したヒーローと一緒に使われているヒーローを調べる
    selected_hero = set()
    for hero in heros:
        if hero is not None:
            hero_id = hero.hero_id
            selected_hero.add(hero_id)

    rack_hero_dict = {}
    for match in tmp_left_matches:
        s = set([match.left_hero1, match.left_hero2, match.left_hero3])
        rack_hero_set = s - selected_hero
        if len(s) != 3:
            continue
        if tuple(rack_hero_set) in rack_hero_dict.keys():
            rack_hero_dict[tuple(rack_hero_set)].append("left")
        else:
            rack_hero_dict[tuple(rack_hero_set)] = ["left"]

    for match in tmp_right_matches:
        s = set([match.right_hero1, match.right_hero2, match.right_hero3])
        rack_hero_set = s - selected_hero
        if len(s) != 3:
            continue
        if tuple(rack_hero_set) in rack_hero_dict.keys():
            rack_hero_dict[tuple(rack_hero_set)].append("right")
        else:
            rack_hero_dict[tuple(rack_hero_set)] = ["right"]

    # 3ヒーロー選ばれていたらNoneを返す
    if len(list(rack_hero_dict)[0]) == 0:
        return None

    # 選ばれていないヒーローが１体のとき
    if len(list(rack_hero_dict)[0]) == 1:
        hero1 = heros[0].hero_id if heros[0] is not None else None
        hero2 = heros[1].hero_id if heros[1] is not None else None

        for rack_hero, sides in rack_hero_dict.items():
            _hero = list(rack_hero)[0]
            if _hero is None:
                continue
            win_count = 0
            sample_count = 0
            if "left" in sides:
                _tmp_matches = tmp_left_matches.filter(Q(left_hero1 = _hero) |
                                           Q(left_hero2 = _hero) |
                                           Q(left_hero3 = _hero))
                for m in _tmp_matches:
                    if m.left_win:
                        win_count += 1
                sample_count += len(_tmp_matches)

            if "right" in sides:
                _tmp_matches = tmp_right_matches.filter(Q(right_hero1 = _hero) |
                                           Q(right_hero2 = _hero) |
                                           Q(right_hero3 = _hero))
                for m in _tmp_matches:
                    if m.right_win:
                        win_count += 1
                sample_count += len(_tmp_matches)

            if sample_count == 0:
                win_rate = 0.0
            else:
                win_rate = win_count / sample_count

            sorted_hero = sorted([hero1, hero2, _hero])
            obj, created = HeroPickStat.objects.get_or_create(
                                                     sample_count=sample_count,
                                                     hero1=sorted_hero[0],
                                                     hero2=sorted_hero[1],
                                                     hero3=sorted_hero[2],
                                                     win_rate=win_rate,
                                                     win_rate_str="{0:.1f}".format(win_rate*100))
            if created:
                obj.save()

        obj = HeroPickStat.objects.filter(Q(hero1=hero1) | Q(hero2=hero1) | Q(hero3=hero1))\
                          .filter(Q(hero1=hero2) | Q(hero2=hero2) | Q(hero3=hero2))\
                          .exclude(hero3=None)\
                          .filter(Q(sample_count__gte = min_sample) & Q(sample_count__lte = max_sample))\
                          .filter(Q(win_rate__gte = min_win_rate) & Q(win_rate__lte = max_win_rate))\
                          .order_by('win_rate').reverse()

    # 選ばれていないヒーローが2体のとき
    elif len(list(rack_hero_dict)[0]) == 2:
        hero1 = heros[0].hero_id if heros[0] is not None else None
        for rack_heros, sides in rack_hero_dict.items():
            _hero, _hero2 = tuple(rack_heros)

            if _hero is None:
                continue
            elif _hero2 is None:
                continue

            win_count = 0
            sample_count = 0
            if "left" in sides:
                _tmp_matches = tmp_left_matches.filter(Q(left_hero1 = _hero) |
                                                       Q(left_hero2 = _hero) |
                                                       Q(left_hero3 = _hero))\
                                               .filter(Q(left_hero1 = _hero2) |
                                                       Q(left_hero2 = _hero2) |
                                                       Q(left_hero3 = _hero2))
                for m in _tmp_matches:
                    if m.left_win:
                        win_count += 1
                sample_count += len(_tmp_matches)

            if "right" in sides:
                _tmp_matches = tmp_right_matches.filter(Q(right_hero1 = _hero) |
                                                        Q(right_hero2 = _hero) |
                                                        Q(right_hero3 = _hero))\
                                                .filter(Q(right_hero1 = _hero2) |
                                                        Q(right_hero2 = _hero2) |
                                                        Q(right_hero3 = _hero2))
                for m in _tmp_matches:
                    if m.right_win:
                        win_count += 1
                sample_count += len(_tmp_matches)

            if sample_count == 0:
                win_rate = 0.0
            else:
                win_rate = win_count / sample_count

            sorted_hero = sorted([hero1, _hero, _hero2])
            obj, created = HeroPickStat.objects.get_or_create(sample_count=sample_count,
                                                     hero1=sorted_hero[0],
                                                     hero2=sorted_hero[1],
                                                     hero3=sorted_hero[2],
                                                     win_rate=win_rate,
                                                     win_rate_str="{0:.1f}".format(win_rate*100))
            if created:
                obj.save()

        obj = HeroPickStat.objects.filter(Q(hero1=hero1) | Q(hero2=hero1) | Q(hero3=hero1))\
                          .exclude(hero2=None)\
                          .exclude(hero3=None)\
                          .filter(Q(sample_count__gte = min_sample) & Q(sample_count__lte = max_sample))\
                          .filter(Q(win_rate__gte = min_win_rate) & Q(win_rate__lte = max_win_rate))\
                          .order_by('win_rate').reverse()
    else:
        obj = None
    return obj

def which_side(heros, m):
    hero_set = set()
    for hero in heros:
        if hero is not None:
            hero_set.add(hero.hero_id)
    if hero_set <= set([m.left_hero1, m.left_hero2, m.left_hero3]):
        return "left"
    elif hero_set <= set([m.right_hero1, m.right_hero2, m.right_hero3]):
        return "right"
    else:
        return "no"

def compati_page(request):
    if request.method == 'POST': # フォームが提出された
        select = HeroSingleSelectForm(request.POST) # POST データの束縛フォーム
        if select.is_valid(): # バリデーションを通った
             message = 'データ検証に成功しました'
             hero = select.cleaned_data['hero']
             compatis = get_compatis(hero)
        else:
             message = 'データ検証に失敗しました'
             message = None
             heros = None
    else:
        select = HeroSingleSelectForm() # 非束縛フォーム
        message = None
        heros = None
        compatis = None
    return render(request, 'vainpick/compati.html', {
                  'select': select,
                  'message': message,
                  'compati': compatis,
                  })

def get_compatis(hero):
    tmp_matches = Match.objects.all()
    hero_id = hero.hero_id
    tmp_left_matches = tmp_matches.filter(Q(left_hero1 = hero_id) |
                                   Q(left_hero2 = hero_id) |
                                   Q(left_hero3 = hero_id))
    tmp_right_matches = tmp_matches.filter(Q(right_hero1 = hero_id) |
                                   Q(right_hero2 = hero_id) |
                                   Q(right_hero3 = hero_id))

    win_rate_dict = {}
    heros = Hero.objects.all()
    for h in heros:
        win_rate_dict[h.hero_id] = [0.0, 0]

    for m in tmp_left_matches:
        # 敵サイドのヒーローを収集
        enemy_heros = []
        enemy_heros.append(m.right_hero1)
        enemy_heros.append(m.right_hero2)
        enemy_heros.append(m.right_hero3)

        # 各敵サイドヒーローに対して勝率を計算
        for eh in enemy_heros:
            _data = win_rate_dict[eh]
            _data[0] += 1 if m.left_win else 0
            _data[1] += 1

    for m in tmp_right_matches:
        # 敵サイドのヒーローを収集
        enemy_heros = []
        enemy_heros.append(m.left_hero1)
        enemy_heros.append(m.left_hero2)
        enemy_heros.append(m.left_hero3)

        # 各敵サイドヒーローに対して勝率を計算
        for eh in enemy_heros:
            _data = win_rate_dict[eh]
            _data[0] += 1 if m.right_win else 0
            _data[1] += 1

    ret_list = []
    for _id, data in win_rate_dict.items():
        d = {}
        if data[1] == 0:
            d["id"] = _id
            d["sample_count"] = 0
            d["win_rate"] = 0.0
            d["win_rate_str"] = "0.0"
        else:
            d["id"] = _id
            d["sample_count"] = data[1]
            win_rate = data[0] / data[1]
            d["win_rate"] = win_rate
            d["win_rate_str"] = "{0:.1f}".format(win_rate*100)
        ret_list.append(d)

    ret_list = sorted(ret_list, key=lambda x:x["win_rate"], reverse=True)

    return {"hero_id": hero_id, "win_rate_list": ret_list}
