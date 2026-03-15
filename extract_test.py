import fitz
import pytesseract
from PIL import Image
import io

doc = fitz.open("Mathematics P1 May-June 2024 Eng.pdf")

print("Extracting text and images from page 2...")
page = doc[2] # page index 2 is usually page 3, maybe questions start here

# Extract text directly
text = page.get_text()
print("--- Text from page ---")
print(text[:1000])

# Extract images and OCR them
image_list = page.get_images(full=True)
print(f"--- Found {len(image_list)} images ---")
for img_index, img in enumerate(image_list):
    xref = img[0]
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    image = Image.open(io.BytesIO(image_bytes))

    # Try OCR
    ocr_text = pytesseract.image_to_string(image)
    if ocr_text.strip():
        print(f"--- OCR from Image {img_index} ---")
        print(ocr_text[:500])
