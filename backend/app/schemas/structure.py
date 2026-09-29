from enum import Enum

from pydantic import BaseModel


class BlockType(str, Enum):
    HEADING = "heading"
    BODY = "body"


class DocumentBlock(BaseModel):
    text: str
    block_type: BlockType
    page_number: int

    font_size: float | None = None
    bold: bool = False
    italic: bool = False