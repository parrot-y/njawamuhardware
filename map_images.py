import json
import os
import re

def map_images():
    data_path = 'src/assets/data/products.json'
    js_path = 'src/scripts/product-data.js'
    img_root = 'src/assets/images/products/'
    
    with open(data_path, 'r') as f:
        products = json.load(f)
        
    # Get all non-placeholder images
    images = []
    for root, dirs, files in os.walk(img_root):
        for file in files:
            if 'placeholder' not in file.lower() and file.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                full_path = os.path.join(root, file)
                # Convert to web-relative path
                rel_path = full_path.replace('src/', '')
                images.append({
                    'path': rel_path,
                    'name': os.path.splitext(file)[0].lower().replace('-v1', '').replace('-', ' ')
                })
    
    print(f"Found {len(images)} unique images to map.")
    
    match_count = 0
    for p in products:
        p_name = p['name'].lower()
        best_match = None
        
        # 1. Exact or near-exact match
        for img in images:
            # If the image name is a significant part of the product name
            if img['name'] in p_name and len(img['name']) > 3:
                best_match = img['path']
                break
        
        # 2. Category matching as fallback (only if we want to show category images)
        # We'll skip this for now to keep it specific as per user's likely intent.
        
        if best_match:
            p['image'] = best_match
            p['images'] = [best_match]
            match_count += 1
            
    print(f"Mapped {match_count} products out of {len(products)}.")
    
    # Save results
    with open(data_path, 'w') as f:
        json.dump(products, f, indent=2)
        
    js_content = f"/**\n * Official NJAWAMU Hardware Catalog - Synchronized with Images\n * Total Count: {len(products)}\n */\n\nwindow.NJAWAMUProducts = {json.dumps(products, indent=2)};"
    with open(js_path, 'w') as f:
        f.write(js_content)

if __name__ == "__main__":
    map_images()
