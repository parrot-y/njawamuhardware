from pypdf import PdfReader
import re
import json

def extract_with_coordinates(pdf_path):
    reader = PdfReader(pdf_path)
    all_products = []
    
    for page_num, page in enumerate(reader.pages):
        text_instances = []
        
        def visitor_text(text, cm, tm, fontDict, fontSize):
            x = tm[4]
            y = tm[5]
            if text.strip():
                text_instances.append({"text": text.strip(), "x": x, "y": y})
        
        page.extract_text(visitor_text=visitor_text)
        
        # Group by Y coordinate (lines)
        lines = {}
        for inst in text_instances:
            y = round(inst["y"], 1)
            if y not in lines:
                lines[y] = []
            lines[y].append(inst)
            
        current_category = "General Hardware"
        sorted_y = sorted(lines.keys(), reverse=True)
        
        for y in sorted_y:
            line_instances = sorted(lines[y], key=lambda x: x["x"])
            line_text = " ".join([inst["text"] for inst in line_instances])
            
            # Detect Category Header
            cat_match = re.match(r'^(.*)\s\((\d+)\sitems\)$', line_text)
            if cat_match:
                current_category = cat_match.group(1).upper()
                continue
                
            # Product row detection
            if line_instances and line_instances[0]["text"].isdigit() and len(line_instances[0]["text"]) <= 5:
                sku = line_instances[0]["text"]
                
                name_parts = []
                brand_parts = []
                
                for inst in line_instances[1:]:
                    # Based on standard 8.5x11 PDF @ 72dpi
                    # SKU < 70, Name 70-380, Brand 380-550, Category > 550
                    if inst["x"] < 380:
                        name_parts.append(inst["text"])
                    elif inst["x"] < 520:
                        brand_parts.append(inst["text"])
                    # Category usually repeats what we found in the header
                
                name = " ".join(name_parts)
                brand = " ".join(brand_parts) if brand_parts else "NJAWAMU"
                
                if name:
                    all_products.append({
                        "id": f"hw-{sku.zfill(4)}",
                        "name": name,
                        "category": current_category,
                        "brand": brand if brand != "—" else "NJAWAMU",
                        "price": "Contact for Price",
                        "description": f"Internal Catalog Item: {name}. High-quality hardware components.",
                        "rating": 4.5,
                        "image": "assets/images/products/hardware/placeholder.png",
                        "images": ["assets/images/products/hardware/placeholder.png"],
                        "keywords": f"NJAWAMU, {current_category}, {name}"
                    })
                    
    return all_products

if __name__ == "__main__":
    products = extract_with_coordinates("products_catalog.pdf")
    
    unique_products = {}
    for p in products:
        # Keep original case for "Exact Name" requirement
        key = f"{p['name']}|{p['category']}"
        if key not in unique_products:
            unique_products[key] = p
            
    final_list = list(unique_products.values())
    print(f"Extraction results: {len(products)} total rows found.")
    print(f"Unique Hardware Products: {len(final_list)}")
    
    with open('src/scripts/product-data.js', 'w') as f:
        f.write(f"window.NJAWAMUProducts = {json.dumps(final_list, indent=2)};")
    
    with open('src/assets/data/products.json', 'w') as f:
        json.dump(final_list, f, indent=2)
    
    print("Catalog successfully synchronized with coordinate-perfect names.")
