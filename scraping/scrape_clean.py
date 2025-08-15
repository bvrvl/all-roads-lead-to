import requests
from bs4 import BeautifulSoup
import re

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_places_from_highway(highway_url):
    """Return raw place names from one highway page."""
    response = requests.get(highway_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    tables = soup.find_all('table', class_='wikitable')
    raw_places = []
    for table in tables:
        header_cells = [th.get_text(strip=True).lower() for th in table.find_all('th')]
        if any(k in header_cells for k in ['junctions', 'location', 'route', 'major intersections']):
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if cells:
                    raw_places.append(cells[0].get_text(strip=True))
    return raw_places

def clean_places(raw_places):
    """Return a cleaned list of place names."""
    cleaned = []
    for place_text in raw_places:
        place_text = re.sub(r'\[\d+\]', '', place_text)   # remove [1]
        place_text = re.sub(r'\(.*?\)', '', place_text)   # remove (foo)
        for place in re.split(r'\n|,', place_text):
            name = place.strip()
            if name and len(name) > 2:
                cleaned.append(name)
    return list(set(cleaned))