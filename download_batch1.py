import requests
import os

images = {
    "super-glue-bottle-v1.png": "https://shop4electrical.co.uk/670983-large_default/industrial-grade-super-glue-50g-bottle.jpg",
    "paint-brush-set-v1.png": "https://decoupagenapkins.com/cdn/shop/products/Polyvine-Synthetic-Paint-Brush-2-sizes.jpg",
    "masonry-trowel-v1.png": "https://www.beorol.com/684-large_default/bricklaying-trowel-wooden-handle-square-shape-160mm.jpg",
    "garden-pruning-shear-v1.png": "https://assets.manufactum.de/p/087/087459/87459_01.jpg/bahco-garden-shears-ergonomic.jpg",
    "shelf-bracket-metal-v1.png": "https://cascadeironco.com/cdn/shop/products/L-bracket-metal-shelf-support-heavy-duty-black-white-gray-raw-steel.jpg"
}

target_dir = "src/assets/images/products/hardware/"
os.makedirs(target_dir, exist_ok=True)

for name, url in images.items():
    try:
        print(f"Downloading {name} from {url}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(os.path.join(target_dir, name), 'wb') as f:
                f.write(response.content)
            print(f"Successfully saved {name}")
        else:
            print(f"Failed to download {name}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {name}: {e}")
