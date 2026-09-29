from collections import Counter

from app.schemas.document import DocumentPage
from app.ingestion.text_cleaner import TextCleaner


class DocumentCleaner:

    def __init__(self):
        self.text_cleaner = TextCleaner()

    def clean(
        self,
        pages: list[DocumentPage]
    ) -> list[DocumentPage]:

        # First perform normal page-level cleaning
        cleaned_pages = [
            self.text_cleaner.clean_page(page)
            for page in pages
        ]

        # Count how many pages contain each line
        line_page_count = Counter()

        for page in cleaned_pages:

            unique_lines = set(
                line
                for line in page.text.split("\n")
                if line.strip()
            )

            for line in unique_lines:
                line_page_count[line] += 1

        # A line appearing on >= 50% of pages
        # is considered a possible repeated header/footer.
        threshold = max(2, len(cleaned_pages) // 2)

        repeated_lines = {
            line
            for line, count in line_page_count.items()
            if count >= threshold
        }

        result = []

        for page in cleaned_pages:

            lines = [
                line
                for line in page.text.split("\n")
                if line.strip() not in repeated_lines
            ]

            result.append(
                page.model_copy(
                    update={
                        "text": "\n".join(lines)
                    }
                )
            )

        return result