import json
import re

def extract_placeholder_products():
    with open('src/scripts/product-data.js', 'r') as f:
        content = f.read()

    # Extract the JSON array from the JS file
    match = re.search(r'window\.NJAWAMUProducts = (\[.*\]);', content, re.DOTALL)
    if not match:
        print("Could not find product data.")
        return

    products = json.loads(match.group(1))
    
    # Generic placeholders found in the codebase
    placeholders = [
        'assets/images/products/hardware/pvc-pipe-grey-v1.png',
        'assets/images/products/hardware/pvc-rainwater-gutter-v1.png',
        'assets/images/products/hardware/placeholder.png',
        'assets/images/hero/hero-1.webp'
    ]
    
    missing = []
    for p in products:
        img = p.get('image', '')
        if not img or any(ph in img for ph in placeholders):
            missing.append(f"{p['id']} | {p['name']} | {p['category']}")

    with open('products_missing_images.txt', 'w') as f:
        f.write('\n'.join(missing))
    
    print(f"Extraction complete. Found {len(missing)} products with missing/placeholder images.")

if __name__ == "__main__":
    extract_placeholder_products()
