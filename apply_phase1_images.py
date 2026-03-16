import json
import os

def apply_images():
    data_path = 'src/assets/data/products.json'
    js_path = 'src/scripts/product-data.js'
    
    # Absolute paths just to be safe in the caller script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'src/assets/data/products.json')
    js_path = os.path.join(base_dir, 'src/scripts/product-data.js')

    if not os.path.exists(data_path):
         print(f"Error: {data_path} not found")
         return

    with open(data_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    mapping = {
        "BARBED WIRE": "assets/images/products/hardware/barbed-wire.jpg",
        "IRON SHEETS": "assets/images/products/hardware/iron-sheets.jpg",
        "CHAIN LINKS": "assets/images/products/hardware/chain-link.jpg",
        "CHICKEN WIRE": "assets/images/products/hardware/chicken-wire.jpg",
        "RIDGES": "assets/images/products/hardware/iron-sheets.jpg",
        "BLACK SHEET": "assets/images/products/hardware/iron-sheets.jpg"
    }

    updated_count = 0
    for p in products:
        cat = p.get('category', '').upper()
        if cat in mapping:
            p['image'] = mapping[cat]
            p['images'] = [mapping[cat]]
            updated_count += 1

    # Write back to JSON
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)

    # Also update the JS file
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write("/**\n * NJAWAMU Hardware — Product Database\n * Extracted from PDF\n */\n\nwindow.RenovyteProducts = ")
        json.dump(products, f, indent=2)
        f.write(";")

    print(f"Updated {updated_count} products with Phase 1 images.")

if __name__ == "__main__":
    apply_images()
