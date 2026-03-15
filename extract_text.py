import fitz

doc = fitz.open("Mathematics P1 May-June 2024 Eng.pdf")
text = ""
for page in doc:
    text += page.get_text()

with open("pdf_text.txt", "w") as f:
    f.write(text)
