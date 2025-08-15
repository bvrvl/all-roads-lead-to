import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_highway_links(main_page_url):
    """Return list of all individual highway Wikipedia URLs."""
    print("Fetching highway links...")
    try:
        response = requests.get(main_page_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        highway_list_header = soup.find(id='List_of_national_highways')

        if not highway_list_header:
            print("Could not find the 'List_of_national_highways' section header.")
            return []

        # Find the first 'wikitable' that comes after the header
        table = highway_list_header.find_next('table', class_='wikitable')
        
        if not table:
            print("Found the header but could not find the wikitable after it.")
            return []

        links = set() # Use a set to automatically handle duplicate links
        for row in table.find_all('tr')[1:]:
            cells = row.find_all(['td', 'th'])
            for cell in cells:
                link_tag = cell.find('a')
                if link_tag and link_tag.get('href') and link_tag['href'].startswith('/wiki/'):
                    links.add(urljoin(main_page_url, link_tag['href']))
                    # Break here to only get the first valid link per row
                    break
        
        print(f"Found {len(links)} unique highway links.")
        return list(links)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return []