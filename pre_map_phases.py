import json
import os

def pre_map_remaining_phases():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        new_image = None
        
        # IRONMONGERY (Phase 14)
        if category == 'LOCKS':
            if 'CYLINDER' in name:
                new_image = 'assets/images/products/hardware/door-lock-cylinder-v1.png'
            else:
                new_image = 'assets/images/products/hardware/mortice-lock-v1.png'
        elif category == 'HINGES':
            if 'HYDRAULIC' in name:
                new_image = 'assets/images/products/hardware/hydraulic-hinge-v1.png'
            else:
                new_image = 'assets/images/products/hardware/butt-hinge-v1.png'
        elif category == 'HANDLE':
            if 'DRAWER' in name:
                new_image = 'assets/images/products/hardware/drawer-handle-v1.png'
            else:
                new_image = 'assets/images/products/hardware/door-handle-lever-v1.png'
                
        # FASTENERS (Phase 15)
        elif category == 'SCREWS':
            if 'GYPSUM' in name or 'DRYWALL' in name:
                new_image = 'assets/images/products/hardware/drywall-screw-black-v1.png'
            elif 'WOOD' in name:
                new_image = 'assets/images/products/hardware/wood-screw-yellow-v1.png'
            else:
                new_image = 'assets/images/products/hardware/self-tapping-screw-v1.png'
        elif category == 'RIVETS':
            new_image = 'assets/images/products/hardware/pop-rivet-v1.png'
            
        # MESH & FENCING (Phase 16)
        elif category == 'KUKU NET':
            new_image = 'assets/images/products/hardware/chicken-wire-mesh-v1.png'
        elif category == 'WIRE MESH':
            new_image = 'assets/images/products/hardware/welded-wire-mesh-v1.png'
            
        if new_image and (not product.get('image') or 'placeholder' in product.get('image', '').lower() or 'hardware/' not in product.get('image', '')):
            product['image'] = new_image
            product['images'] = [new_image]
            count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Pre-mapped {count} products for remaining phases in products.json")

if __name__ == "__main__":
    pre_map_remaining_phases()
