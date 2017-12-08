from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from .models import Data, Hero, HeroSelectForm, Match, HeroPickStat
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

    for hero in heros:
        if hero is None:
            hero_id = '%'
        else:
            hero_id = hero.hero_id
            tmp_matches = tmp_matches.filter(Q(hero1 = hero_id) |
                                           Q(hero2 = hero_id) |
                                           Q(hero3 = hero_id))

    win_count = 0
    for win in tmp_matches:
        if win.win:
            win_count += 1
    if len(tmp_matches) == 0:
        win_rate = 0.0
    else:
        win_rate = win_count / len(tmp_matches)

    hero1 = heros[0].hero_id if heros[0] is not None else "None"
    hero2 = heros[1].hero_id if heros[1] is not None else "None"
    hero3 = heros[2].hero_id if heros[2] is not None else "None"
    sorted_hero = sorted([hero1, hero2, hero3])
    for i, x in enumerate(sorted_hero):
        if x is "None":
            sorted_hero[i] = None
    print(sorted_hero)
    obj, created = HeroPickStat.objects.get_or_create(sample_count=len(tmp_matches),
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

    None_num = 0
    selected_hero = set()
    for hero in heros:
        if hero is None:
            None_num += 1
        else:
            hero_id = hero.hero_id
            selected_hero.add(hero_id)
            tmp_matches = tmp_matches.filter(Q(hero1 = hero_id) |
                                           Q(hero2 = hero_id) |
                                           Q(hero3 = hero_id))
    rack_hero_list = []
    for match in tmp_matches:
        s = set([match.hero1, match.hero2, match.hero3])
        rack_hero_set = s - selected_hero
        if len(s) != 3:
            continue
        rack_hero_list.append(rack_hero_set)

    if len(rack_hero_list) == 0:
        return None

    if len(rack_hero_list[0]) == 1:
        hero1 = heros[0].hero_id if heros[0] is not None else None
        hero2 = heros[1].hero_id if heros[1] is not None else None

        for rack_hero in rack_hero_list:
            _hero = list(rack_hero)[0]
            if _hero is None:
                continue
            _tmp_matches = tmp_matches.filter(Q(hero1 = _hero) |
                                           Q(hero2 = _hero) |
                                           Q(hero3 = _hero))
            win_count = 0
            for win in _tmp_matches:
                if win.win:
                    win_count += 1
            if len(_tmp_matches) == 0:
                win_rate = 0.0
            else:
                win_rate = win_count / len(_tmp_matches)

            sorted_hero = sorted([hero1, hero2, _hero])
            obj, created = HeroPickStat.objects.get_or_create(
                                                     sample_count=len(_tmp_matches),
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

    elif len(rack_hero_list[0]) == 2:
        hero1 = heros[0].hero_id if heros[0] is not None else None

        for rack_heros in rack_hero_list:
            _hero, _hero2 = tuple(rack_heros)
            if _hero is None:
                continue
            elif _hero2 is None:
                continue
            _tmp_matches = tmp_matches.filter(Q(hero1 = _hero) |
                                              Q(hero2 = _hero) |
                                              Q(hero3 = _hero))

            _tmp_matches = _tmp_matches.filter(Q(hero1 = _hero2) |
                                               Q(hero2 = _hero2) |
                                               Q(hero3 = _hero2))
            win_count = 0
            for win in _tmp_matches:
                if win.win:
                    win_count += 1
            if len(_tmp_matches) == 0:
                win_rate = 0.0
            else:
                win_rate = win_count / len(_tmp_matches)

            sorted_hero = sorted([hero1, _hero, _hero2])
            obj, created = HeroPickStat.objects.get_or_create(sample_count=len(_tmp_matches),
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
