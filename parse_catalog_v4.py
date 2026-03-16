from pypdf import PdfReader
import json
import re

def parse_with_layout_logic(pdf_path):
    reader = PdfReader(pdf_path)
    all_products = []
    current_category = "General Hardware"
    
    # Define column regions (approximate X coordinates)
    # SKU: Starts at ~0
    # Name: Starts at ~70
    # Brand: Starts at ~380
    # Category: Starts at ~550
    
    for page in reader.pages:
        # Get raw text with layout mode
        layout_text = page.extract_text(extraction_mode="layout")
        
        for line in layout_text.split('\n'):
            line = line.rstrip()
            if not line.strip(): continue
            
            # Detect Category Header
            cat_match = re.search(r'^(.*?)\s\((\d+)\sitems\)$', line.strip())
            if cat_match:
                current_category = cat_match.group(1).upper()
                continue
            
            # Detect row: Starts with a numeric SKU (often indented)
            # Match 1-5 digits at the start of the line (after possible whitespace)
            row_match = re.match(r'^\s*(\d{1,5})\s+(.*)$', line)
            if row_match:
                sku = row_match.group(1)
                remainder = row_match.group(2)
                
                # The remainder contains Name, Brand, Category.
                # Since we used layout mode, we can try to find large gaps.
                # Or just split by columns if they are fixed.
                
                # Try to slice by column positions (found by inspection previously)
                # Note: 'remainder' starts at some offset from the original line.
                line_offset = line.find(sku) + len(sku)
                
                # Adjusting offsets relative to the start of the line
                name_start = 70
                brand_start = 380
                cat_start = 550
                
                # Ensure line is long enough
                name_part = line[name_start:brand_start].strip() if len(line) > name_start else ""
                brand_part = line[brand_start:cat_start].strip() if len(line) > brand_start else ""
                # category part usually is redundant but we can use it to verify
                
                if name_part:
                    # Clean up double spaces in name if any
                    name_part = re.sub(r'\s+', ' ', name_part)
                    brand_part = re.sub(r'\s+', ' ', brand_part)
                    
                    all_products.append({
                        "id": f"hw-{sku.zfill(4)}",
                        "name": name_part,
                        "category": current_category,
                        "brand": brand_part if brand_part and brand_part != "—" else "NJAWAMU",
                        "price": "Contact for Price",
                        "description": f"Internal Catalog Item: {name_part}. Available at NJAWAMU Hardware.",
                        "rating": 4.5,
                        "image": "assets/images/products/hardware/placeholder.png",
                        "images": ["assets/images/products/hardware/placeholder.png"],
                        "keywords": f"NJAWAMU, {current_category}, {name_part}"
                    })
                    
    return all_products

if __name__ == "__main__":
    products = parse_with_layout_logic("products_catalog.pdf")
    
    # Deduplicate by (Name, SKU) to be safe
    unique_products = {}
    for p in products:
        key = f"{p['name']}|{p['id']}".upper()
        if key not in unique_products:
            unique_products[key] = p
            
    final_list = list(unique_products.values())
    print(f"Total Rows: {len(products)}")
    print(f"Unique Products: {len(final_list)}")
    
    # Final write
    with open('src/scripts/product-data.js', 'w') as f:
        f.write(f"window.NJAWAMUProducts = {json.dumps(final_list, indent=2)};")
        
    with open('src/assets/data/products.json', 'w') as f:
        json.dump(final_list, f, indent=2)
        
    print("Catalog extraction complete with high-fidelity names.")
