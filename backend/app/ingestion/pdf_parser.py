from pathlib import Path

import pymupdf

from app.schemas.document import (
    DocumentLine,
    DocumentPage,
    TextSpan,
)


class PDFParser:

    def parse(self, file_path: Path) -> list[DocumentPage]:

        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {file_path}"
            )

        pages = []

        try:
            document = pymupdf.open(file_path)

            for page_number, page in enumerate(
                document,
                start=1
            ):
                page_data = page.get_text("dict")

                lines = []

                for block in page_data["blocks"]:

                    if "lines" not in block:
                        continue

                    for line in block["lines"]:

                        spans = []

                        for span in line["spans"]:

                            flags = span.get("flags", 0)

                            spans.append(
                                TextSpan(
                                    text=span["text"],
                                    font=span.get("font"),
                                    font_size=span.get("size"),
                                    bold=bool(flags & 16),
                                    italic=bool(flags & 2),
                                    bbox=tuple(span["bbox"]),
                                )
                            )

                        line_text = "".join(
                            span.text
                            for span in spans
                        ).strip()

                        if not line_text:
                            continue

                        lines.append(
                            DocumentLine(
                                text=line_text,
                                spans=spans,
                                bbox=tuple(line["bbox"]),
                            )
                        )

                page_text = "\n".join(
                    line.text
                    for line in lines
                )

                pages.append(
                    DocumentPage(
                        page_number=page_number,
                        text=page_text,
                        lines=lines,
                    )
                )

            document.close()

        except Exception as exc:
            raise ValueError(
                f"Failed to parse PDF: {file_path}"
            ) from exc

        return pages