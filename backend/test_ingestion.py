from pathlib import Path

from app.ingestion.ingestion_service import IngestionService


service = IngestionService()

chunks = service.ingest(
    file_path=Path("data/documents/test.pdf"),
    document_id="test_document",
)

print("Total chunks:", len(chunks))

for chunk in chunks:
    print("\n==============================")
    print("ID:", chunk.chunk_id)
    print("Section:", chunk.section)
    print("Pages:", chunk.page_start, "-", chunk.page_end)
    print("==============================")
    print(chunk.text[:500])