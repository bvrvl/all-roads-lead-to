import time
import pandas as pd
from scrape_clean import get_page_text, extract_places_with_gemini

# Define rate limit interval in seconds
REQUEST_INTERVAL = 6.7  # (60 seconds / around 9 requests)

def build_connections(highway_urls):
    """Return list of {'highway': str, 'place': str} dicts for all highways using Gemini."""
    all_connections = []
    for url in highway_urls:
        # Record the start time of the loop
        loop_start_time = time.time()
        
        highway_name = url.split('/')[-1].replace('_', ' ')
        print(f"\nProcessing {highway_name}...")
        
        page_text = get_page_text(url)
        
        if page_text:
            print("  - Asking Gemini to find places...")
            places = extract_places_with_gemini(page_text)
            print(f"  - Gemini found {len(places)} places.")
            for p in places:
                all_connections.append({'highway': highway_name, 'place': p})
        else:
            print("  - No text found to analyze.")
        
        # Calculate how long the processing took
        processing_time = time.time() - loop_start_time
        
        # Calculate how long still need to wait
        wait_time = REQUEST_INTERVAL - processing_time
        
        if wait_time > 0:
            print(f"  - Waiting for {wait_time:.2f} seconds to respect rate limit.")
            time.sleep(wait_time)
            
    return all_connections

def save_raw_data(connections, filename="nepal_highways_raw_data.csv"):
    if not connections:
        print("No connections found to save.")
        return None
    df = pd.DataFrame(connections)
    df.to_csv(filename, index=False)
    print(f"\nRaw data saved to {filename}")
    return df