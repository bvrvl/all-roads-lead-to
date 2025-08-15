import requests
from bs4 import BeautifulSoup
from google import genai
import os
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
    This version uses the genai.Client() method.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("    - ERROR: GEMINI_API_KEY not found in environment.")
            return []

        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        From the following text about a highway in Nepal, extract ALL names of cities, towns, villages, districts, or specific junctions.
        
        RULES:
        1. Return the result as a single, valid JSON array of strings. Example: ["Kathmandu", "Pokhara", "Hetauda"]
        2. If no places are found, return an empty array [].
        3. Do not include any other text, explanation, or markdown formatting in your response. Only the JSON array.
        
        TEXT TO ANALYZE:
        ---
        {page_text}
        ---
        """
        
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )
        
        json_text = response.text.strip().lstrip("```json").rstrip("```")
        
        places = json.loads(json_text)
        return places
        
    except json.JSONDecodeError:
        print(f"    - Gemini returned invalid JSON. Response: {response.text}")
        return []
    except Exception as e:
        # This will catch other API errors like authentication, etc.
        print(f"    - An error occurred with the Gemini API: {e}")
        return []