from pathlib import Path

from app.ingestion.pdf_parser import PDFParser
from app.ingestion.document_cleaner import DocumentCleaner
from app.ingestion.structure_detector import StructureDetector
from app.ingestion.chunker import StructureAwareChunker


class IngestionService:

    def __init__(self):
        self.pdf_parser = PDFParser()
        self.document_cleaner = DocumentCleaner()
        self.structure_detector = StructureDetector()
        self.chunker = StructureAwareChunker()

    def ingest(
        self,
        file_path: Path,
        document_id: str,
    ):

        # 1. Parse PDF
        pages = self.pdf_parser.parse(file_path)

        # 2. Clean document
        pages = self.document_cleaner.clean(pages)

        # 3. Detect structure
        blocks = self.structure_detector.detect(pages)

        # 4. Create chunks
        chunks = self.chunker.chunk(
            document_id=document_id,
            blocks=blocks,
        )

        return chunks