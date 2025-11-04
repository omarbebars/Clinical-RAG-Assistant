import re
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter  # <-- THIS IS THE FIX

RAW_TEXT_FILE = "full_book_raw.txt"
CLEAN_JSON_FILE = "cases_database.json"


def clean_and_chunk_v3(input_file, output_file):
    """
    Reads the raw text, cleans it, and splits it into
    small, 1000-character chunks with overlap.
    This is the standard, robust RAG method.
    """
    print(f"Reading raw text from: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return

    # 1. Clean the *entire* text first
    try:
        start_index = full_text.index("Case Study #1: Chronic Obstructive Pulmonary")
        full_text = full_text[start_index:]
        print("Found start of content, ignoring Table of Contents.")
    except ValueError:
        print("Warning: Could not find 'Case Study #1' start. Chunking entire book.")

    full_text = re.sub(r'--- End of Page ---', '', full_text)
    full_text = re.sub(r'\n\s*\d+\s*\n', '\n', full_text)
    full_text = re.sub(r'\n{3,}', '\n\n', full_text).strip()

    print("Text cleaned. Now splitting into small chunks...")

    # 2. Split the text into small, fixed-size chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    small_chunks = text_splitter.split_text(full_text)

    print(f"Split the book into {len(small_chunks)} small chunks.")

    # 3. Format as JSON
    case_data = []
    for i, chunk_text in enumerate(small_chunks):
        case_data.append({
            "id": f"chunk_{i + 1}",
            "text": chunk_text
        })

    # 4. Saving
    print(f"Saving {len(case_data)} chunks to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(case_data, f, indent=2, ensure_ascii=False)

    print("\n--- SUCCESS! (V3) ---")
    print("Your new 'cases_database.json' is ready with small, fixed-size chunks.")


if __name__ == "__main__":
    clean_and_chunk_v3(RAW_TEXT_FILE, CLEAN_JSON_FILE)