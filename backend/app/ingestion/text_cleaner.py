import re

from app.schemas.document import DocumentPage


class TextCleaner:

    def clean_page(self, page: DocumentPage) -> DocumentPage:

        text = page.text

        text = self._normalize_line_endings(text)
        text = self._remove_repeated_whitespace(text)
        text = self._fix_hyphenation(text)
        text = self._remove_empty_lines(text)

        return page.model_copy(
            update={
                "text": text
            }
        )

    def _normalize_line_endings(self, text: str) -> str:

        return text.replace(
            "\r\n", "\n"
        ).replace(
            "\r", "\n"
        )

    def _remove_repeated_whitespace(self, text: str) -> str:

        lines = []

        for line in text.split("\n"):

            line = re.sub(
                r"[ \t]+",
                " ",
                line
            )

            lines.append(line.strip())

        return "\n".join(lines)

    def _fix_hyphenation(self, text: str) -> str:

        return re.sub(
            r"(\w)-\n(\w)",
            r"\1\2",
            text
        )

    def _remove_empty_lines(self, text: str) -> str:

        lines = [
            line
            for line in text.split("\n")
            if line.strip()
        ]

        return "\n".join(lines)