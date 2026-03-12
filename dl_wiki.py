import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req_headers = {'User-Agent': 'Mozilla/5.0'}

images = {
    "engine_mount_batch7.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/23/Engine_mount_from_Honda_Civic.jpg",
    "engine_seal_batch7.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Oil_seal.jpg/1024px-Oil_seal.jpg",
    "car_perfume_batch7.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Wunder-Baum_2_%28Little_Trees%29.jpg/800px-Wunder-Baum_2_%28Little_Trees%29.jpg"
}

output_dir = "/home/kali/.gemini/antigravity/brain/c8e871aa-8ab3-462e-a93c-062f81284342"

for name, url in images.items():
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            with open(f"{output_dir}/{name}", 'wb') as f:
                f.write(response.read())
            print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed {name}: {e}")
