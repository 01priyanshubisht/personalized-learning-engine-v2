from pathlib import Path

from app.ingestion.chunker import StructureAwareChunker
from app.ingestion.structure_detector import StructureDetector
from app.ingestion.pdf_parser import PDFParser


pdf_path = Path("data/documents/test.pdf")

parser = PDFParser()
pages = parser.parse(pdf_path)

detector = StructureDetector()
blocks = detector.detect(pages)

chunker = StructureAwareChunker(
    max_words=400
)

chunks = chunker.chunk(
    document_id="test_document",
    blocks=blocks,
)

print("Total chunks:", len(chunks))

for chunk in chunks:

    print("\n==============================")
    print("Chunk ID:", chunk.chunk_id)
    print("Section:", chunk.section)
    print(
        "Pages:",
        chunk.page_start,
        "->",
        chunk.page_end
    )
    print("==============================")
    print(chunk.text)