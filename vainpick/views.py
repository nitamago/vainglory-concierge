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
             pick_stat = get_pick_stat(heros)
             recommend = get_recommends(heros)
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

    hero1 = heros[0].hero_id if heros[0] is not None else None
    hero2 = heros[1].hero_id if heros[1] is not None else None
    hero3 = heros[2].hero_id if heros[2] is not None else None
    sorted_hero = sorted([hero1, hero2, hero3])
    obj, created = HeroPickStat.objects.get_or_create(sample_count=len(tmp_matches),
                                             hero1=sorted_hero[0],
                                             hero2=sorted_hero[1],
                                             hero3=sorted_hero[2],
                                             win_rate=win_rate,
                                             win_rate_str="{0:.1f}".format(win_rate*100))
    if created:
        obj.save()
    return obj


def get_recommends(heros):
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

            hero1 = heros[0].hero_id if heros[0] is not None else None
            hero2 = heros[1].hero_id if heros[1] is not None else None
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
        obj = HeroPickStat.objects.filter(hero1=hero1, hero2=hero2)\
                          .exclude(hero3=None)\
                          .order_by('win_rate').reverse()[:5]

    elif len(rack_hero_list[0]) == 2:
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

            hero1 = heros[0].hero_id if heros[0] is not None else None
            sorted_hero = sorted([hero1, _hero, _hero2])
            obj, created = HeroPickStat.objects.get_or_create(sample_count=len(_tmp_matches),
                                                     hero1=sorted_hero[0],
                                                     hero2=sorted_hero[1],
                                                     hero3=sorted_hero[2],
                                                     win_rate=win_rate,
                                                     win_rate_str="{0:.1f}".format(win_rate*100))
            if created:
                obj.save()

        obj = HeroPickStat.objects.filter(hero1=hero1)\
                          .exclude(hero2=None, hero3=None)\
                          .order_by('win_rate').reverse()[:5]
    else:
        obj = None
    return obj
