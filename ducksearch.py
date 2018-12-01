"""duckduckgo wrapper/html scraper"""
from urllib import request
from urllib.parse import urlencode, quote_plus, unquote
from bs4 import BeautifulSoup

SEARCH_URL = "https://duckduckgo.com/html/"


def _parse_href(link):
    if link is None or link["href"] is None:
        return None
    sep = link["href"].find("&uddg=")
    if sep == -1:
        return link["href"]
    return unquote(link["href"][sep + 6:])


def ifeellucky(term):
    """return the first result url"""
    query = {"q": term}
    url = SEARCH_URL + "?" + urlencode(query, quote_via=quote_plus)
    print(" ->", "search=", url)
    result_html = request.urlopen(url).read()
    soup = BeautifulSoup(result_html, "html.parser")
    link = soup.find("a", class_="result__url")
    return _parse_href(link)


def beer(term):
    """return the first beer from untappd.com"""
    result = ifeellucky("site:untappd.com " + term)
    if result is None:
        return None
    segments = result.split("/")
    if len(segments) < 4 or segments[3].lower() != "b":
        return None
    return result
