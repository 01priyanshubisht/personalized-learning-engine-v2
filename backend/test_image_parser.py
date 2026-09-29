from pathlib import Path

from app.ingestion.image_parser import ImageParser


image_path = Path("data/documents/test.png")

parser = ImageParser()

pages = parser.parse(image_path)

print("Total pages:", len(pages))

for page in pages:
    print("\n-------------------------")
    print("Page:", page.page_number)
    print("-------------------------")
    print(page.text)