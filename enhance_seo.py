import json
import os

def enhance_seo_and_standardize():
    json_path = 'src/assets/data/products.json'
    
    with open(json_path, 'r') as f:
        products = json.load(f)
    
    count = 0
    for product in products:
        name = product['name'].upper()
        category = product['category']
        brand = product.get('brand', 'NJAWAMU')
        
        # 1. Smarter SEO Description
        # If the description is the generic one or missing, improve it.
        if not product.get('description') or 'Contact NJAWAMU' in product['description'] or 'High-quality' in product['description']:
            # Construct a more descriptive SEO text
            cat_label = category.lower().replace('/', ' ')
            desc = (f"Discover the premium {product['name']} at NJAWAMU Hardware. "
                    f"This {cat_label} essential is engineered for durability and reliable performance in "
                    f"various construction and maintenance applications. Trusted by professionals across Kenya.")
            
            if product.get('description') != desc:
                product['description'] = desc
                count += 1
        
        # 2. Add Meta Keywords (proactive enhancement)
        keywords = [brand, category, product['name']]
        # Add some broad hardware keywords
        keywords.extend(["Hardware Kenya", "Construction Materials", "Njawamu Store"])
        product['keywords'] = ", ".join(keywords)

    with open(json_path, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"Enhanced SEO for {count} products in products.json")

if __name__ == "__main__":
    enhance_seo_and_standardize()
