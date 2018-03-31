#! /usr/bin/python3

import requests

url = "https://api.dc01.gamelockerapp.com/shards/ea/matches"

APIKEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0M2Y4ZDliMC1iOGI5LTAxMzUtNjkwNC0wYTU4NjQ2MGFhYzQiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTEyMTI3OTYxLCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJ2Z19ubiIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.IbSw6eT8OgF7Kn3Vk9QAttgoCkshH2PxGWqnAtbA5Is"

header = {
        "Authorization": APIKEY,
            "Accept": "application/vnd.api+json"
}

query = {
    "sort": "createdAt",
    "filter[playerNames]": "BoiledEggEx",
    "page[limit]": "3"
}

r = requests.get(url, headers=header, params=query)

print(r.json())
