import json
import os

def finalize_phases_13_14():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        new_image = None
        
        # Phase 13: SANITARYWARE
        if category == 'SINKS':
            if 'DOUBLE' in name:
                new_image = 'assets/images/products/hardware/kitchen-sink-double-v1.png'
            else:
                new_image = 'assets/images/products/hardware/kitchen-sink-single-v1.png'
        elif category == 'TOILET':
            if 'ASIAN' in name:
                new_image = 'assets/images/products/hardware/toilet-asian-step-v1.png'
            elif 'COMPLETE' in name or 'P-TRAP' in name or 'S-TRAP' in name:
                new_image = 'assets/images/products/hardware/toilet-set-complete-v1.png'
            elif 'BASIN' in name or 'H.W.B' in name:
                new_image = 'assets/images/products/hardware/wash-basin-pedestal-v1.png'
            elif 'URINAL' in name:
                new_image = 'assets/images/products/hardware/urinal-bowl-v1.png'
        
        # Phase 14: IRONMONGERY
        elif category == 'LOCKS':
            if 'CYLINDER' in name:
                new_image = 'assets/images/products/hardware/door-lock-cylinder-v1.png'
            else:
                new_image = 'assets/images/products/hardware/door-lock-mortice-v1.png'
        elif category == 'HINGES':
            new_image = 'assets/images/products/hardware/butt-hinge-steel-v1.png'
        elif category == 'HANDLE':
            if 'DRAWER' in name:
                new_image = 'assets/images/products/hardware/drawer-handle-v1.png'
            else:
                new_image = 'assets/images/products/hardware/door-handle-lever-v1.png'
                
        if new_image:
            product['image'] = new_image
            product['images'] = [new_image]
            count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Finalized {count} products for Phases 13 & 14.")

if __name__ == "__main__":
    finalize_phases_13_14()
