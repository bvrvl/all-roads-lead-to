import requests
from bs4 import BeautifulSoup
from google import genai
import os
import json

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_page_text(highway_url):
    """
    Scrapes the highway page, cleans out boilerplate HTML elements, 
    and then returns the clean text of the main article body.
    """
    try:
        response = requests.get(highway_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Isolate the main content area of the page
        content_div = soup.find(id='mw-content-text')
        
        if content_div:
            # Before extracting text, we find and destroy unwanted elements.
            # .decompose() removes a tag and all its children.
            
            # Remove all navigation boxes (the main source of noise)
            for navbox in content_div.find_all('div', class_='navbox'):
                navbox.decompose()
                
            # Remove reference lists
            for reflist in content_div.find_all('div', class_='reflist'):
                reflist.decompose()
                
            # Remove "stub" message boxes at the bottom
            for stub in content_div.find_all(class_='asbox'):
                stub.decompose()

            # Remove the little "[edit]" links next to section headers
            for edit_section in content_div.find_all('span', class_='mw-editsection'):
                edit_section.decompose()
            
            return content_div.get_text(separator=' ', strip=True)
            
        return ""
        
    except requests.exceptions.RequestException as e:
        print(f"    - Could not scrape {highway_url}. Error: {e}")
        return ""

def extract_places_with_gemini(page_text):
    """
    Uses the Gemini API to extract Nepalese place names from text.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("    - ERROR: GEMINI_API_KEY not found in environment.")
            return []

        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        From the following text about a specific highway in Nepal, extract ALL names of cities, towns, villages, districts, or specific junctions that it touches.
        
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
        print(f"    - An error occurred with the Gemini API: {e}")
        return []