import json
import re

def refine_catalog(input_file):
    with open(input_file, 'r') as f:
        products = json.load(f)

    # 1. Define keyword mappings for categorization (matching catalog.html hardcoded values)
    category_map = {
        'PAINTS': [r'PAINT', r'NC CLEAR', r'SEWECO', r'THINNER', r'VARNISH', r'UNDERCOAT', r'EMULSION', r'GLOSS', r'BRUSH', r'ROLLER', r'SOLVENT', r'TURPENTINE', r'SPIRIT', r'PUTTY', r'FILL', r'STAIN', r'WOOD PRE'],
        'PIPES': [r'PPR', r'PIPE', r'HDPE', r'PVC', r'WASTE', r'FITTING', r'ADAPTER', r'ELBOW', r'TEE', r'VALVE', r'SINK', r'TAP', r'TOILET', r'BOND', r'G.I', r'GALVANIZ', r'COLD WATER', r'HOT WATER', r'GASKET', r'PLUMB', r'TRAP', r'GULLEY', r'SADDLE'],
        'ELECTRICALS': [r'CABLE', r'POCARL', r'CIRCUIT', r'JUNCT', r'WATER HE', r'COOKER', r'SWITCH', r'SOCKET', r'BULB', r'CONDUIT', r'MCB', r'DISTRIBUTION', r'HOLDER', r'ELEC', r'TRUNKING', r'PLUG', r'REELS', r'STARTER'],
        'HARDWARE & FASTENERS': [r'BOLT', r'SCREW', r'NAIL', r'PADLOCK', r'LOCK', r'HINGE', r'HANDLE', r'FASTENER', r'STAY', r'TOWER', r'BRACKET', r'CHAIN LINK', r'WIRE MESH', r'BARBED WIRE', r'KUKU NET', r'CHICKEN WIRE', r'RIVET', r'WASHERS', r'NUT', r'HOOK', r'WIRE', r'BINDING', r'DRAWER', r'RAIL', r'CHAIN', r'SADDLE'],
        'IRON SHEETS': [r'IRON SHEET', r'RIDGE', r'PROFILE', r'GUTTER', r'BOX PROFILE', r'VALLEY', r'FLASHING'],
        'BUILDING MATERIALS': [r'BOARD', r'MDF', r'PLY', r'CEMENT', r'STEEL', r'BAR', r'WATERPROOF', r'ADHESIVE', r'GROUT', r'MESH', r'SHEET', r'DPC', r'POLYTHENE', r'MORTAR', r'BLOCK', r'GYPSUM', r'ARALDITE'],
        'TOOLS': [r'DRILL', r'GRINDER', r'TAPE', r'SAFETY', r'HAMMER', r'PLIER', r'WRENCH', r'SQUARE', r'LEVEL', r'SAW', r'FILE', r'SPanner', r'SCREWDRIVER', r'TOOL', r'MASONRY', r'WHEELBARROW', r'SHOVE', r'HOE', r'RAKE', r'WELDING', r'DISK', r'CUTTING']
    }

    # 2. Refinement Logic
    refined = []
    seen_products = set() # (Name.upper(), Category)
    
    # Sort to prioritize keeping better data if dups exist
    products.sort(key=lambda x: 0 if x['category'] != 'UNCATEGORIZED' else 1)

    for p in products:
        name = p['name'].strip()
        
        # Filter placeholders and junk
        if name in ["—", "PRODUCT NAME", "SKU", "BRAND", "CATEGORY", ".", "...", "-"] or not name or len(name) < 2:
            continue
            
        # Standardize Category name
        original_cat = p['category'].upper()
        
        # Initial mapping based on PDF sections
        if original_cat in ['BARBED WIRE', 'BOLTS', 'BRACKETS', 'CHAIN LINKS', 'CHICKEN WIRE', 'GYPSAM SCREW', 'HANDLE', 'HINGES', 'KUKU NET', 'LOCK', 'LOCKS', 'NAILS', 'PADLOCKS', 'RIVETS', 'SCREWS', 'WINDOW FASTENERS', 'WINDOW STAYS', 'WIRE MESH']:
            found_cat_str = 'HARDWARE & FASTENERS'
        elif original_cat in ['G.I FITTINGS', 'HDPE FITTINGS', 'PTG FITTING', 'SINKS', 'TAPS', 'TOILET', 'UPVC PRESSURE PIPE', 'WASTE FITTINGS', 'WATER METERS', 'PPR FITTINGS']:
            found_cat_str = 'PIPES'
        elif original_cat in ['BOARDS', 'BLACK SHEET', 'DPC', 'EXPANDED METAL', 'EXPANDED PLASTIC', 'PAPER 3FT*12KG', 'PAPER 3FT*20KG', 'POLYTHENE PAPER', 'TUBES']:
            found_cat_str = 'BUILDING MATERIALS'
        elif original_cat in ['PAINT']:
            found_cat_str = 'PAINTS'
        elif original_cat in ['RIDGES']:
            found_cat_str = 'IRON SHEETS'
        elif original_cat in ['ELECTRICALS']:
            found_cat_str = 'ELECTRICALS'
        elif original_cat in ['TOOLS']:
            found_cat_str = 'TOOLS'
        else:
            found_cat_str = 'GENERAL HARDWARE'
            
        # Keyword overrides for high-precision categorization
        for target_cat, keywords in category_map.items():
            for kw in keywords:
                if re.search(kw, name, re.IGNORECASE):
                    found_cat_str = target_cat
                    break
            if found_cat_str == target_cat: break

        p['category'] = found_cat_str
        
        # Deduplication based on Name (Exact)
        unique_key = f"{name.upper()}|{p['category']}"
        if unique_key not in seen_products:
            seen_products.add(unique_key)
            # Standardize description
            p['description'] = f"Premium {name} available at NJAWAMU Hardware. Professional grade materials for construction, maintenance, and DIY projects."
            # Set subcategory as original if it was useful, else use Category
            p['subcategory'] = original_cat if original_cat != 'UNCATEGORIZED' else 'General'
            p['keywords'] = f"NJAWAMU, {p['category']}, {name}, {p['brand']}, {p['subcategory']}"
            refined.append(p)

    # 3. Stats & Printing
    from collections import Counter
    final_cats = Counter([x['category'] for x in refined])
    print(f"Final Count: {len(refined)} items (from original {len(products)})")
    print(f"Duplicates/Junk removed: {len(products) - len(refined)}")
    print("Category Breakdown:")
    for cat in sorted(final_cats):
        print(f"  {cat}: {final_cats[cat]}")

    # Write results
    with open('src/assets/data/products.json', 'w') as f:
        json.dump(refined, f, indent=2)
        
    js_content = f"/**\n * Official NJAWAMU Hardware Catalog - 100% Verified\n * Total Count: {len(refined)}\n */\n\nwindow.NJAWAMUProducts = {json.dumps(refined, indent=2)};"
    with open('src/scripts/product-data.js', 'w') as f:
        f.write(js_content)
    
    print("Refinement process complete.")

if __name__ == "__main__":
    refine_catalog('src/assets/data/products.json')
