import time
import pandas as pd
from scrape_clean import get_page_text, extract_places_with_gemini

def build_connections(highway_urls):
    """Return list of {'highway': str, 'place': str} dicts for all highways using Gemini."""
    all_connections = []
    for url in highway_urls:
        highway_name = url.split('/')[-1].replace('_', ' ')
        print(f"\nProcessing {highway_name}...")
        
        page_text = get_page_text(url)
        
        if page_text:
            # Use Gemini to extract places from the text
            print("  - Asking Gemini to find places...")
            places = extract_places_with_gemini(page_text)
            print(f"  - Gemini found {len(places)} places.")
            for p in places:
                all_connections.append({'highway': highway_name, 'place': p})
        else:
            print("  - No text found to analyze.")
            
        time.sleep(2)  # Add a longer delay for API rate limits
    return all_connections

def save_raw_data(connections, filename="nepal_highways_raw_data.csv"):
    if not connections:
        print("No connections found to save.")
        return None
    df = pd.DataFrame(connections)
    df.to_csv(filename, index=False)
    print(f"\nRaw data saved to {filename}")
    return df