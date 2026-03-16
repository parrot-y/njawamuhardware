from pypdf import PdfReader

def inspect_coordinates(pdf_path, page_idx=0):
    reader = PdfReader(pdf_path)
    page = reader.pages[page_idx]
    
    text_data = []
    def visitor(text, cm, tm, fontDict, fontSize):
        if text.strip():
            text_data.append({
                "text": text.strip(),
                "x": round(tm[4], 2),
                "y": round(tm[5], 2)
            })
            
    page.extract_text(visitor_text=visitor)
    
    # Sort by Y (descending) and then X (ascending)
    text_data.sort(key=lambda x: (-x['y'], x['x']))
    
    for item in text_data[:100]: # First 100 objects
        print(f"X: {item['x']:<8} Y: {item['y']:<8} Text: {item['text']}")

if __name__ == "__main__":
    inspect_coordinates("products_catalog.pdf")
