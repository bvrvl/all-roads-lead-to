from dotenv import load_dotenv
load_dotenv()
from get_highway_links import get_highway_links
from build_save import build_connections, save_raw_data
from analyze_display import analyze_connections, display_top_cities

MAIN_WIKI_URL = "https://en.wikipedia.org/wiki/National_Highway_System_(Nepal)"

if __name__ == "__main__":
    print("--- Starting Nepal Highway Analysis Project ---")

    urls = get_highway_links(MAIN_WIKI_URL)
    if not urls:
        print("No highway links found. Exiting.")
    else:
        connections = build_connections(urls)
        if connections:
            df = save_raw_data(connections)
            city_counts = analyze_connections(df)
            display_top_cities(city_counts)
        else:
            print("No data collected. Exiting.")