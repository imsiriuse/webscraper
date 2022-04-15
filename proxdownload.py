import requests
import re


# http://spys.me/proxy.txt
def getspysme():
    # download text file
    try:
        content = requests.get("https://spys.me/proxy.txt").text
    except Exception as e:
        print(e)
        print('Exception during download spys.me/proxy.txt')
        return []

    # grep only IP adresses
    found = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5} ..-H-S.*", content)
    # extract only ip adress
    i = 0
    for line in found:
        found[i] = line.split()[0]
        i += 1
    return found


# https://free-proxy-list.net/
def getfreeproxylist():
    # download text file

    # for now download it
    content = requests.get("https://free-proxy-list.net/").text
    found = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", content)
    return found


def getlist():

    proxylinks = []
    # start downloads
    proxylinks = proxylinks + getspysme()
    # proxylinks = proxylinks + getFreeProxyList()
    getfreeproxylist()
    return proxylinks
