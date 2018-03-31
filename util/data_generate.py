#! /usr/bin/python3

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


def get_ban_pick(path):
    ret = {}
    dec = None
    with open(path) as f:
        dec = json.load(f)
    seq = []
    action_set = set()
    for event in dec["pick"]:
        action = event['type']
        team = event['payload']['Team']
        hero = event['payload']['Hero']
        seq.append({"action": action,
                    "team": team,
                    "hero": hero})
        action_set.add(action)
    if "HeroBan" not in action_set:
        return None
    ret["seq"] = seq

    if dec["winner"] == "left/blue":
        ret["winner"] = 1
    else:
        ret["winner"] = -1

    return ret


def ban_pick_list():
    ranked_list = []
    for path in glob.glob("data/pick/*.json"):
        dic = get_ban_pick(path)
        if dic is not None:
            ranked_list.append(dic)

    print("Sample count %d" % len(ranked_list))

    for d in ranked_list:
        data_list = []
        for pick in d["seq"]:
            hero = pick["hero"]
            data_list.append(hero)
        data_list.append(str(d["winner"]))
        print(" ".join(data_list))


def pick_dict():
    pick_list = []
    for path in glob.glob("data/pick/*.json"):
        dic = get_pick(path)
        if dic is not None:
            pick_list.append(dic)

    print("Sample count %d" % len(pick_list))

    dic = {}
    tmp_set = set()
    for d in pick_list:
        team1 = tuple(sorted(d["teams"]['1']))
        team2 = tuple(sorted(d["teams"]['2']))

        if team1 in tmp_set:
            dic[team1].append(1 if d["winner"] == 1 else 0)
        else:
            dic[team1] = [1] if d["winner"] == 1 else [0]
            tmp_set.add(team1)

        if team2 in tmp_set:
            dic[team2].append(1 if d["winner"] == -1 else 0)
        else:
            dic[team2] = [1] if d["winner"] == -1 else [0] 
            tmp_set.add(team2)
        
    for team, rate in dic.items():
        if len(rate) != 0:
            print(str(team) + " %f" % (sum(rate) / len(rate)))
        else:
            print("No record")
    print(len(dic))
    return dic


def get_win_rate(dic, pick_set):
    mean = []
    team_cmp = {}
    for team, rate in dic.items():
        if pick_set <= set(team):
            mean.extend(rate)
            win_rate  = sum(rate) / len(rate)
            match_count = len(rate)
            team_cmp[team] = (win_rate, match_count)
    if len(mean) != 0:
        print(pick_set, (sum(mean) / len(mean)), len(mean))
    else:
        print("No record")

    print("Recommend")
    for team, rate in sorted(team_cmp.items(), key=lambda x: x[1][0], reverse=True)[:10]:
        print(team, rate)


def main():
    ban_pick_list()
    exit()
    dic = pick_dict()
    while True:
        names = input("Hero names: ")
        get_win_rate(dic, set(names.split()))


if __name__ == "__main__":
    main()
