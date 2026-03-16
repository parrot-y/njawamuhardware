import json

def sync_js():
    with open('src/assets/data/products.json', 'r') as f:
        data = json.load(f)
    
    with open('src/scripts/product-data.js', 'w') as f:
        f.write("/**\n * NJAWAMU Hardware — Product Database\n * Consolidated and Deduplicated\n */\n\n")
        f.write("window.RenovyteProducts = ")
        json.dump(data, f, indent=2)
        f.write(";\n")
    
    print("Successfully synced src/scripts/product-data.js")

if __name__ == "__main__":
    sync_js()
