import json
import os

def update_sanitaryware_images():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        new_image = None
        
        # SINKS
        if category == 'SINKS':
            if 'DOUBLE' in name:
                new_image = 'assets/images/products/hardware/kitchen-sink-double-v1.png'
            else:
                new_image = 'assets/images/products/hardware/kitchen-sink-single-v1.png'
        
        # TOILET
        elif category == 'TOILET':
            if 'ASIAN' in name:
                new_image = 'assets/images/products/hardware/toilet-asian-step-v1.png'
            elif 'COMPLETE' in name or 'TOILET' in name:
                new_image = 'assets/images/products/hardware/toilet-set-complete-v1.png'
            elif 'BASIN' in name or 'H.W.B' in name or 'WASH' in name:
                new_image = 'assets/images/products/hardware/wash-basin-pedestal-v1.png'
            elif 'URINAL' in name:
                new_image = 'assets/images/products/hardware/urinal-bowl-v1.png'
            else:
                new_image = 'assets/images/products/hardware/toilet-set-complete-v1.png' # Fallback
                
        if new_image:
            product['image'] = new_image
            product['images'] = [new_image]
            count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Updated {count} sanitaryware products in products.json")

if __name__ == "__main__":
    update_sanitaryware_images()
