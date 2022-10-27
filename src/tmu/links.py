from usp.tree import sitemap_tree_for_homepage
from webscraper.urlutils import Url
import requests
import time
import os
import re
from collections import Counter
import random
import glob


def readfiles(folderpath, n=None, ext=""):
    filenames = glob.glob(folderpath + "/*" + ext)

    if not n:
        n = len(filenames)

    results = []
    for i in range(n):
        f = open(filenames[i], "r")
        results.append(f.read())
        f.close()

    return results


def getsitemaplinks(url):
    tree = sitemap_tree_for_homepage(url)

    links = []
    for page in tree.all_pages():
        links.append(page.url)

    return links


def batchdownload(lines, resdir=".", timeout=10):
    try:
        if not os.path.exists(resdir):
            os.makedirs(resdir)
        while len(lines) != 0:
            line = lines[0]
            print("downloading: " + line)
            html = requests.get(line).text
            time.sleep(timeout)
            f = open(resdir + "/" + Url(line).tofilename(), "w", encoding="utf-8")
            f.write(html)
            f.close()
            lines.remove(line)
    except Exception as e:
        print(e)

    return lines


def readlines(path):
    f = open(path, "r", encoding="utf-8")
    lines = f.read()
    lines = lines.split()
    f.close()
    return lines


def savelines(lines, path):
    f = open(path, "w", encoding="utf-8")
    for line in lines:
        f.write(line + "\n")
    f.close()


def uniq(lines):
    return list(dict.fromkeys(lines))


def grep(lines, regex):
    result = []

    if len(lines) == 1:
        temp = re.match(regex, lines)
        if temp:
            return lines
        else:
            return ""

    for line in lines:
        temp = re.match(regex, line)
        if temp:
            result.append(line)
    return result


def head(lines, count=10):
    result = []
    if count > len(lines):
        count = len(lines)

    for i in range(0, count):
        result.append(lines[i])
    return result


def union(a, b):
    res = set(a)
    res.union(set(b))
    return list(res)


def diff(a, b):
    res = set(a)
    res.difference(set(b))
    return list(res)


def inter(a, b):
    res = set(a)
    res.intersection(set(b))
    return list(res)


def sort(lines):
    return lines.sort()


def getpaths(lines, maxlen=0):
    results = []

    for line in lines:
        paths = Url(line).paths
        if maxlen == 0:
            for path in paths:
                results.append(path)
        else:
            if maxlen > len(paths):
                maxlen = len(paths)
            for i in range(0, maxlen):
                results.append(paths[i])

    results = Counter(results)

    return results


def getlengths(lines):
    results = []
    for line in lines:
        paths = Url(line).paths
        results.append(len(paths))

    results = Counter(results)
    return results


def lengthfilter(lines, length=0):
    if length == 0:
        return lines

    results = []
    for line in lines:
        paths = Url(line).paths
        if len(paths) == length:
            results.append(line)

    return results


def getrandom(lines, length=10):
    results = []
    if length > len(lines):
        length = len(lines)

    start = random.randint(0, len(lines) - length)
    for i in range(start, start + length):
        results.append(lines[i])

    return results
