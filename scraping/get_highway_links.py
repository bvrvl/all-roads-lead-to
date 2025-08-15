import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_highway_links(main_page_url):
    """Return list of all individual highway Wikipedia URLs."""
    response = requests.get(main_page_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    highway_list_header = soup.find('span', id='List_of_national_highways')
    if not highway_list_header:
        return []

    table = highway_list_header.find_next('table', class_='wikitable')
    links = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all(['td', 'th'])
        for cell in cells:
            link_tag = cell.find('a')
            if link_tag and link_tag.get('href'):
                links.append(urljoin(main_page_url, link_tag['href']))
                break
    return links