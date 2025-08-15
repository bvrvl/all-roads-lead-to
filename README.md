# All Roads Lead To: A Data-Driven Analysis of Nepal's Highway Network

[![Status](https://img.shields.io/badge/status-complete-green.svg)](https://github.com/bvrvl/all-roads-lead-to)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

This project explores Nepal's national highway system to answer a simple question: All Roads Lead to ___ ?

Through a programmatic analysis of all 80 national highways listed on Wikipedia, this project scrapes, processes, and analyzes the network's structure to find the most connected hubs in the country.

The initial assumption was that the central hub would be a major city like Kathmandu or Hetauda. The data, however, revealed a surprising answer.

## The Finding: All Roads Lead to Koshi Province

The heart of Nepal's highway network isn't a single city, but a province. **Koshi Province** is the most frequently mentioned region across the entire highway system, making it the "Rome" of Nepal in this analysis.

Here are the top 15 most connected places identified by the script:

| Place              | Connection Count |
| ------------------ | ---------------- |
| **Koshi Province** | **16**           |
| Madhesh Province   | 14               |
| Kathmandu          | 13               |
| Lumbini Province   | 10               |
| Bagmati Province   | 10               |
| Gandaki Province   | 7                |
| Karnali Province   | 6                |
| Jhapa              | 6                |
| Dhanusha District  | 6                |
| Pokhara            | 5                |
| Janakpur           | 5                |
| Nepal              | 5                |
| Siraha             | 5                |
| Lalitpur           | 4                |
| Chainpur           | 4                |

## The Story Behind the Data

For a full narrative about this project, the methodology, and personal reflections on the findings, please read the accompanying blog post: **[All Roads Lead to Koshi](https://bvrvl.com/all-roads-lead-to-koshi.html)**.

> I remember returning from Kathmandu and seeing the Koshi River. It was that moment when everything felt like home... It feels fitting that all roads lead here. After all, *rome* is where the heart is.

---

## Methodology

The project follows a multi-step, automated workflow to arrive at its conclusion:

1.  **Link Discovery:** The script begins by scraping the main [Wikipedia page on the National Highways of Nepal](https://en.wikipedia.org/wiki/National_Highway_System_(Nepal)) to gather the unique URLs for all 80 individual highway pages.

2.  **HTML Scraping & Cleaning:** For each highway URL, the script fetches the page's HTML. To ensure high-quality data, it performs a crucial pre-processing step, surgically removing two major sources of noise:
    *   The "National Highway System" navigation box at the bottom of each page.
    *   The "References" section and its associated citation lists.
    This ensures that only the relevant article content is analyzed.

3.  **Intelligent Extraction with Gemini:** The cleaned text content is then passed to the Google Gemini API (gemini-2.5-flash). A carefully crafted prompt instructs the AI to read the text and extract all names of cities, towns, villages, and districts mentioned. This AI-driven approach is robust enough to handle unstructured paragraphs and varied page layouts where simple table scraping would fail.

4.  **Data Aggregation & Analysis:** The extracted places for each highway are compiled into a raw CSV file (`nepal_highways_raw_data.csv`). A final script then uses the `pandas` library to calculate the frequency of each place, determining how many highways connect to it.

5.  **Output Generation:** The final analysis is saved to `nepal_city_connections.csv` and the top 20 results are printed to the console.

## Project Structure

The codebase is organized into a modular 5-file structure for clarity and maintainability.

```/
├── scraping/
│ ├── main.py # The main entry point to run the entire project.
│ ├── get_highway_links.py # Fetches all individual highway URLs.
│ ├── scrape_clean.py # Scrapes and cleans HTML; contains the Gemini API call.
│ ├── build_save.py # Orchestrates the scraping loop and saves raw data.
│ └── analyze_display.py # Analyzes the raw data and displays the final results.
└── .env # For storing the Gemini API Key.
```

## How to Run This Project

To replicate this analysis, follow these steps:

**1. Clone the Repository:**
```bash
git clone https://github.com/bvrvl/all-roads-lead-to.git
cd all-roads-lead-to
```
**2. Set Up a Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**3. Install Dependencies:**
A `requirements.txt`` file is included.
```bash
pip install -r requirements.txt
```
**4. Create an Environment File**
Create a file named .env in the project's root directory. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and add it to the file:
```env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```
## Output Files
Upon successful execution, two CSV files will be generated in the root directory:
- `nepal_highways_raw_data.csv`: A detailed list of every highway and every single place Gemini identified along its route.
- `nepal_city_connections.csv`: The final, aggregated analysis showing each unique place and its total connection count, sorted from most to least connected.
---
### License
This project is licensed under the MIT License. See the LICENSE file for details.
