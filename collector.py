# Copyright 2012-2023 The Collector (lite) - Mr.Chess

import requests, time, re
from bs4 import BeautifulSoup
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
        print(f"Error accessing URL {url}\n\n{e}") # changed to English + new lines for readabilty 
        return
    if response.status_code != 200:
        print(f"Error accessing URL {url}\n\nStatus code: {response.status_code}") # changed to English + new lines for readabilty 
        return
    visited_links.add(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for keyword in keywords:
        if keyword and keyword.lower() in response.text.lower():
            bad_sites.append(url)
            print(f"BAD Site Found: {url}") # changed to English
            break
    with Bar('Follow Links...', max=len(links)) as bar: # changed to English
        for link in links:
            href = link['href']
            if not (href.startswith('http') or href.startswith('https')):
                continue
            if href not in visited_links:
                bar.next()
                print(f"Visits: {href}") # changed to English
                find_links(href)
                time.sleep(2)
find_links(URL)
with open('collector_domainlist.txt', 'w') as file:
    for link in visited_links:
        if link in bad_sites:
            file.write(f"{link} BAD Site\n")
        else:
            file.write(f"{link}\n")