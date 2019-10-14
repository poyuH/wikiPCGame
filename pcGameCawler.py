from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from collections import defaultdict
import json
import wikipedia

# TODO instrument, music genre, https://en.wikipedia.org/wiki/List_of_video_game_musicians

# TODO  producer(name, nation, age)

# TODO create list of producers, composers, and then manually fill out the rest

def _get_string_from_td(td):
    try:
        string = td.a.string
    except:
        string = td.string
    return string


def crawl_developer_wikiList(url="https://en.wikipedia.org/wiki/List_of_video_game_developers", save=False):
    # TODO developer (name, started, location)
    soup = bs(requests.get(url).content, features='html.parser')
    count = 0
    d = {}
    for td in soup.findAll('tbody')[2].findAll('td'):
        string = _get_string_from_td(td)
        if count % 7 == 0:
            d[string] = defaultdict(list)
            name = string
        elif count % 7 == 1:
            d[name]['city'] = string
        elif count % 7 == 3:
            try:
                d[name]['country'] = string[:-1]
            except:
                d[name]['country'] = None
        elif count % 7 == 4:
            try:
                if string=='\n':
                    d[name]['found_year'] = None
                else:
                    d[name]['found_year'] = int(string)
            except:
                print(name)
                print(td)
                string = input('your decision on found year:')
                d[name]['found_year'] = int(string)
        elif count % 7 == 5:
            if name in ('Gaijin Entertainment', 'Asobo Studio', 'Epic Games', 'Nippon Ichi Software', 'Robot Entertainment', 'Robinson Technologies', 'Sherman3D'):
                count += 1
            try:
                for a in td.findAll('a'):
                    d[name]['notable_games'].append(a.string)
            except:
                d[name]['notable_games'].append(td.string)
        count += 1
    if save:
        with open('vidio_game_developer.json', 'w') as f:
            json.dump(d, f)
    print(d)


def crawl_game_wikiList(url, save=False):
    soup = bs(requests.get(url).content, features='html.parser')
    count = 0
    d = {}
    for td in soup.findAll('table')[0].findAll('td'):
        if count % 6 == 0:
            if td.a:
                string = td.a.string
                print('try', string)
                d[string] = defaultdict(list)
                d[string].update(crawl_game_infobox(td.a.get('href')))
            else:
                string = td.string
                if not string:
                    string = td.find('i').string
                print('except', string)
                d[string] = defaultdict(list)
            name = string
            try:
                summary = wikipedia.summary(name)
            except:
                summary = None
            d[name]['description'] = summary
            if 'Red dead redemption\n' == string:
                count -= 1
        elif count % 6 == 1:
            try:
                for a in td.findAll('a'):
                    d[name]['developer'].append(a.string)
            except:
                d[name]['developer'].append(td.string)
        elif count % 6 == 3:
            try:
                string = td.a.string
            except:
                string = td.string
            d[name]['genre'] = string
            if name in ("Baldur's Gate II: Throne of Bhaal",):
                count += 1
        elif count % 6 == 5:
            if name in ("Resident Evil: Revelations 2", "Rocket League"):
                count -= 1
            try:
                release_date = datetime.strptime(td.span['data-sort-value'][8:-5], '%Y-%m-%d')
                d[name]['date_release'] = datetime.date(release_date).strftime('%Y-%m-%d')
            except:
                if td.string:
                    try:
                        release_date = datetime.strptime(td.string[:-1], '%B %d, %Y')
                        d[name]['date_release'] = datetime.date(release_date).strftime('%Y-%m-%d')
                    except:
                        d[name]['date_release'] = None
        count += 1
    if save:
        with open(url[-20:] + '.json', 'w') as f:
            json.dump(d, f)


def crawl_game_infobox(url):
    d = defaultdict(list)
    try:
        r = requests.get("https://en.wikipedia.org" + url)
    except:
        return d
    soup = bs(r.content, features='html.parser')
    info = soup.find('table', {'class':'infobox hproduct'})
    if not info:
        info = soup.find('table', {'class':'infobox'})
    if not info:
        return d
    for tr in info.findAll('tr'):
        if tr.find('a'):
            a = tr.find('a')
            if a.get('title') == 'Video game composer':
                d['composer'] = tr.find('td').string
            elif a.get('title') == "Video game producer":
                if tr.find('td').find('li'):
                    for li in tr.find('td').findAll('li'):
                        d['producer'].append(tr.find('td').string)
                else:
                    d['producer'] = tr.find('td').string
            # elif a.get('title') == "Video game developer":
                # d['developer'] = tr.find('td').string
    return d


if __name__ == '__main__':
    # crawl_game_infobox('/wiki/Dark_Sun:_Shattered_Lands')
    # crawl_game_wikiList('https://en.wikipedia.org/wiki/List_of_PC_games_(B)')
    # print(wikipedia.summary("Dark_Souls"))
    crawl_developer_wikiList()
