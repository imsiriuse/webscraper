# module works now only with
# html code and nothing more

from bs4 import BeautifulSoup

def concattags(tags):
    result = ""
    for tag in tags:
        result += tag.get_text() + " "
    return result


def getlinks(html, selector):
    # parse html by beatuiful soup $
    soup = BeautifulSoup(html, "html5lib")
    # use selector
    divs = soup.select(selector)
    # find all links from div
    links = []
    for div in divs:
        if div.name == 'a':
            href = div['href']
            if href not in links:
                links.append(href)
            continue

        aas = div.find_all('a')
        for a in aas:
            href = a['href']
            if href not in links:
                links.append(href)
    return links


def getcontent(html, contentids, contents):
    # parse html with BS
    soup = BeautifulSoup(html, "html5lib")

    result = []
    for selectorid in contentids:
        tags = soup.select(contents[selectorid])

        # add to result file in form of pair col number and string
        result.append((selectorid, concattags(tags)))
    return result

def getrandomlink(html, domain):
    pass
