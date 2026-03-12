import urllib.request
import urllib.parse
import re
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

searches = {
    "engine_mount_batch7.jpg": "auto part engine mount rubber isolated on white background",
    "engine_seal_batch7.jpg": "auto part engine oil seal black rubber white background",
    "car_perfume_batch7.jpg": "car air freshener hanging auto accessory white background"
}

output_dir = "/home/kali/.gemini/antigravity/brain/c8e871aa-8ab3-462e-a93c-062f81284342"

for filename, query in searches.items():
    print(f"Searching: {query}")
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
            
            # Find the first image link (usually pointing to an external site or a thumbnail proxy)
            img_matches = re.findall(r'<img class="tile--img__img"\s+src="([^"]+)"', html)
            if img_matches:
                img_url = img_matches[0]
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                    
                print(f"Found image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, context=ctx) as img_resp:
                    out_path = os.path.join(output_dir, filename)
                    with open(out_path, 'wb') as f:
                        f.write(img_resp.read())
                    print(f"Successfully downloaded {filename}")
            else:
                print(f"No images found for {filename}")
    except Exception as e:
        print(f"Error for {filename}: {e}")
