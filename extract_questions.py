import os
import glob
import re
from pdf2image import convert_from_path
import pytesseract
import json

def extract_text_from_pdfs(input_dir):
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return []

    all_texts = []
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        try:
            # First check if full_ocr_text.txt already exists to speed up development
            if os.path.exists("full_ocr_text.txt"):
                with open("full_ocr_text.txt", "r", encoding="utf-8") as f:
                    full_text = f.read()
                print("  Loaded from cached full_ocr_text.txt")
            else:
                images = convert_from_path(pdf_file, dpi=300)
                full_text = ""
                for i, image in enumerate(images):
                    print(f"  OCR page {i+1}/{len(images)}...")
                    text = pytesseract.image_to_string(image)
                    full_text += f"\n\n--- PAGE {i+1} ---\n\n" + text
                with open("full_ocr_text.txt", "w", encoding="utf-8") as f:
                    f.write(full_text)

            all_texts.append({
                "file": pdf_file,
                "text": full_text
            })
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

    return all_texts

def parse_questions_from_text(text):
    questions = []
    lines = text.split('\n')
    current_q = ""

    for line in lines:
        line = line.strip()
        # Skip header/footer lines and page markers
        if "SC/NSC" in line or "DBE/" in line or "Copyright reserved" in line or "Please turn over" in line or line.startswith("--- PAGE"):
            continue

        # Match pattern like "1.1", "1.1.1", "2.1"
        if re.match(r'^\d+\.\d+(\.\d+)?\s+', line):
            if current_q:
                questions.append(current_q.strip())
            current_q = line
        elif line.startswith("QUESTION "):
            if current_q:
                questions.append(current_q.strip())
                current_q = ""
        elif current_q and line:
            # Skip single numbers in parentheses which are marks like "(5)"
            if re.match(r'^\(\d+\)$', line) or re.match(r'^\[\d+\]$', line):
                continue
            current_q += " " + line

    if current_q:
        questions.append(current_q.strip())

    return questions

if __name__ == "__main__":
    texts = extract_text_from_pdfs("papers")
    for t in texts:
        print(f"\nExtracted {len(t['text'])} characters from {t['file']}")
        questions = parse_questions_from_text(t['text'])
        print(f"Parsed {len(questions)} questions.")
        with open("parsed_questions.json", "w") as f:
            json.dump(questions, f, indent=4)
        print("Saved to parsed_questions.json")
