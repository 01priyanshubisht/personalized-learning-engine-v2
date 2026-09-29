from pathlib import Path

from app.ingestion.pdf_parser import PDFParser


pdf_path = Path("data/documents/test.pdf")

parser = PDFParser()

pages = parser.parse(pdf_path)

for page in pages:

    print("\n==============================")
    print(f"PAGE {page.page_number}")
    print("==============================")

    for line in page.lines:

        print(f"\nLine: {line.text}")
        print(f"Line bbox: {line.bbox}")

        for span in line.spans:

            print(
                f"  Span: {span.text!r}"
            )

            print(
                f"  Font: {span.font}"
            )

            print(
                f"  Size: {span.font_size}"
            )

            print(
                f"  Bold: {span.bold}"
            )

            print(
                f"  Italic: {span.italic}"
            )

            print(
                f"  BBox: {span.bbox}"
            )