def analyze_connections(df, filename="nepal_city_connections.csv"):
    city_counts = df['place'].value_counts().reset_index()
    city_counts.columns = ['place', 'connection_count']
    city_counts.to_csv(filename, index=False)
    print(f"Analysis saved to {filename}")
    return city_counts

def display_top_cities(city_counts, n=20):
    print("\n--- All Roads Lead To... ---")
    print(f"Top {n} Most Connected Places in Nepal's Highway System:")
    print(city_counts.head(n).to_string(index=False))