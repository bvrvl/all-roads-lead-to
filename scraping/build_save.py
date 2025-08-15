import time
import pandas as pd
from scrape_clean import scrape_places_from_highway, clean_places

def build_connections(highway_urls):
    """Return list of {'highway': str, 'place': str} dicts for all highways."""
    all_connections = []
    for url in highway_urls:
        highway_name = url.split('/')[-1].replace('_', ' ')
        print(f"Scraping {highway_name} ...")
        raw_places = scrape_places_from_highway(url)
        places = clean_places(raw_places)
        print(f"  - {len(places)} unique places found.")
        for p in places:
            all_connections.append({'highway': highway_name, 'place': p})
        time.sleep(1)  # delay
    return all_connections

def save_raw_data(connections, filename="nepal_highways_raw_data.csv"):
    df = pd.DataFrame(connections)
    df.to_csv(filename, index=False)
    print(f"Raw data saved to {filename}")
    return df