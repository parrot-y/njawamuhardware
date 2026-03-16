import json
import os

def finalize_phase_15():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        new_image = None
        
        # Phase 15: FASTENERS
        if category == 'SCREWS':
            if 'GYPSUM' in name or 'DRYWALL' in name or 'MDF' in name:
                new_image = 'assets/images/products/hardware/drywall-screw-black-v1.png'
            elif 'WOOD' in name or 'CHIPBOARD' in name:
                new_image = 'assets/images/products/hardware/wood-screw-yellow-v1.png'
            else:
                new_image = 'assets/images/products/hardware/self-tapping-screw-v1.png'
        elif category == 'RIVETS':
            new_image = 'assets/images/products/hardware/pop-rivet-v1.png'
                
        if new_image:
            product['image'] = new_image
            product['images'] = [new_image]
            count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Finalized {count} products for Phase 15.")

if __name__ == "__main__":
    finalize_phase_15()
