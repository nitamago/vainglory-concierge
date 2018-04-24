# coding: UTF-8
import numpy as np
import os
import django
from django.db.models import Q
import pickle

def stat(obj, exp):
    n = exp.shape[1]

    exp = np.vstack([np.ones(n), exp]) # 定数項、説明変数

    coef = np.linalg.lstsq(exp.T, obj)[0] # 偏回帰係数

    return coef

def main():
    objects = Pick_Seq.objects.all()

    # パラメタの抽出
    param_dict = {}

    #{'', 'brink', 'sustain', 'shield', 'initiate', 'cc', 'heal', 'reflect_block', 'stealth', 'poke'}
    param_list = ["left_brink", "right_brink",
                  "left_cc", "right_cc",
                  "left_sustain", "right_sustain",
                  "left_shield", "right_shield",
                  "left_initiate", "right_initiate",
                  "left_heal", "right_heal",
                  "left_reflect_block", "right_reflect_block",
                  "left_stealth", "right_stealth",
                  "left_poke", "right_poke",
                  "left_adc", "right_adc",
                  "left_apc", "right_apc",
                  "left_win"]
    for p_name in param_list:
        param_dict[p_name] = []
    #for obj in objects[0:1000]:
    for obj in objects:
        blue_seq = [0, 2, 4, 7, 8, 11, 12]
        blue_team = [
            obj.pick5,
            obj.pick8,
            obj.pick9,
            obj.pick12,
            obj.pick13]
        red_team = [
            obj.pick6,
            obj.pick7,
            obj.pick10,
            obj.pick11,
            obj.pick14]

        blue_feature = {}
        for hero in blue_team:
            hero_obj = Hero.objects.get(Q(hero_id=hero))
            for f in hero_obj.feature.split(":"):
                if f in blue_feature:
                    blue_feature[f] += 1
                else:
                    blue_feature[f] = 1

        red_feature = {}
        for hero in red_team:
            hero_obj = Hero.objects.get(Q(hero_id=hero))
            for f in hero_obj.feature.split(":"):
                if f in red_feature:
                    red_feature[f] += 1
                else:
                    red_feature[f] = 1

        #{'', 'brink', 'sustain', 'shield', 'initiate', 'cc', 'heal', 'reflect_block', 'stealth', 'poke'}

        try:
            param_dict["left_brink"].append(blue_feature["brink"])
        except KeyError:
            param_dict["left_brink"].append(0)
        try:
            param_dict["right_brink"].append(red_feature["brink"])
        except KeyError:
            param_dict["right_brink"].append(0)

        try:
            param_dict["left_sustain"].append(blue_feature["sustain"])
        except KeyError:
            param_dict["left_sustain"].append(0)
        try:
            param_dict["right_sustain"].append(red_feature["sustain"])
        except KeyError:
            param_dict["right_sustain"].append(0)

        try:
            param_dict["left_shield"].append(blue_feature["shield"])
        except KeyError:
            param_dict["left_shield"].append(0)
        try:
            param_dict["right_shield"].append(red_feature["shield"])
        except KeyError:
            param_dict["right_shield"].append(0)

        try:
            param_dict["left_initiate"].append(blue_feature["initiate"])
        except KeyError:
            param_dict["left_initiate"].append(0)
        try:
            param_dict["right_initiate"].append(red_feature["initiate"])
        except KeyError:
            param_dict["right_initiate"].append(0)

        try:
            param_dict["left_cc"].append(blue_feature["cc"])
        except KeyError:
            param_dict["left_cc"].append(0)
        try:
            param_dict["right_cc"].append(red_feature["cc"])
        except KeyError:
            param_dict["right_cc"].append(0)

        try:
            param_dict["left_reflect_block"].append(blue_feature["reflect_block"])
        except KeyError:
            param_dict["left_reflect_block"].append(0)
        try:
            param_dict["right_reflect_block"].append(red_feature["reflect_block"])
        except KeyError:
            param_dict["right_reflect_block"].append(0)

        try:
            param_dict["left_stealth"].append(blue_feature["stealth"])
        except KeyError:
            param_dict["left_stealth"].append(0)
        try:
            param_dict["right_stealth"].append(red_feature["stealth"])
        except KeyError:
            param_dict["right_stealth"].append(0)

        try:
            param_dict["left_heal"].append(blue_feature["heal"])
        except KeyError:
            param_dict["left_heal"].append(0)
        try:
            param_dict["right_heal"].append(red_feature["heal"])
        except KeyError:
            param_dict["right_heal"].append(0)

        try:
            param_dict["left_poke"].append(blue_feature["poke"])
        except KeyError:
            param_dict["left_poke"].append(0)
        try:
            param_dict["right_poke"].append(red_feature["poke"])
        except KeyError:
            param_dict["right_poke"].append(0)

        try:
            param_dict["left_adc"].append(blue_feature["adc"])
        except KeyError:
            param_dict["left_adc"].append(0)
        try:
            param_dict["right_adc"].append(red_feature["adc"])
        except KeyError:
            param_dict["right_adc"].append(0)

        try:
            param_dict["left_apc"].append(blue_feature["apc"])
        except KeyError:
            param_dict["left_apc"].append(0)
        try:
            param_dict["right_apc"].append(red_feature["apc"])
        except KeyError:
            param_dict["right_apc"].append(0)

        if obj.left_win:
            param_dict["left_win"].append(1)
        else:
            param_dict["left_win"].append(0)

    lb = tuple(param_dict["left_brink"])
    rb = tuple(param_dict["right_brink"])
    lsh = tuple(param_dict["left_shield"])
    rsh = tuple(param_dict["right_shield"])
    li = tuple(param_dict["left_initiate"])
    ri = tuple(param_dict["right_initiate"])
    lh = tuple(param_dict["left_heal"])
    rh = tuple(param_dict["right_heal"])
    lr = tuple(param_dict["left_reflect_block"])
    rr = tuple(param_dict["right_reflect_block"])
    lst = tuple(param_dict["left_stealth"])
    rst = tuple(param_dict["right_stealth"])
    lcc = tuple(param_dict["left_cc"])
    rcc = tuple(param_dict["right_cc"])
    lp = tuple(param_dict["left_poke"])
    rp = tuple(param_dict["right_poke"])
    ladc = tuple(param_dict["left_adc"])
    radc = tuple(param_dict["right_adc"])
    lapc = tuple(param_dict["left_apc"])
    rapc = tuple(param_dict["right_apc"])

    lw = tuple(param_dict["left_win"])

    obj = np.array(lw)      # 目的変数
    exp = np.array([lb, rb, lsh, rsh, li, ri, lh, rh, lst, rst, lcc, rcc, lr, rr, lp, rp, ladc, radc, lapc, rapc]) # 説明変数
    tup = stat(obj, exp)
    b0 = tup[0]
    lb = tup[1]
    rb = tup[2]
    lsh = tup[3]
    rsh = tup[4]
    li = tup[5]
    ri = tup[6]
    lh = tup[7]
    rh = tup[8]
    lst = tup[9]
    rst = tup[10]
    lcc = tup[11]
    rcc = tup[12]
    lr = tup[13]
    rr = tup[14]
    lp = tup[15]
    rp = tup[16]
    ladc = tup[17]
    radc = tup[18]
    lapc = tup[19]
    rapc = tup[20]

    print("重回帰式: 左勝率 = %f + %f*lb + %f*rb + %f*lsh + %f*rsh + %f*li +%f*ri + %f*lh + %f*rh + %f*lr + %f*rr + %f*lst + %f*rst + %f*lcc + %f*rcc + %f*lp + %f*rp + %f*ladc + %f*radc + %f*lapc+ %f*rapc" % (b0, lb, rb, lsh, rsh, li, ri, lh, rh, lr, rr, lst, rst, lcc, rcc, lp, rp, ladc,radc, lapc, rapc))
    coef = {}
    #(b0, lb, rb, lsh, rsh, li, ri, lh, rh, lr, rr, lst, rst, lcc, rcc, lp, rp)

    coef["b0"] = b0
    coef["left_brink"] = lb
    coef["right_brink"] = rb
    coef["left_shield"] = lsh
    coef["right_shield"] = rsh
    coef["left_initiate"] = li
    coef["right_initiate"] = ri
    coef["left_heal"] = lh
    coef["right_heal"] = rh
    coef["left_reflect_block"] = lr
    coef["right_reflect_block"] = rr
    coef["left_stealth"] = lst
    coef["right_stealth"] = rst
    coef["left_cc"] = lcc
    coef["right_cc"] = rcc
    coef["left_poke"] = lp
    coef["right_poke"] = rp
    coef["left_adc"] = ladc
    coef["right_adc"] = radc
    coef["left_apc"] = lapc
    coef["right_apc"] = rapc

    with open("coef.dat", "wb") as f:
        pickle.dump(coef, f)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from banpick.models import Pick_Seq, Hero

    main()
