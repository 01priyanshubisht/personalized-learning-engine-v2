import re

from app.schemas.document import DocumentPage, DocumentLine
from app.schemas.structure import BlockType, DocumentBlock


class StructureDetector:

    NUMBERED_HEADING = re.compile(
        r"^(\d+(\.\d+)*)[\.\)]?\s+\S+"
    )

    def detect(
        self,
        pages: list[DocumentPage],
    ) -> list[DocumentBlock]:

        blocks = []

        for page in pages:

            body_font_size = self._estimate_body_font_size(page)

            for line in page.lines:

                text = line.text.strip()

                if not text:
                    continue

                font_size = self._get_average_font_size(line)
                bold = self._is_bold(line)

                heading_score = self._heading_score(
                    text=text,
                    font_size=font_size,
                    body_font_size=body_font_size,
                    bold=bold,
                )

                block_type = (
                    BlockType.HEADING
                    if heading_score >= 2
                    else BlockType.BODY
                )

                blocks.append(
                    DocumentBlock(
                        text=text,
                        block_type=block_type,
                        page_number=page.page_number,
                        font_size=font_size,
                        bold=bold,
                        italic=self._is_italic(line),
                    )
                )

        return blocks

    def _estimate_body_font_size(
        self,
        page: DocumentPage,
    ) -> float | None:

        sizes = []

        for line in page.lines:

            for span in line.spans:

                if span.font_size is not None:
                    sizes.append(span.font_size)

        if not sizes:
            return None

        # Most common font size is a reasonable
        # approximation of body text.
        frequency = {}

        for size in sizes:
            frequency[size] = frequency.get(size, 0) + 1

        return max(
            frequency,
            key=frequency.get
        )

    def _get_average_font_size(
        self,
        line: DocumentLine,
    ) -> float | None:

        sizes = [
            span.font_size
            for span in line.spans
            if span.font_size is not None
        ]

        if not sizes:
            return None

        return sum(sizes) / len(sizes)

    def _is_bold(
        self,
        line: DocumentLine,
    ) -> bool:

        if not line.spans:
            return False

        return all(
            span.bold
            for span in line.spans
        )

    def _is_italic(
        self,
        line: DocumentLine,
    ) -> bool:

        if not line.spans:
            return False

        return all(
            span.italic
            for span in line.spans
        )

    def _heading_score(
        self,
        text: str,
        font_size: float | None,
        body_font_size: float | None,
        bold: bool,
    ) -> int:

        score = 0

        # Signal 1: noticeably larger font
        if (
            font_size is not None
            and body_font_size is not None
            and font_size >= body_font_size * 1.15
        ):
            score += 1

        # Signal 2: bold
        if bold:
            score += 1

        # Signal 3: numbered heading
        if self.NUMBERED_HEADING.match(text):
            score += 1

        # Signal 4: short line
        if len(text.split()) <= 10:
            score += 1

        return score