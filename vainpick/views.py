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
    return render(request, 'vainpick/index.html', {
                  'select': select,
                  'message': message,
                  'pick': pick_stat,
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
    obj, created = HeroPickStat.objects.get_or_create(sample_count=len(tmp_matches),
                                             hero1=hero1,
                                             hero2=hero2,
                                             hero3=hero3,
                                             win_rate=win_rate,
                                             win_rate_str="{0:.1f}".format(win_rate*100))
    if created:
        obj.save()
    return obj
