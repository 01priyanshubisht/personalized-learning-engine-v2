from app.schemas.document import DocumentChunk
from app.schemas.structure import BlockType, DocumentBlock


class StructureAwareChunker:

    def __init__(self, max_words: int = 400):
        self.max_words = max_words

    def chunk(
        self,
        document_id: str,
        blocks: list[DocumentBlock],
    ) -> list[DocumentChunk]:

        chunks: list[DocumentChunk] = []

        current_section: str | None = None
        current_blocks: list[DocumentBlock] = []

        chunk_index = 0

        def flush() -> None:
            nonlocal chunk_index

            if not current_blocks:
                return

            text = "\n".join(
                block.text
                for block in current_blocks
            ).strip()

            if not text:
                return

            pages = [
                block.page_number
                for block in current_blocks
            ]

            chunks.append(
                DocumentChunk(
                    chunk_id=f"{document_id}_{chunk_index}",
                    document_id=document_id,
                    page_start=min(pages),
                    page_end=max(pages),
                    section=current_section,
                    text=text,
                )
            )

            chunk_index += 1

        for block in blocks:

            # A new heading starts a new logical section.
            if block.block_type == BlockType.HEADING:

                flush()

                current_blocks.clear()

                current_section = block.text

                current_blocks.append(block)

                continue

            current_word_count = sum(
                len(b.text.split())
                for b in current_blocks
            )

            block_word_count = len(
                block.text.split()
            )

            # Prevent excessively large chunks.
            if (
                current_blocks
                and current_word_count + block_word_count
                > self.max_words
            ):
                flush()

                current_blocks.clear()

            current_blocks.append(block)

        flush()

        return chunks