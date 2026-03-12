import urllib.request
import json
import os
import ssl

output_dir = "/home/kali/.gemini/antigravity/brain/c8e871aa-8ab3-462e-a93c-062f81284342"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req_headers = {'User-Agent': 'Mozilla/5.0 GMA Spares Bot'}

items = {
    "engine_mount_batch7": "Engine_mount_from_Honda_Civic.jpg",
    "engine_seal_batch7": "Oil_seal.jpg",
    "car_perfume_batch7": "Car_air_freshener_Tree.jpg"
}

def get_image_url(filename):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{filename}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            pages = data['query']['pages']
            for page_id in pages:
                return pages[page_id]['imageinfo'][0]['url']
    except Exception as e:
        print(f"Failed to get URL for {filename}: {e}")
    return None

def download_image(url, out_name):
    if not url: return
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            out_path = os.path.join(output_dir, f"{out_name}.jpg")
            with open(out_path, 'wb') as f:
                f.write(response.read())
            print(f"Downloaded: {out_name}")
    except Exception as e:
        print(f"Failed to download {out_name}: {e}")

for name, wiki_file in items.items():
    url = get_image_url(wiki_file)
    download_image(url, name)
