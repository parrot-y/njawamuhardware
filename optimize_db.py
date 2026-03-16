import json
import os

def optimize_database():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    stats = {
        'unified': 0,
        'categorized': 0,
        'standardized': 0
    }
    
    # Mapping for category unification
    unify_map = {
        'PAINT': 'PAINTS',
        'LOCK': 'LOCKS',
        'CHICKEN WIRE': 'KUKU NET'
    }
    
    # Mapping for auto-categorization based on keywords
    keyword_map = {
        'HINGE': 'HINGES',
        'HANDLE': 'HANDLE', # Existing category
        'SCREW': 'SCREWS',
        'RIVET': 'RIVETS',
        'VALVE': 'PPR FITTINGS', # Often related
        'COUPLING': 'PPR FITTINGS', # or HDPE
        'ADAPTER': 'HDPE FITTINGS',
        'ELBOW': 'PPR FITTINGS',
        'TEE': 'PPR FITTINGS',
        'UNION': 'PPR FITTINGS',
        'CABLE': 'ELECTRICALS',
        'SWITCH': 'ELECTRICALS',
        'SOCKET': 'ELECTRICALS',
        'BULB': 'ELECTRICALS',
        'BREAKER': 'ELECTRICALS',
        'TRAP': 'WASTE FITTINGS',
        'BATH': 'TOILET', # Usually grouped
        'BASIN': 'TOILET',
        'TILE': 'TILES', # I'll create this category
        'BRUSH': 'PAINTS' # Painting accessories
    }
    
    for product in products:
        name_upper = product['name'].upper()
        category = product['category']
        
        # 1. Unify categories
        if category in unify_map:
            product['category'] = unify_map[category]
            stats['unified'] += 1
            category = product['category'] # Update for next steps
            
        # 2. Auto-categorize UNCATEGORIZED
        if category == 'UNCATEGORIZED':
            for kw, cat in keyword_map.items():
                if kw in name_upper:
                    product['category'] = cat
                    stats['categorized'] += 1
                    category = cat # Update for next steps
                    break
        
        # 3. Standardize image paths (ensure no double slashes, correct prefix)
        if 'image' in product and product['image']:
            # Fix common path issues
            path = product['image'].replace('//', '/').lstrip('/')
            if not path.startswith('assets/'):
                path = 'assets/' + path if not path.startswith('src/') else path.replace('src/', '')
            
            if product['image'] != path:
                product['image'] = path
                product['images'] = [path]
                stats['standardized'] += 1
        
        # 4. Basic SEO Description reinforcement
        if not product.get('description') or 'Contact NJAWAMU' in product['description']:
            brand = product.get('brand', 'NJAWAMU')
            cat_name = product['category'].replace('_', ' ').capitalize()
            product['description'] = f"High-quality {product['name']} from {brand}. Perfect for professional and DIY {cat_name} projects. Available at NJAWAMU Hardware."

    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Optimization Complete:")
    print(f"- Unified categories for {stats['unified']} products")
    print(f"- Categorized {stats['categorized']} previously unknown products")
    print(f"- Standardized paths for {stats['standardized']} products")

if __name__ == "__main__":
    optimize_database()
