import fitz  # PyMuPDF
import os

# ------------------------------------------------------------------
# 1. IMPORTANT: Make sure this name is correct
PDF_FILE_NAME = "Health-Case-Studies-1654543959.pdf"
# 2. This will be our new output file
OUTPUT_TEXT_FILE = "full_book_raw.txt"


# ------------------------------------------------------------------

def extract_all_text(pdf_path, output_path):
    """
    Extracts all text from a text-based PDF and saves it
    to a single .txt file.
    """

    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    print(f"Opening PDF: {pdf_path}")
    all_text = ""

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"PDF has {total_pages} pages. Starting extraction...")

        # Loop through every page
        for page_num in range(total_pages):
            if (page_num + 1) % 20 == 0:  # Print a progress update every 20 pages
                print(f"  Processing page {page_num + 1}/{total_pages}...")

            page = doc.load_page(page_num)
            all_text += page.get_text()
            all_text += "\n--- End of Page ---\n"  # Add a marker for our reference

        doc.close()

        # Write all the extracted text to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(all_text)

        print("\n--- SUCCESS! ---")
        print(f"All text has been extracted and saved to: {OUTPUT_TEXT_FILE}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Run the extraction
if __name__ == "__main__":
    extract_all_text(PDF_FILE_NAME, OUTPUT_TEXT_FILE)