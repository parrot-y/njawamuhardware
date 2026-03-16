from pypdf import PdfReader

def dump_page_layout(pdf_path, page_num=0):
    reader = PdfReader(pdf_path)
    page = reader.pages[page_num]
    
    objects = []
    def visitor(text, cm, tm, fontDict, fontSize):
        if text.strip():
            objects.append({
                "text": text.strip(),
                "x": tm[4],
                "y": tm[5]
            })
            
    page.extract_text(visitor_text=visitor)
    
    # Group by Y (allow for small variations)
    lines = {}
    for obj in objects:
        y_key = round(obj["y"], 0)
        if y_key not in lines:
            lines[y_key] = []
        lines[y_key].append(obj)
        
    sorted_y = sorted(lines.keys(), reverse=True)
    for y in sorted_y:
        row = sorted(lines[y], key=lambda x: x["x"])
        row_str = " | ".join([f"[{item['x']:>6.1f}] {item['text']}" for item in row])
        print(f"Y={y:>6.1f}: {row_str}")

if __name__ == "__main__":
    print("--- Page 1 Layout ---")
    dump_page_layout("products_catalog.pdf", 0)
