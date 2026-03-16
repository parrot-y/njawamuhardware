import json
import os
import shutil

def organize():
    data_path = 'src/assets/data/products.json'
    img_root = 'src/assets/images/products'
    
    with open(data_path, 'r') as f:
        products = json.load(f)
    
    # Map official categories to clean folder names
    cat_folder_map = {
        'PAINTS':               'paints',
        'PIPES':                'plumbing',
        'ELECTRICALS':          'electrical',
        'HARDWARE & FASTENERS': 'hardware-fasteners',
        'BUILDING MATERIALS':   'building-materials',
        'IRON SHEETS':          'iron-sheets',
        'TOOLS':                'tools',
        'GENERAL HARDWARE':     'general-hardware',
    }
    
    # 1. Create all category folders if they don't exist
    for folder in cat_folder_map.values():
        folder_path = os.path.join(img_root, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"  ✅ Folder ready: {folder_path}")

    # 2. Move existing images from old folders into correct category folders
    #    Old folders: hardware, plumbing, electrical, paints, building-materials, tools
    old_folder_map = {
        'hardware':   'general-hardware',
        'plumbing':   'plumbing',
        'electrical': 'electrical',
        'paints':     'paints',
        'building-materials': 'building-materials',
        'tools':      'tools',
    }
    moved = 0
    for old_folder, new_folder in old_folder_map.items():
        src_dir = os.path.join(img_root, old_folder)
        dst_dir = os.path.join(img_root, new_folder)
        if not os.path.exists(src_dir):
            continue
        for f in os.listdir(src_dir):
            if 'placeholder' in f.lower():
                continue
            src_file = os.path.join(src_dir, f)
            dst_file = os.path.join(dst_dir, f)
            if not os.path.exists(dst_file):
                shutil.move(src_file, dst_file)
                moved += 1
    print(f"\n  Moved {moved} images into category folders.")

    # 3. Update products.json image paths and generate helpful missing images list
    placeholder = 'assets/images/products/hardware/placeholder.png'
    missing_lines = []
    
    for p in products:
        cat = p['category']
        folder = cat_folder_map.get(cat, 'general-hardware')
        folder_path = f'/home/kali/Desktop/NJAWAMU/src/assets/images/products/{folder}'
        
        # If product still uses placeholder, add to missing list
        if p.get('image', '').endswith(('placeholder.png', 'placeholder.jpg')):
            missing_lines.append(
                f"{p['id']} | {p['name']} | {folder_path}"
            )
        
        # Also fix the product placeholder path to use correct category folder
        p['image'] = f'assets/images/products/{folder}/placeholder.png'
        p['images'] = [f'assets/images/products/{folder}/placeholder.png']
    
    # 4. Write updated products.json and JS
    with open(data_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    js_content = f"/**\n * Official NJAWAMU Hardware Catalog\n * Total Count: {len(products)}\n */\n\nwindow.NJAWAMUProducts = {json.dumps(products, indent=2)};"
    with open('src/scripts/product-data.js', 'w') as f:
        f.write(js_content)

    # 5. Write updated missing images list with FULL FOLDER PATHS
    with open('products_missing_images.txt', 'w') as f:
        f.write("FORMAT: ID | PRODUCT NAME | FOLDER TO ADD IMAGE\n")
        f.write("=" * 80 + "\n")
        f.write('\n'.join(missing_lines))
    
    print(f"\n  ✅ {len(missing_lines)} products still need images.")
    print("  ✅ products_missing_images.txt updated with full folder paths.")

    # 6. Copy placeholder.png to every new folder so the site doesn't break
    src_placeholder = os.path.join(img_root, 'hardware', 'placeholder.png')
    for folder in cat_folder_map.values():
        dst_placeholder = os.path.join(img_root, folder, 'placeholder.png')
        if not os.path.exists(dst_placeholder) and os.path.exists(src_placeholder):
            shutil.copy(src_placeholder, dst_placeholder)

if __name__ == '__main__':
    organize()
