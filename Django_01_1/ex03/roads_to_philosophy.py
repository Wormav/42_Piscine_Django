import sys
import requests
from bs4 import BeautifulSoup

def search_wikipeadia(path: str, prev: list) -> None:
    URL: str = 'https://en.wikipedia.org{page}'.format(page=path)
    try:
        res: requests.Response = requests.get(url=URL)
        res.raise_for_status()
    except requests.HTTPError as e:
        if (res.status_code == 404):
            return print("It's a dead end !")
        return print(e)

    soup: BeautifulSoup = BeautifulSoup(res.text, 'html.parser')
    title: str = soup.find(id='firstHeading').text

    if title in prev:
        return print("It leads to an infinite loop !")

    prev.append(title)
    print(title)

    if title == 'Philosophy':
        return print("{} roads from {} to Philosophy".format(len(prev), prev[0] if len(prev) > 0 else 'Philosophy'))

    content = soup.find(id='mw-content-text')
    allLinks = content.select('p > a')
    for link in allLinks:
        if link.get('href') is not None and link['href'].startswith('/wiki/') \
                and not link['href'].startswith('/wiki/Wikipedia:') and not link['href'].startswith('/wiki/Help:'):
            return search_wikipeadia(link['href'], prev)
    return print("It leads to a dead end !.")


def main() -> None:
    prev: List[str] = []
    if (len(sys.argv) == 2):
        search_wikipeadia('/wiki/' + sys.argv[1], prev)
    else:
        print('Usage: python3 roads_to_philosophy.py "search term"')


if __name__ == '__main__':
    main()