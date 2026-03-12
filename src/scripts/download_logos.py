import urllib.request
import urllib.parse
import json
import os
import time

brands = [
    ("Toyota logo", "toyota-logo.png", "brands"),
    ("Nissan logo", "nissan-logo.png", "brands"),
    ("Honda logo", "honda-logo.png", "brands"),
    ("Mazda logo", "mazda-logo.png", "brands"),
    ("BMW logo", "bmw-logo.png", "brands"),
    ("Subaru logo", "subaru-logo.png", "brands")
]

def search_wikimedia(query):
    # Try searching for exact logo pages or getting images from the main brand page
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={urllib.parse.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 GracefulMotionApp/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            pages = data['query']['pages']
            for page_id in pages:
                if 'original' in pages[page_id]:
                    img_url = pages[page_id]['original']['source']
                    if img_url.lower().endswith(('.png', '.svg', '.jpg', '.jpeg')):
                        return img_url
    except Exception as e:
        print(f"Error searching {query}: {e}")
    return None

def download_image(url, filepath):
    headers = {"User-Agent": "Mozilla/5.0 GracefulMotionApp/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

base_dir = "/home/kali/Documents/graceful-motion-autospares/src/assets/images"

for query, filename, category_dir in brands:
    print(f"Searching for: {query}")
    img_url = search_wikimedia(query)
    
    if img_url:
        print(f"Found URL: {img_url}")
        target_dir = os.path.join(base_dir, category_dir)
        os.makedirs(target_dir, exist_ok=True)
        filepath = os.path.join(target_dir, filename)
        
        if download_image(img_url, filepath):
            print(f"Downloaded -> {filepath}")
        else:
            print(f"Failed to download -> {filepath}")
    else:
        print("No image found.")
    
    time.sleep(1)
