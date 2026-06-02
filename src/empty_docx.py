from docx import Document
from pathlib import Path


def create_empty_docx(
    path: Path,
):

    document = Document()

    document.save(path)
