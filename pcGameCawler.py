from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from collections import defaultdict
import json

# TODO instrument, music genre

# https://en.wikipedia.org/wiki/List_of_video_game_musicians

def crawl_developer_wikiList(url="https://en.wikipedia.org/wiki/List_of_video_game_developers"):
    # TODO developer (name, started, location)
    return

def crawl_game_wikiList(url):
    url = 'https://en.wikipedia.org/wiki/List_of_PC_games_(B)'
    soup = bs(requests.get(url).content, features='html.parser')
    count = 0
    d = {}
    for td in soup.findAll('table')[0].findAll('td'):
        if count % 6 == 0:
            try:
                string = td.a.string
                d[string] = defaultdict(list)
                d[string].update(crawl_game_infobox(td.a.get('href')))
            except:
                string = td.string
                d[string] = defaultdict(list)
            name = string
        elif count % 6 == 1:
            try:
                for a in td.findAll('a'):
                    d[name]['developer'].append(a.string)
            except:
                print(d[name])
                print(d[name]['developer'])
                d[name]['developer'].append(td.string)
        elif count % 6 == 3:
            try:
                string = td.a.string
            except:
                string = td.string
            d[name]['genre'] = string
        elif count % 6 == 5:
            try:
                release_date = datetime.strptime(td.span['data-sort-value'][8:-5], '%Y-%m-%d')
            except:
                release_date = datetime.strptime(td.string[:-1], '%B %d, %Y')
            d[name]['date_release'] = datetime.date(release_date).strftime('%Y-%m-%d')
        count += 1
    """
    with open(url[-20:] + '.json', 'w') as f:
        json.dump(d, f)
    """
    print(d)


def crawl_game_infobox(url):
    d = defaultdict(list)
    soup = bs(requests.get("https://en.wikipedia.org" + url).content, features='html.parser')
    # TODO game (description), producer(name, nation, age), developer (name, started, location)
    info = soup.find('table', {'class':'infobox hproduct'})
    for tr in info.findAll('tr'):
        if tr.find('a'):
            a = tr.find('a')
            if a.get('title') == 'Video game composer':
                d['composer'] = tr.find('td').string
            elif a.get('title') == "Video game producer":
                if tr.find('td').find('li'):
                    for li in tr.find('td').findAll('li'):
                        print(li.string)
                        d['producer'].append(tr.find('td').string)
                else:
                    d['producer'] = tr.find('td').string
            # elif a.get('title') == "Video game developer":
                # d['developer'] = tr.find('td').string
    return d

crawl_game_wikiList('/wiki/Dark_Souls')
