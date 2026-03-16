import json
import os

def finalize_phase_16_partial():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        new_image = None
        
        # Phase 16: MESH & FENCING
        if category == 'KUKU NET' or 'CHICKEN' in name:
            new_image = 'assets/images/products/hardware/chicken-wire-mesh-v1.png'
        elif category == 'WIRE MESH':
            new_image = 'assets/images/products/hardware/welded-wire-mesh-v1.png'
            
        if new_image:
            product['image'] = new_image
            product['images'] = [new_image]
            count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Finalized {count} products for Phase 16 (Partial).")

if __name__ == "__main__":
    finalize_phase_16_partial()
