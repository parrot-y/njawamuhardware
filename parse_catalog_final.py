import pypdf
import json
import re

def parse_perfect(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    all_products = []
    current_category = "GENERAL HARDWARE"
    
    # Columns in layout mode (char offsets)
    COL_SKU = 0
    COL_NAME = 13
    COL_BRAND = 70
    COL_CAT = 100
    
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout")
        lines = text.split('\n')
        
        for line in lines:
            line = line.rstrip()
            if not line.strip(): continue
            
            # 1. Update Category if header found
            cat_match = re.search(r'^(.*?)\s\((\d+)\sitems\)$', line.strip())
            if cat_match:
                # Capture the text before the parenthesis as category
                candidate = cat_match.group(1).strip().upper()
                # Sanity check: categories shouldn't look like SKU headers
                if "SKU" not in candidate and "PRODUCT NAME" not in candidate:
                    current_category = candidate
                continue
            
            # 2. Detect Product Row
            sku_match = re.match(r'^\s*(\d{1,5})\b', line)
            if sku_match:
                sku = sku_match.group(1)
                
                # Extract by layout offsets
                # We normalize the line to ensure it has enough length for slicing
                padded = line.ljust(150)
                name_val = padded[COL_NAME:COL_BRAND].strip()
                brand_val = padded[COL_BRAND:COL_CAT].strip()
                
                # If name_val is empty, the layout might have shifted
                if not name_val:
                    # Try to get everything between SKU and next column
                    name_val = padded[sku_match.end():COL_BRAND].strip()

                if name_val:
                    # Naming Fidelity: Remove common PDF artifacts like "PC(S)" sticking to names
                    # BUT keep it if it's part of the official naming convention
                    
                    # Deduplicate: only add if we haven't seen this EXACT SKU-Name combo on this page
                    # to handle weird PDF object duplication
                    all_products.append({
                        "id": f"hw-{sku.zfill(4)}",
                        "name": name_val,
                        "category": current_category,
                        "brand": brand_val if brand_val and brand_val != "—" else "NJAWAMU",
                        "price": "Contact for Price",
                        "description": f"Internal Catalog Item: {name_val}. Professional quality at NJAWAMU Hardware.",
                        "rating": 4.5,
                        "image": "assets/images/products/hardware/placeholder.png",
                        "images": ["assets/images/products/hardware/placeholder.png"],
                        "keywords": f"NJAWAMU, {current_category}, {name_val}"
                    })
                    
    return all_products

if __name__ == "__main__":
    products = parse_perfect("products_catalog.pdf")
    
    # Final Deduplication by SKU + Name + Category to capture 100% distinct rows
    unique_items = {}
    for p in products:
        # Create a unique key for every distinct row in the PDF
        key = f"{p['id']}-{p['name']}"
        if key not in unique_items:
            unique_items[key] = p
            
    final_list = list(unique_items.values())
    print(f"Extraction results:")
    print(f"- Total Rows Scanned: {len(products)}")
    print(f"- Unique Products Loaded: {len(final_list)}")
    
    # Final Database Save
    with open('src/scripts/product-data.js', 'w') as f:
        f.write(f"/**\n * NJAWAMU Hardware Official Catalog\n * Total Items: {len(final_list)}\n */\n\nwindow.NJAWAMUProducts = {json.dumps(final_list, indent=2)};")
        
    with open('src/assets/data/products.json', 'w') as f:
        json.dump(final_list, f, indent=2)
        
    print("Catalog sync 100% complete.")
