import os
import time
import requests
from duckduckgo_search import DDGS

# Target directory
output_dir = "/home/kali/.gemini/antigravity/brain/c8e871aa-8ab3-462e-a93c-062f81284342"
os.makedirs(output_dir, exist_ok=True)

# Define searches
searches = {
    "engine_mounting_batch7": "car engine mount replacement part white background",
    "suspension_bush_batch7": "car suspension polyurethane bush auto part white background",
    "engine_seal_batch7": "car engine oil seal auto part white background",
    "car_perfume_batch7": "car air freshener perfume auto accessory white background"
}

def download_image(url, filename, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://duckduckgo.com/'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"Downloading {filename} from {url} (Attempt {attempt+1})")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                filepath = os.path.join(output_dir, f"{filename}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Successfully downloaded: {filepath}")
                return True
            else:
                print(f"Failed to download: Status {response.status_code}, Content-Type {response.headers.get('Content-Type')}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
        time.sleep(2)
    return False

# Main execution
with DDGS() as ddgs:
    for filename, query in searches.items():
        print(f"\nSearching for: {query}")
        try:
            results = list(ddgs.images(query, max_results=5))
            success = False
            for result in results:
                image_url = result.get('image')
                if image_url:
                    if download_image(image_url, filename):
                        success = True
                        break
            if not success:
                print(f"Could not download any images for {filename}")
        except Exception as e:
            print(f"Search failed for {query}: {e}")
        time.sleep(2) # Be polite to the API
