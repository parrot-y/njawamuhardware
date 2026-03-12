import json
import re

def parse_catalog_text(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    products = []
    current_category = None
    
    # Skip headers
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Detect Category Header like "BARBED WIRE (6 items)"
        cat_match = re.match(r'^(.*)\s+\(\d+\s+items\)$', line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            i += 1
            continue
            
        # Skip Table Headers
        if line in ["SKU", "PRODUCT NAME", "BRAND", "CATEGORY"]:
            i += 1
            continue
            
        # Potential SKU (usually 4 digits)
        if re.match(r'^\d{4}$', line):
            sku = line
            name = lines[i+1] if i+1 < len(lines) else ""
            brand = lines[i+2] if i+2 < len(lines) else ""
            category = lines[i+3] if i+3 < len(lines) else ""
            
            # Simple validation: category should match current_category or be a valid category name
            # If line i+3 is not a category, we might have a shift.
            # But based on the file preview, it's pretty consistent: SKU, Name, Brand, Category
            
            products.append({
                "sku": sku,
                "name": name,
                "brand": brand,
                "category": category if category else current_category
            })
            i += 4
            continue
            
        i += 1
        
    return products

if __name__ == "__main__":
    products = parse_catalog_text("/home/kali/Desktop/NJAWAMU/products_catalog_extracted.txt")
    with open("/home/kali/Desktop/NJAWAMU/products_parsed.json", "w") as f:
        json.dump(products, f, indent=4)
    print(f"Parsed {len(products)} products.")
