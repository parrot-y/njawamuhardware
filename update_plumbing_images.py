import json
import os

def update_plumbing_images():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        
        new_image = None
        
        # TAPS
        if category == 'TAPS':
            if 'PEGLER' in name or 'BIB' in name or 'GARDEN' in name:
                new_image = 'assets/images/products/hardware/brass-bib-tap-v1.png'
            elif 'COBRA' in name or 'SINK' in name or 'BASIN' in name or 'BIP' in name:
                new_image = 'assets/images/products/hardware/chrome-sink-tap-v1.png'
            else:
                new_image = 'assets/images/products/hardware/chrome-sink-tap-v1.png' # Fallback
        
        # PIPES
        elif category in ['PIPES', 'UPVC PRESSURE PIPE']:
            if 'PPR' in name:
                new_image = 'assets/images/products/hardware/ppr-pipe-green-v1.png'
            elif 'HDPE' in name:
                new_image = 'assets/images/products/hardware/hdpe-pipe-black-v1.png'
            elif 'PVC' in name or 'PRESSURE' in name:
                new_image = 'assets/images/products/hardware/pvc-pipe-grey-v1.png'
        
        # FITTINGS
        elif category == 'HDPE FITTINGS':
            if 'TEE' in name:
                new_image = 'assets/images/products/hardware/hdpe-fitting-tee-v1.png'
            elif 'ELBOW' in name:
                new_image = 'assets/images/products/hardware/hdpe-fitting-elbow-v1.png'
            elif 'COUPLING' in name or 'ADAPTER' in name:
                new_image = 'assets/images/products/hardware/hdpe-fitting-coupling-v1.png'
            else:
                new_image = 'assets/images/products/hardware/hdpe-fitting-tee-v1.png' # Fallback
                
        elif category == 'PPR FITTINGS':
            new_image = 'assets/images/products/hardware/ppr-fitting-socket-v1.png'
            
        elif category == 'WASTE FITTINGS':
            if 'TRAP' in name:
                new_image = 'assets/images/products/hardware/waste-fitting-bottle-trap-v1.png'
            else:
                new_image = 'assets/images/products/hardware/waste-fitting-bottle-trap-v1.png' # Fallback
                
        if new_image:
            product['image'] = new_image
            product['images'] = [new_image]
            count += 1
            
    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Updated {count} plumbing products in products.json")

if __name__ == "__main__":
    update_plumbing_images()
