import json
import re

def parse_catalog(txt_path, json_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    products = []
    current_category = "UNCATEGORIZED"
    
    # Skip first few branding lines
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Detection of Category Header: "CATEGORY NAME (X items)"
        cat_match = re.match(r"^([A-Z &]+) \((\d+) items\)$", line)
        if cat_match:
            current_category = cat_match.group(1)
            i += 1
            continue
        
        # Skip noise and headers
        if line in ["PRODUCT", "CATALOG", "SKU", "PRODUCT NAME", "BRAND", "CATEGORY", "—"] or line.startswith("Total Products:") or "\f" in line:
            i += 1
            continue
            
        # Basic heuristic: if it looks like an ID (numeric SKU)
        if re.match(r"^\d{2,6}$", line):
            sku = line
            i += 1
            if i < len(lines):
                name = lines[i]
                i += 1
                brand = "—"
                
                # Look ahead for brand and category repetition
                temp_i = i
                if temp_i < len(lines) and lines[temp_i] == "—":
                    temp_i += 1
                elif temp_i < len(lines) and lines[temp_i] not in [current_category, "SKU"] and not re.match(r"^\d{2,6}$", lines[temp_i]):
                    brand = lines[temp_i]
                    temp_i += 1
                
                if temp_i < len(lines) and lines[temp_i] == current_category:
                    temp_i += 1
                
                i = temp_i
                
                products.append({
                    "id": f"hw-{sku}",
                    "name": name,
                    "category": current_category,
                    "brand": brand if brand != "—" else "NJAWAMU",
                    "price": "Contact for Price",
                    "description": f"High quality {name} for your construction and hardware needs. Contact NJAWAMU Hardware for current pricing and availability.",
                    "rating": 4.5,
                    "image": "assets/images/products/hardware/tools.jpg",
                    "images": ["assets/images/products/hardware/tools.jpg"]
                })
            else:
                break
        else:
            i += 1

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)
    
    print(f"Parsed {len(products)} products into {json_path}")

if __name__ == "__main__":
    parse_catalog("products_catalog_extracted.txt", "src/assets/data/products.json")
