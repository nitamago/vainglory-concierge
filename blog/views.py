#-*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from django.db.models import Q

def top_page(request,seq=""):
    return render(request, 'blog/top.html', {})

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
