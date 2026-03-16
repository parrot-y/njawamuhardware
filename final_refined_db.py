import json
import os

def final_refined_optimization():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    stats = {
        'categorized': 0,
        'mapped': 0
    }
    
    # CRYSTALLIZED KEYWORD MAP
    keyword_map = {
        'CEMENT': 'BUILDING MATERIALS',
        'CONCRETE': 'BUILDING MATERIALS',
        'FILLER': 'ADHESIVES',
        'BONDEX': 'ADHESIVES',
        'BODEX': 'ADHESIVES',
        'BOX PROFILE': 'IRON SHEETS',
        'CEILING NAILS': 'NAILS',
        'CHICKEN WIRE': 'KUKU NET',
        'CHAIN LINK': 'CHAIN LINKS',
        'HAMMER': 'TOOLS',
        'CHISEL': 'TOOLS',
        'WHEEL': 'TOOLS',
        'AXE': 'TOOLS',
        'LEVEL': 'TOOLS',
        'MEASURE': 'TOOLS',
        'SAW': 'TOOLS',
        'PLIER': 'TOOLS',
        'VALLEY': 'RIDGES',
        'SYPHON': 'WASTE FITTINGS',
        'AVS': 'ELECTRICALS',
        'WESTERN': 'ELECTRICALS',
        'LAMP': 'ELECTRICALS',
        'CABLE': 'ELECTRICALS',
        'VARNISH': 'PAINTS',
        'TURP': 'PAINTS',
        'PAINT': 'PAINTS'
    }
    
    # REFINED IMAGE MAPPING
    image_map = {
        'BUILDING MATERIALS': 'assets/images/products/hardware/black-sheet-v1.png', # Placeholder variant
        'ADHESIVES': 'assets/images/products/hardware/tools.jpg',
        'TOOLS': 'assets/images/products/hardware/tools.jpg',
        'KUKU NET': 'assets/images/products/hardware/chicken-wire-mesh-v1.png',
        'CHAIN LINKS': 'assets/images/products/hardware/chain-link-galvanized-v1.png'
    }

    generic_placeholders = ['tools.jpg', 'fasteners.jpg', 'plumbing.jpg', 'nails.jpg', 'electricals.jpg', 'paints.jpg', 'iron-sheets.jpg', 'plumbing.jpg']

    for product in products:
        name_upper = product['name'].upper()
        # Clean current category if it was assigned loosely in previous steps
        if product['category'] == 'UNCATEGORIZED' or product['category'] == 'PLUMBING':
            for kw, cat in keyword_map.items():
                if kw in name_upper:
                    product['category'] = cat
                    stats['categorized'] += 1
                    break
        
        # Mapping
        cat = product['category']
        if cat in image_map:
            current_image = product.get('image', '')
            is_generic = any(p in current_image for p in generic_placeholders)
            if not current_image or is_generic:
                product['image'] = image_map[cat]
                product['images'] = [image_map[cat]]
                stats['mapped'] += 1

    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Final Refined Optimization Complete:")
    print(f"- Categorized {stats['categorized']} products")
    print(f"- Mapped {stats['mapped']} products to target visuals")

if __name__ == "__main__":
    final_refined_optimization()
