#! /usr/bin/python3

import os
import requests
import json
import time
import datetime

APIKEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0M2Y4ZDliMC1iOGI5LTAxMzUtNjkwNC0wYTU4NjQ2MGFhYzQiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTEyMTI3OTYxLCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJ2Z19ubiIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.IbSw6eT8OgF7Kn3Vk9QAttgoCkshH2PxGWqnAtbA5Is"

header = {
        "Authorization": APIKEY,
        "Accept": "application/vnd.api+json"
        }


def get_matches(offset, now, yesterday, area="na"):
    url = "https://api.dc01.gamelockerapp.com/shards/"+area+"/matches"
    query = {
            #"filter[gameMode]": "ranked",
            "filter[gameMode]": "5v5_pvp_ranked",
            "page[offset]": offset,
            "page[limit]": "5",
            #"filter[createdAt-start]": "2017-12-06T11:47:48Z",
            "filter[createdAt-start]": yesterday.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "filter[createdAt-end]": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

    r = requests.get(url, headers=header, params=query)
    IDs = []
    for data in r.json()["data"]:
        ID = data["id"]
        asset_id = data["relationships"]["assets"]["data"][0]["id"]
        version = data["attributes"]["patchVersion"]
        IDs.append({"id": ID, "asset": asset_id, "version": version})


    #with open("data/raw/raw_%d.json" % offset, "w") as f:
        #f.write(json.dumps(r.json(), indent=4))

    tel2ros = create_tel_to_roster_dict(r.json())

    num = offset
    tel_infos = get_telemetory_info(r.json())

    for ID_obj in IDs:
        ID = ID_obj["id"]
        asset_id = ID_obj["asset"]
        version = ID_obj["version"]

        dic = {}
        tel_url = tel_infos[asset_id]
        seq = get_pick_seq(tel_url, asset_id)
        dic["pick"] = seq

        ros_id = tel2ros[asset_id]
        win, side = is_win(r.json(), ros_id)
        if win == "true":
            dic["winner"] = side
            dic["loser"] = "another"
        else:
            dic["winner"] = "another"
            dic["loser"] = side

        if not os.path.exists("data/pick/%s" % version):
            os.mkdir("data/pick/%s" % version)
        with open("data/pick/%s/%s.json" % (version, ID), "w") as f:
            f.write(json.dumps(dic, indent=4))
        num += 1
        time.sleep(1.5)


def is_win(match_obj, ros_id):
    for data in match_obj["included"]:
        if data["type"] == "roster":
            if data["id"] == ros_id:
                won = data["attributes"]["won"]
                side = data["attributes"]["stats"]["side"]
                return won, side

def create_tel_to_roster_dict(match_obj):
    dic = {}
    for match in match_obj["data"]:
        if match["type"] == "match":
            asset_id = match["relationships"]["assets"]["data"][0]["id"]
            roster_id = match["relationships"]["rosters"]["data"][0]["id"]
            dic[asset_id] = roster_id
    return dic

def get_telemetory_info(match_obj):
    urls = {}
    for data in match_obj["included"]:
        if data["type"] == "asset":
            asset_id = data["id"]
            if __debug__:
                print(data["attributes"]["URL"])
            url = data["attributes"]["URL"]
            urls[asset_id] = url
    return urls


def get_pick_seq(tel_url, ID):
    ret = []
    tel_res = requests.get(tel_url, headers=header)

    """
    with open("data/tel/tel_%s.json" % ID, "w") as f:
            f.write(json.dumps(tel_res.json(), indent=4))
    """

    for payload in tel_res.json():
        if payload["type"] == "HeroBan":
            if __debug__:
                print(payload)
            ret.append(payload)

        if payload["type"] == "HeroSelect":
            if __debug__:
                print(payload)
            ret.append(payload)

    return ret


def main():
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("data/pick"):
        os.mkdir("data/pick")
    n = datetime.datetime.now()
    y = n - datetime.timedelta(days = 1)
    area = ["ea", "na"]
    for area_code in area:
        for i in range(0, 20000, 5):
            get_matches(i, n, y, area_code)

#print(json.dumps(r.json(), indent=4))


if __name__ == "__main__":
    now = datetime.datetime.now()
    tomorrow = now
    while True:
        if now >= tomorrow:
            try:
                print("Start getting logs at " + str(now))
                main()
            except Exception as e:
                print(e)
            tomorrow = now + datetime.timedelta(days = 1)
        else:
            time.sleep(900)

        now = datetime.datetime.now()
