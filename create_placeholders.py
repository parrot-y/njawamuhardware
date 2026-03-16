"""
Physically creates a named placeholder file for each product whose image
does not yet exist on disk. Products.json already has the right paths.
"""
import json
import os
import shutil

def create_files():
    data_path = 'src/assets/data/products.json'
    src_dir = 'src'
    placeholder_src = 'src/assets/images/products/hardware/placeholder.png'

    with open(data_path, 'r') as f:
        products = json.load(f)

    created = 0
    skipped = 0

    for p in products:
        web_path = p.get('image', '')
        if not web_path:
            continue

        # Convert web path to filesystem path
        disk_path = os.path.join('src', web_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(disk_path), exist_ok=True)

        if not os.path.exists(disk_path):
            if os.path.exists(placeholder_src):
                shutil.copy(placeholder_src, disk_path)
                created += 1
        else:
            skipped += 1

    print(f"✅ Created {created} named placeholder files.")
    print(f"   Skipped {skipped} products (real image already exists).")

if __name__ == '__main__':
    create_files()
