#!/usr/bin/python
#coding:utf-8

import sys, urllib, urllib.request
import os.path

def download(url, dir):
    if __debug__:
        print(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    img = urllib.request.urlopen(req)
    localfile = open(dir+os.path.basename(url), 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()


if __name__ == "__main__":
    Heros = ['vox', 'taka', 'idris', 'gwen',
              'celeste', 'grumpjaw', 'ringo',
              'phinn', 'baron', 'fortress',
              'joule', 'lyra', 'blackfeather',
              'ardan', 'skaarf', 'glaive', 'lance',
              'rona', 'churnwalker', 'samuel',
              'kestrel', 'baptiste', 'reza', 'petal',
              'koshka', 'adagio', 'saw', 'catherine',
              'skye', 'alpha', 'reim', 'grace', 'flicker',
              'ozo', 'krul', 'lorelai', 'varya', 'tony']

    url = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/"
    for hero in Heros:
        download(url+hero+".png", "icons/")


