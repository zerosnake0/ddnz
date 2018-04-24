import requests


def getip():
    r = requests.get("https://api.ipify.org/")
    if r.ok:
        return r.text
