import pypdf

def test_extraction():
    reader = pypdf.PdfReader("products_catalog.pdf")
    # Test on page 3 or 4 where ELECTRICALS usually start
    for i in range(2, 6):
        print(f"--- Page {i+1} ---")
        print(reader.pages[i].extract_text(extraction_mode="layout"))

if __name__ == "__main__":
    test_extraction()
