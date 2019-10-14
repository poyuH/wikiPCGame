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
    return


def crawl_game_wikiList(url, save=False):
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
            d[name]['description'] = wikipedia.summary(name)
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
        elif count % 6 == 5:
            try:
                release_date = datetime.strptime(td.span['data-sort-value'][8:-5], '%Y-%m-%d')
            except:
                release_date = datetime.strptime(td.string[:-1], '%B %d, %Y')
            d[name]['date_release'] = datetime.date(release_date).strftime('%Y-%m-%d')
        count += 1
        if count == 18:
            break
    if save:
        with open(url[-20:] + '.json', 'w') as f:
            json.dump(d, f)
    print(d)


def crawl_game_infobox(url):
    d = defaultdict(list)
    r = requests.get("https://en.wikipedia.org" + url)
    soup = bs(r.content, features='html.parser')
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


if __name__ == '__main__':
    # crawl_game_infobox('/wiki/Dark_Sun:_Shattered_Lands')
    # crawl_game_wikiList('https://en.wikipedia.org/wiki/List_of_PC_games_(B)')
    # print(wikipedia.summary("Dark_Souls"))
    crawl_developer_wikiList()
