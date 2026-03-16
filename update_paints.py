import json
import os

def update_paint_images():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        if category in ['PAINT', 'PAINTS']:
            new_image = None
            
            # Gloss/Standard cans
            if 'GLO' in name or 'GLOSS' in name or 'STANDARD' in name:
                new_image = 'assets/images/products/hardware/paint-can-gloss-v1.png'
            # Fallback to existing paints.jpg if quota hit for specialized buckets
            else:
                new_image = 'assets/images/products/hardware/paints.jpg'
                
            if new_image:
                product['image'] = new_image
                product['images'] = [new_image]
                count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Updated {count} paint products in products.json")

if __name__ == "__main__":
    update_paint_images()
