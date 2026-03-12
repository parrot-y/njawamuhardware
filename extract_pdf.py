import pypdf
import json

def extract_pdf_data(pdf_path, output_json):
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open(output_json, "w") as f:
        f.write(text)

if __name__ == "__main__":
    extract_pdf_data("/home/kali/Desktop/NJAWAMU/products_catalog.pdf", "/home/kali/Desktop/NJAWAMU/products_catalog_extracted.txt")
