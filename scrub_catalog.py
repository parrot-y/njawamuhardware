"""
Scrubs redundant numbers and extraction artifacts from product names in the catalog.
Also renames associated image files to match the new clean names.
"""
import json
import os
import re
import shutil

def scrub_catalog():
    data_path = 'src/assets/data/products.json'
    js_path = 'src/scripts/product-data.js'
    img_root = 'src/assets/images/products'
    
    with open(data_path, 'r') as f:
        products = json.load(f)

    # 1. Define cleaning function
    def get_clean_name(name):
        original = name
        
        # Strip trailing PC(S), PCS, (S), PC
        name = re.sub(r'\s*(PC\(S\)|PCS|\(S\)|PC)$', '', name, flags=re.I)
        
        # Fix 'CARL AND' column merge artifact
        name = name.replace('CARL AND', 'CARLAND')
        
        # Remove redundant numbers from merges (e.g., '1 GANG 2 CARLAND' -> '1 GANG CARLAND')
        name = re.sub(r'(\d+\s*GANG)\s+\d+\s+(CARLAND)', r'\1 \2', name, flags=re.I)
        name = re.sub(r'(\d+\s*WAY)\s+\d+\s+(CARLAND)', r'\1 \2', name, flags=re.I)
        
        # Clean brand joins (e.g., 'SHELLAC 1ORION' -> 'SHELLAC ORION')
        name = re.sub(r'(\w+)\s+\d+(ORION|CARLAND|NJAWAMU)', r'\1 \2', name, flags=re.I)
        
        # General lone number removal at the end of the string (if not preceded by size markers)
        # We only do this if the number is small (1-5) and likely an index or page number artifact
        name = re.sub(r'\s+[1-5]$', '', name)
        
        return name.strip()

    def get_file_safe_name(name, pid):
        clean = name.lower()
        clean = clean.replace(' ', '-').replace('/', '-').replace('*', 'x')
        clean = ''.join(c for c in clean if c.isalnum() or c in '-_.')
        clean = clean.strip('-')
        return f"{clean[:60]}-{pid}.png"

    clean_count = 0
    rename_count = 0
    
    for p in products:
        old_name = p['name']
        new_name = get_clean_name(old_name)
        pid = p['id']
        
        if old_name != new_name:
            p['name'] = new_name
            p['description'] = p['description'].replace(old_name, new_name)
            p['keywords'] = p['keywords'].replace(old_name, new_name)
            clean_count += 1
            
        # Handle file renames
        old_image_path = p.get('image', '')
        if old_image_path and 'placeholder' not in old_image_path: # We treat the named placeholders as files to rename
            # Get folder from old path
            folder_part = os.path.dirname(old_image_path)
            new_filename = get_file_safe_name(new_name, pid)
            new_image_path = os.path.join(folder_part, new_filename)
            
            if old_image_path != new_image_path:
                old_disk_path = os.path.join('src', old_image_path)
                new_disk_path = os.path.join('src', new_image_path)
                
                if os.path.exists(old_disk_path):
                    os.makedirs(os.path.dirname(new_disk_path), exist_ok=True)
                    os.rename(old_disk_path, new_disk_path)
                    rename_count += 1
                
                p['image'] = new_image_path
                p['images'] = [new_image_path]

    # Save results
    with open(data_path, 'w') as f:
        json.dump(products, f, indent=2)
        
    js_content = f"/**\n * Official NJAWAMU Hardware Catalog - Cleaned\n * Total Count: {len(products)}\n */\n\nwindow.NJAWAMUProducts = {json.dumps(products, indent=2)};"
    with open(js_path, 'w') as f:
        f.write(js_content)

    print(f"✅ Scrubbed {clean_count} product names.")
    print(f"✅ Renamed {rename_count} image files on disk.")

if __name__ == "__main__":
    scrub_catalog()
