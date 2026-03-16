import requests
import os

images = {
    "super-glue-bottle-v1.jpg": "https://shop4electrical.co.uk/670983-large_default/industrial-grade-super-glue-50g-bottle.jpg",
    "paint-brush-set-v1.jpg": "https://decoupagenapkins.com/cdn/shop/products/Polyvine-Synthetic-Paint-Brush-2-sizes.jpg",
    "masonry-trowel-v1.jpg": "https://www.beorol.com/684-large_default/bricklaying-trowel-wooden-handle-square-shape-160mm.jpg",
    "garden-pruning-shear-v1.jpg": "https://assets.manufactum.de/p/162/162608/162608_01.jpg/garden-shears-ergonomic.jpg",
    "shelf-bracket-metal-v1.jpg": "https://cascadeironco.com/cdn/shop/products/L-bracket-metal-shelf-support-heavy-duty-black-white-gray-raw-steel.jpg",
    "silicone-sealant-v1.jpg": "https://www.homeflairdecor.co.uk/images/multi-purpose-silicone-300ml-cartridge-white-p1278-1389_image.jpg",
    "wood-varnish-can-v1.jpg": "https://www.beorol.com/3960-large_default/wood-varnish-gloss-750ml.jpg",
    "mineral-spirits-bottle-v1.jpg": "https://www.vlsdistributors.co.za/wp-content/uploads/2021/04/Mineral-Spirits-Thinners-Bottle.jpg",
    "wall-plugs-set-v1.jpg": "https://www.plasplugs.com/wp-content/uploads/2016/10/Assorted-Wall-Plugs.png",
    "curtain-rod-set-v1.jpg": "https://www.kirsch.com/wp-content/uploads/2019/10/Designer-Metals-Curtain-Rod.jpg",
    "tile-grout-pack-v1.jpg": "https://www.tilefixdirect.com/images/products/Mapei-Ultracolor-Plus-Grout-Bag.jpg",
    "sweeping-broom-v1.jpg": "https://www.hillbrush.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/b/0/b004_1.jpg",
    "gas-spring-v1.jpg": "https://www.gas-spring.shop/wp-content/uploads/2017/01/gas-spring-industrial.jpg",
    "rawl-bolt-sleeve-v1.jpg": "https://www.fixfast.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/s/l/sleeve-anchor-bolt.jpg",
    "pipe-end-cap-v1.jpg": "https://www.pvc-fittings.pro/wp-content/uploads/2018/06/PVC-End-Cap.jpg"
}

target_dir = "src/assets/images/products/hardware/"
os.makedirs(target_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for name, url in images.items():
    try:
        print(f"Downloading {name} from {url}...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            with open(os.path.join(target_dir, name), 'wb') as f:
                f.write(response.content)
            print(f"Successfully saved {name}")
        else:
            print(f"Failed to download {name}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {name}: {e}")

print("\n--- Download Summary ---")
for name in images.keys():
    if os.path.exists(os.path.join(target_dir, name)):
        print(f"[OK] {name}")
    else:
        print(f"[FAILED] {name}")
