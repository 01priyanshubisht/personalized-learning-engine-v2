from pathlib import Path

import pytesseract
from PIL import Image

from app.schemas.document import DocumentPage


class ImageParser:

    def parse(self, file_path: Path) -> list[DocumentPage]:

        if not file_path.exists():
            raise FileNotFoundError(
                f"Image not found: {file_path}"
            )

        try:
            image = Image.open(file_path)

            text = pytesseract.image_to_string(
                image
            ).strip()

        except Exception as exc:
            raise ValueError(
                f"Failed to process image: {file_path}"
            ) from exc

        return [
            DocumentPage(
                page_number=1,
                text=text
            )
        ]