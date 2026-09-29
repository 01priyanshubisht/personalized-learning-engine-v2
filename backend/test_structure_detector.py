from app.ingestion.structure_detector import StructureDetector
from app.schemas.document import DocumentPage


pages = [
    DocumentPage(
        page_number=1,
        text="""Chapter 1: Hashing
HashMap stores key-value pairs.

Time Complexity
Average lookup is O(1).
Worst case lookup is O(n).

Conclusion
Hashing provides efficient lookup."""
    )
]


detector = StructureDetector()

blocks = detector.detect(pages)

for block in blocks:

    print(
        f"[{block.block_type.value.upper()}] "
        f"Page {block.page_number}: "
        f"{block.text}"
    )