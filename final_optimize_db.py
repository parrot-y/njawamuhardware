import json
import os

def final_systematic_optimization():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    initial_count = len(products)
    
    # 1. DELETE JUNK DATA
    # Remove products named "—" or "PRODUCT NAME" or "BRAND"
    junk_names = ["—", "PRODUCT NAME", "BRAND"]
    products = [p for p in products if p['name'].upper() not in junk_names and len(p['name']) > 1]
    
    deleted_count = initial_count - len(products)
    
    stats = {
        'categorized': 0,
        'mapped': 0
    }
    
    # 2. EXPANDED KEYWORD MAP
    keyword_map = {
        'WINDOW': 'WINDOW FASTENERS',
        'VALVE': 'PPR FITTINGS',
        'FLEX TUBE': 'TUBES',
        'FLEXIBLE': 'TUBES',
        'STAND PIPE': 'PIPES',
        'STOP': 'TAPS',
        'WASTE': 'WASTE FITTINGS',
        'STRAINER': 'WASTE FITTINGS',
        'CONNECTOR': 'PPR FITTINGS',
        'POP UP': 'WASTE FITTINGS',
        'DRAIN': 'WASTE FITTINGS',
        'ELBOW': 'PPR FITTINGS',
        'TEE': 'PPR FITTINGS',
        'UNION': 'PPR FITTINGS',
        'SOCKET': 'PPR FITTINGS',
        'NIPPLE': 'PPR FITTINGS',
        'BUSH': 'PPR FITTINGS',
        'PLUG': 'PPR FITTINGS',
        'CAP': 'PPR FITTINGS',
        'ADAPTER': 'HDPE FITTINGS',
        'COUPLING': 'HDPE FITTINGS'
    }
    
    # 3. MAPPING FOR PRE-MAPPED IMAGES (Aggressive)
    pre_map = {
        'LOCKS': 'assets/images/products/hardware/mortice-lock-v1.png',
        'HINGES': 'assets/images/products/hardware/butt-hinge-v1.png',
        'HANDLE': 'assets/images/products/hardware/door-handle-lever-v1.png',
        'SCREWS': 'assets/images/products/hardware/self-tapping-screw-v1.png',
        'RIVETS': 'assets/images/products/hardware/pop-rivet-v1.png',
        'KUKU NET': 'assets/images/products/hardware/chicken-wire-mesh-v1.png',
        'WIRE MESH': 'assets/images/products/hardware/welded-wire-mesh-v1.png',
        'WINDOW FASTENERS': 'assets/images/products/hardware/tower-bolt-v1.png', # Temporary but closer
        'WASTE FITTINGS': 'assets/images/products/hardware/waste-fitting-bottle-trap-v1.png'
    }
    
    generic_placeholders = ['tools.jpg', 'fasteners.jpg', 'plumbing.jpg', 'nails.jpg', 'electricals.jpg']

    for product in products:
        name_upper = product['name'].upper()
        category = product['category']
        
        # Auto-categorize
        if category == 'UNCATEGORIZED':
            for kw, cat in keyword_map.items():
                if kw in name_upper:
                    product['category'] = cat
                    stats['categorized'] += 1
                    category = cat
                    break
        
        # Aggressive Pre-mapping
        if category in pre_map:
            current_image = product.get('image', '')
            # Replace if it's generic OR if it's one of our category placeholders
            is_generic = any(p in current_image for p in generic_placeholders)
            if not current_image or is_generic or 'placeholder' in current_image:
                product['image'] = pre_map[category]
                product['images'] = [pre_map[category]]
                stats['mapped'] += 1

    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Final Systematic Optimization Complete:")
    print(f"- Deleted {deleted_count} junk products")
    print(f"- Categorized {stats['categorized']} products")
    print(f"- Aggressively mapped {stats['mapped']} products to specific target visual paths")

if __name__ == "__main__":
    final_systematic_optimization()
