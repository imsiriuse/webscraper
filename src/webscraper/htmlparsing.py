from bs4 import BeautifulSoup


# module works now only with html code and nothing more
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


def getcontent(html, selector):
    # parse html with BS
    soup = BeautifulSoup(html, "html5lib")

    # select all found tags
    result =  soup.select(selector)

    return result