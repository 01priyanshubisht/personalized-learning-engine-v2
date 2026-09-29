from pydantic import BaseModel, Field


class TextSpan(BaseModel):
    text: str
    font: str | None = None
    font_size: float | None = None
    bold: bool = False
    italic: bool = False
    bbox: tuple[float, float, float, float] | None = None


class DocumentLine(BaseModel):
    text: str
    spans: list[TextSpan] = []
    bbox: tuple[float, float, float, float] | None = None


class DocumentPage(BaseModel):
    page_number: int = Field(..., ge=1)
    text: str
    lines: list[DocumentLine] = []


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str

    page_start: int = Field(..., ge=1)
    page_end: int = Field(..., ge=1)

    section: str | None = None
    text: str

    metadata: dict[str, str | int | float | bool] = {}