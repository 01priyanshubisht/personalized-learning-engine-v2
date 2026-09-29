from app.ingestion.document_cleaner import DocumentCleaner
from app.schemas.document import DocumentPage


pages = [
    DocumentPage(
        page_number=1,
        text="""My DSA Notes

HashMap
HashMap stores key-value pairs."""
    ),

    DocumentPage(
        page_number=2,
        text="""My DSA Notes

Linked List
Linked lists contain nodes."""
    ),

    DocumentPage(
        page_number=3,
        text="""My DSA Notes

Trees
Trees are hierarchical structures."""
    ),
]


cleaner = DocumentCleaner()

cleaned_pages = cleaner.clean(pages)

for page in cleaned_pages:

    print("\n--------------------")
    print(f"Page {page.page_number}")
    print("--------------------")

    print(page.text)