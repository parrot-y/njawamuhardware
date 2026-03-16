import json
import os

# Paths
INPUT_PRODUCTS = 'src/assets/data/products.json'
SOURCE_OF_TRUTH = 'products_parsed.json'
OUTPUT_PRODUCTS = 'src/assets/data/products.json-new'

def reconcile():
    print("Starting reconciliation and deduplication...")
    
    # Load source of truth (parsed from PDF)
    with open(SOURCE_OF_TRUTH, 'r') as f:
        truth_data = json.load(f)
    
    # Map SKUs to original names
    sku_to_name = {item['sku'].strip(): item['name'].strip() for item in truth_data}
    
    # Load current products
    with open(INPUT_PRODUCTS, 'r') as f:
        current_products = json.load(f)
    
    reconciled_products = []
    seen_names = set()
    duplicates_removed = 0
    names_fixed = 0
    
    # Sort current products by ID to keep consistent order if possible
    current_products.sort(key=lambda x: x['id'])

    for p in current_products:
        sku = p['id'].replace('hw-', '')
        original_name = sku_to_name.get(sku)
        
        # 1. Fix Name if mismatch
        if original_name and p['name'] != original_name:
            p['name'] = original_name
            names_fixed += 1
            
        # 2. Deduplicate by Name
        # If the name is already seen, we skip it (remove duplicate)
        if p['name'] in seen_names:
            duplicates_removed += 1
            continue
            
        seen_names.add(p['name'])
        reconciled_products.append(p)

    print(f"Names fixed: {names_fixed}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final product count: {len(reconciled_products)}")

    # Update images list and other fields if needed (standardizing)
    for p in reconciled_products:
        if 'images' not in p:
            p['images'] = [p['image']]
        
    with open(OUTPUT_PRODUCTS, 'w') as f:
        json.dump(reconciled_products, f, indent=2)
    
    # Atomically replace (via rename would be better but this is fine for now)
    os.replace(OUTPUT_PRODUCTS, INPUT_PRODUCTS)
    print(f"Successfully updated {INPUT_PRODUCTS}")

if __name__ == "__main__":
    reconcile()
