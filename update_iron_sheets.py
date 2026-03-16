import json
import os

def update_iron_sheet_images():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        new_image = None
        
        # IRON SHEETS
        if category == 'IRON SHEETS':
            if 'BOX PROFILE' in name:
                if 'BLUE' in name:
                    new_image = 'assets/images/products/hardware/iron-sheet-box-profile-blue-v1.png'
                elif 'GREEN' in name:
                    new_image = 'assets/images/products/hardware/iron-sheet-box-profile-green-v1.png'
                else:
                    # Default box profile to maroon as it's common
                    new_image = 'assets/images/products/hardware/iron-sheet-box-profile-maroon-v1.png'
            elif 'CORRUGA' in name or 'ORDINARY' in name:
                new_image = 'assets/images/products/hardware/iron-sheet-corrugated-v1.png'
            elif 'PLAIN' in name or 'GALV' in name or 'SHEETS' in name:
                new_image = 'assets/images/products/hardware/iron-sheet-plain-galv-v1.png'
            else:
                new_image = 'assets/images/products/hardware/iron-sheet-corrugated-v1.png' # Fallback
        
        # RIDGES
        elif category == 'RIDGES':
            new_image = 'assets/images/products/hardware/roof-ridge-v1.png'
                
        if new_image:
            product['image'] = new_image
            product['images'] = [new_image]
            count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Updated {count} iron sheet products in products.json")

if __name__ == "__main__":
    update_iron_sheet_images()
