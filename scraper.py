import argparse, os
import lxml.html
import scraperwiki
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', help='year')
    parser.add_argument('-m', help='month')
    parser.add_argument('-d', help='day')
    parser.add_argument('-l', help='language')
    args = parser.parse_args()
    pre_crawl(args.y, args.m, args.d, args.l)


def init_soup(page):
    soup = BeautifulSoup(page.html, "html.parser")
    return soup


def init_output(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def pre_crawl(year, month, day, lang):
    TARGET_URL = 'http://www.hko.gov.hk/cgi-bin/hko/yes.pl?year={YEAR}&month={MONTH}&day={DAY}&language={LANGUAGE}&B1=Confirm'
    d = datetime.today() - timedelta(days=1)

    if year is None:
        year = d.year

    if month is None:
        month = d.strftime('%m')

    if day is None:
        day = d.strftime('%d')

    if lang is None:
        lang = 'english'

    crawl(TARGET_URL.replace('{YEAR}', str(year)).replace('{MONTH}', str(month)).replace('{DAY}', str(day)).replace('{LANGUAGE}', lang))


def crawl(url):
    html = scraperwiki.scrape(url)
    r = lxml.html.fromstring(html)
    el = r.cssselect("pre")[0]
    lines = el.text.splitlines()

    s_arr = []
    min_arr = []
    max_arr = []
    for l in lines[16:41]:
        station = l.strip()[0:15]
        min = l.strip()[26:35]
        max = l.strip()[36:]

        s_arr.append(station.strip())
        min_arr.append(min.strip())
        max_arr.append(max.strip())

    d = datetime.today() - timedelta(days=1)
    str_d = str(d.date())

    ytd_weather = pd.DataFrame({
        'date': str_d,
        'station': s_arr,
        'min': min_arr,
        'max': max_arr
    }, columns=['date', 'station', 'min', 'max'])

    ytd_weather.to_json('weather.json', orient='records')


if __name__ == '__main__':
    init()