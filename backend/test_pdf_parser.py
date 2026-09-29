from pathlib import Path

from app.ingestion.pdf_parser import PDFParser


pdf_path = Path("data/documents/test.pdf")

parser = PDFParser()

pages = parser.parse(pdf_path)

print("Total pages:", len(pages))

for page in pages:
    print("\n-------------------------")
    print("Page:", page.page_number)
    print("-------------------------")
    print(page.text[:500])