import json
import os

# Define keyword mapping to image paths
# Structure: { "keyword": "image_path" }
# IMPORTANT: Put more specific keywords FIRST to avoid incorrect mapping (e.g. BARBED WIRE before WIRE)
KEYWORD_MAPPING = [
    # Building Materials
    ("BAMBURI", "assets/images/products/building-materials/cement.jpg"),
    ("SIMBA", "assets/images/products/building-materials/cement.jpg"),
    ("SAVANNAH", "assets/images/products/building-materials/cement.jpg"),
    ("NGUVU", "assets/images/products/building-materials/cement.jpg"),
    ("CEMENT", "assets/images/products/building-materials/cement.jpg"),
    ("DEVKI", "assets/images/products/building-materials/iron-sheet.jpg"),
    ("MAISHA", "assets/images/products/building-materials/iron-sheet.jpg"),
    ("BOX PROFILE", "assets/images/products/building-materials/iron-sheet.jpg"),
    ("IRON SHEET", "assets/images/products/building-materials/iron-sheet.jpg"),
    ("ROOFING", "assets/images/products/building-materials/iron-sheet.jpg"),
    ("MDF BOARD", "assets/images/products/building-materials/mdf.jpg"),
    ("MDF", "assets/images/products/building-materials/mdf.jpg"),
    ("PLYWOOD", "assets/images/products/building-materials/plywood.jpg"),
    ("BLOCK BOARD", "assets/images/products/building-materials/plywood.jpg"),

    # Plumbing
    ("KENTANK", "assets/images/products/plumbing/tank.jpg"),
    ("ROTO", "assets/images/products/plumbing/tank.jpg"),
    ("TANK", "assets/images/products/plumbing/tank.jpg"),
    ("PPR PIPE", "assets/images/products/plumbing/ppr-pipe.jpg"),
    ("PVC PIPE", "assets/images/products/plumbing/tap.jpg"),
    ("BIB TAP", "assets/images/products/plumbing/tap.jpg"),
    ("BRASS", "assets/images/products/plumbing/tap.jpg"),
    ("TAP", "assets/images/products/plumbing/tap.jpg"),
    ("MIXER", "assets/images/products/plumbing/tap.jpg"),
    ("WASTE", "assets/images/products/plumbing/tap.jpg"),
    ("SINK", "assets/images/products/plumbing/tap.jpg"),

    # Electrical
    ("TRONIC", "assets/images/products/electrical/socket.jpg"),
    ("SOCKET", "assets/images/products/electrical/socket.jpg"),
    ("SWITCH", "assets/images/products/electrical/socket.jpg"),
    ("CABLE", "assets/images/products/electrical/cable.jpg"),
    ("WIRE", "assets/images/products/electrical/cable.jpg"), # Generic wire fallback
    ("BULB", "assets/images/products/electrical/bulb.jpg"),
    ("LED", "assets/images/products/electrical/bulb.jpg"),

    # Hardware & Security
    ("TRI-CIRCLE", "assets/images/products/hardware/padlock.jpg"),
    ("PADLOCK", "assets/images/products/hardware/padlock.jpg"),
    ("BARBED WIRE", "assets/images/products/hardware/barbed-wire.jpg"), # More specific than WIRE
    ("NAIL", "assets/images/products/hardware/nails.jpg"),
    ("SCREW", "assets/images/products/hardware/nails.jpg"),
    ("BOLT", "assets/images/products/hardware/nails.jpg"),
    ("NUT", "assets/images/products/hardware/nails.jpg"),

    # Paints
    ("CROWN", "assets/images/products/paints/paints.jpg"),
    ("BASCO", "assets/images/products/paints/paints.jpg"),
    ("VINYL", "assets/images/products/paints/paints.jpg"),
    ("EMULSION", "assets/images/products/paints/paints.jpg"),
    ("PAINT", "assets/images/products/paints/paints.jpg"),
]

# Category fallbacks
CATEGORY_MAPPING = {
    "BUILDING MATERIALS": "assets/images/products/building-materials/cement.jpg",
    "ELECTRICALS": "assets/images/products/electrical/socket.jpg",
    "PIPES": "assets/images/products/plumbing/tap.jpg",
    "PAINTS": "assets/images/products/paints/paints.jpg",
    "NAILS": "assets/images/products/hardware/nails.jpg",
    "PADLOCKS": "assets/images/products/hardware/padlock.jpg",
    "TOOLS": "assets/images/products/hardware/tools.jpg",
}

DEFAULT_IMAGE = "assets/images/products/hardware/tools.jpg"

def update_products():
    with open('src/assets/data/products.json', 'r') as f:
        products = json.load(f)

    updated_count = 0
    for product in products:
        name = product.get('name', '').upper()
        category = product.get('category', '').upper()
        
        assigned = False
        
        # 1. Keyword match in Name (using ordered list)
        for kw, img in KEYWORD_MAPPING:
            if kw in name:
                product['image'] = img
                product['images'] = [img]
                assigned = True
                break
        
        # 2. Category match if not assigned
        if not assigned:
            if category in CATEGORY_MAPPING:
                product['image'] = CATEGORY_MAPPING[category]
                product['images'] = [CATEGORY_MAPPING[category]]
                assigned = True
        
        # 3. Default fallback
        if not assigned:
            product['image'] = DEFAULT_IMAGE
            product['images'] = [DEFAULT_IMAGE]
        
        updated_count += 1

    with open('src/assets/data/products.json', 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Successfully updated {updated_count} products with authentic Kenyan hardware images.")

if __name__ == "__main__":
    update_products()
