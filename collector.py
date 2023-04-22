# Copyright 2012-2023 The Collector (lite) - Mr.Chess
import requests
from bs4 import BeautifulSoup
import re
import time
from progress.bar import Bar
URL = 'https://targetonionwebsites.onion'
keywords = ['Keyword1', 'Keyword2', 'Keyword3']  # add your keywords
visited_links = set()
bad_sites = []
def find_links(url):
    global visited_links
    global bad_sites
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Error beim Zugriff auf URL {url}: {e}")
        return
    if response.status_code != 200:
        print(f"Error beim Zugriff auf URL {url}: Statuscode {response.status_code}")
        return
    visited_links.add(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for keyword in keywords:
        if keyword and keyword.lower() in response.text.lower():
            bad_sites.append(url)
            print(f"BAD Site gefunden: {url}")
            break
    with Bar('Verfolge Links...', max=len(links)) as bar:
        for link in links:
            href = link['href']
            if not (href.startswith('http') or href.startswith('https')):
                continue
            if href not in visited_links:
                bar.next()
                print(f"Besuche: {href}")
                find_links(href)
                time.sleep(2)
find_links(URL)
with open('collector_domainlist.txt', 'w') as file:
    for link in visited_links:
        if link in bad_sites:
            file.write(f"{link} BAD Site\n")
        else:
            file.write(f"{link}\n")
