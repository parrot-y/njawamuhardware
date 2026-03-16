import json
import os

def mega_categorization_and_premapping():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    stats = {
        'categorized': 0,
        'mapped': 0
    }
    
    # 1. ADVANCED KEYWORD MAP
    # Format: Keyword -> Category
    adv_keyword_map = {
        'ANGLE LINE': 'METAL SECTIONS',
        'VARNISH': 'PAINTS',
        'TURPENTINE': 'PAINTS',
        'GLOSS': 'PAINTS',
        'MATT': 'PAINTS',
        'EMULSION': 'PAINTS',
        'BITUMINO': 'PAINTS',
        'SPIRIT': 'PAINTS',
        'SHOWER': 'TOILET', # For now group bathroom items
        'BID': 'TOILET',
        'ARALDITE': 'ADHESIVES',
        'ASMACO': 'ADHESIVES',
        'AXE': 'TOOLS',
        'TRAY': 'TOOLS',
        'BALL CATCH': 'IRONMONGERY',
        'BARBED WIRE': 'BARBED WIRE',
        'BED BOLT': 'BOLTS',
        'BINDING WIRE': 'MESH & FENCING',
        'BRAC': 'BRACKETS',
        'PAD BOLT': 'LOCKS',
        'BLACK PIPE': 'PIPES',
        'BLACK SHEET': 'BLACK SHEET',
        'PADLOCK': 'PADLOCKS',
        'CURTAIN': 'DECORATIVE',
        'MDF': 'BOARDS',
        'PLYWOOD': 'BOARDS',
        'GYPSUM': 'BOARDS',
        'BLOCK': 'BOARDS',
        'SPOUT': 'TAPS',
        'TAP': 'TAPS',
        'VALVE': 'PPR FITTINGS',
        'BALL VALVE': 'PPR FITTINGS',
        'TANK': 'PLUMBING',
        'BATH': 'TOILET',
        'TRAP': 'WASTE FITTINGS',
        'BOTTLE TRAP': 'WASTE FITTINGS',
        'STAY': 'WINDOW FASTENERS',
        'FASTENER': 'WINDOW FASTENERS'
    }
    
    # 2. TARGET IMAGE MAP (Phase 1-16)
    target_image_map = {
        'METAL SECTIONS': 'assets/images/products/hardware/black-tube-v1.png', # Placeholder variant
        'ADHESIVES': 'assets/images/products/hardware/tools.jpg',
        'TOOLS': 'assets/images/products/hardware/tools.jpg',
        'BOLTS': 'assets/images/products/hardware/roofing-bolts-v1.png',
        'BARBED WIRE': 'assets/images/products/hardware/barbed-wire-v1.png',
        'BLACK SHEET': 'assets/images/products/hardware/black-sheet-v1.png',
        'BOARDS': 'assets/images/products/hardware/mdf-boards-v1.png',
        'MESH & FENCING': 'assets/images/products/hardware/chain-link-galvanized-v1.png'
    }

    generic_placeholders = ['tools.jpg', 'fasteners.jpg', 'plumbing.jpg', 'nails.jpg', 'electricals.jpg', 'paints.jpg', 'iron-sheets.jpg']

    for product in products:
        name_upper = product['name'].upper()
        category = product['category']
        
        # Auto-categorize
        if category == 'UNCATEGORIZED':
            for kw, cat in adv_keyword_map.items():
                if kw in name_upper:
                    product['category'] = cat
                    stats['categorized'] += 1
                    category = cat
                    break
        
        # Pre-mapping
        if category in target_image_map:
            current_image = product.get('image', '')
            is_generic = any(p in current_image for p in generic_placeholders)
            if not current_image or is_generic or 'placeholder' in current_image:
                product['image'] = target_image_map[category]
                product['images'] = [target_image_map[category]]
                stats['mapped'] += 1

    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Mega Systematic Optimization Complete:")
    print(f"- Categorized {stats['categorized']} products")
    print(f"- Mapped {stats['mapped']} products to target visuals")

if __name__ == "__main__":
    mega_categorization_and_premapping()
