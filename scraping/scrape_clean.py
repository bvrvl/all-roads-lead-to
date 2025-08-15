import requests
from bs4 import BeautifulSoup
import os
from google import genai
import json

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_page_text(highway_url):
    """Return the clean, visible text content of a highway page."""
    try:
        response = requests.get(highway_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        content_div = soup.find(id='mw-content-text')
        if content_div:
            return content_div.get_text(separator=' ', strip=True)
        return ""
    except requests.exceptions.RequestException as e:
        print(f"    - Could not scrape {highway_url}. Error: {e}")
        return ""

def extract_places_with_gemini(page_text):
    """
    Uses the Gemini API to extract Nepalese place names from text.
    The API key is loaded automatically from the .env file.
    """
    try:
        # Configure the Gemini API client
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        From the following text about a highway in Nepal, extract ALL names of cities, towns, villages, districts, or specific junctions that the Highway touches.
        
        RULES:
        1. Return the result as a single, valid JSON array of strings. Example: ["Kathmandu", "Pokhara", "Hetauda"]
        2. Do not include any other text or explanation in your response. Only the JSON array.
        
        TEXT TO ANALYZE:
        ---
        {page_text}
        ---
        """
        
        response = model.generate_content(prompt)
        json_text = response.text.strip().lstrip("```json").rstrip("```")
        
        places = json.loads(json_text)
        return places
        
    except json.JSONDecodeError:
        print(f"    - Gemini returned invalid JSON. Response: {response.text}")
        return []
    except Exception as e:
        print(f"    - An error occurred with the Gemini API: {e}")
        return []