import json
import urllib.request


def downloadFile(url, filename="ffile.jpg"):
    # Download the file from `url` and save it locally under `file_name`:
    urllib.request.urlretrieve(url, filename)


furl = "https://my.mail.ru/87dce9f0-3298-4004-a5ac-e35f67f4f869"

# downloadFile(furl, "ff.mp4")  # "http://192.168.2.207:8000/static/123.jpg"

first = "https://my.mail.ru/community/new-year/video/newyear/105.html"

a = {'provider': 'ugc', 'multiOverlay': 3, 'skipOverlay': False, 'isChannel': False,
     'author': {'profile': '/community/new-year/', 'email': 'new-year', 'name': 'new-year'},
     'meta': {'externalId': 'community/new-year/newyear/105', 'accId': 63777460, 'duration': 197, 'viewsCount': 22473,
              'itemId': 105, 'timestamp': 1512645420, 'url': '//my.mail.ru/community/new-year/video/newyear/105.html',
              'id': '-16599924044988311', 'title': 'sergej.mov',
              'poster': '//filed14-4.my.mail.ru/pic?url=http%3A%2F%2Fmy.mail.ru%2F%2B%2Fvideo%2Furl%2Fsc02%2F-16599924044988311&sigt=852628953526d166066f0d9c5182bdc7&ts=1513156491'},
     'overlayTime': 10, 'relatedHost': '//my.mail.ru/+/video', 'adSlot': 10000000, 'isCommunity': True,
     'encoding': True, 'cluster': {'name': '', 'id': 0}, 'targetParent': False, 'flags': 16387,
     'admanUrl': '//ad.mail.ru/static/admanhtml/2.1.28/rbadman-html5.min.js', 'version': 3, 'skipAd': False,
     'isPrivate': False, 'region': 188, 'service': 'mail', 'spAccess': None, 'sitezone': None,
     'backscreenCounter': None, 'videos': [{
        'url': '//cdn25.my.mail.ru/hv/63777460.mp4?slave[]=s%3Ahttp%3A%2F%2F127.0.0.1%3A5010%2F63777460-hv.mp4&p=f&expire_at=1513166400&touch=1512605046&reg=188&sign=0a5e2de3020532a5818afb1637cef5f29d3bbfe5',
        'seekSchema': 3, 'key': '1080p'}, {
        'url': '//cdn25.my.mail.ru/v/63777460.mp4?slave[]=s%3Ahttp%3A%2F%2F127.0.0.1%3A5010%2F63777460-v.mp4&p=f&expire_at=1513166400&touch=1512605046&reg=188&sign=53229c5ba7d44ad9a992fd9fd2c474e8ed0e700e',
        'seekSchema': 3, 'key': '360p'}], 'dash': True}

# print(json.loads(a))
url = "http://35.198.161.58/static/123.png"

print(downloadFile(url, filename="ff.png"))
