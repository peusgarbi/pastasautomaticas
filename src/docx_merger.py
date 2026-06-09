from docx.enum.section import WD_SECTION_START
from docxcompose.composer import Composer
from docx import Document
from pathlib import Path


def merge_docx_files(
    files: list[Path],
    output_file: Path,
) -> Path:

    if not files:
        raise ValueError("Nenhum arquivo para unir.")

    master = Document(files[0])
    composer = Composer(master)

    for file in files[1:]:
        composer.doc.add_section(WD_SECTION_START.NEW_PAGE)
        composer.append(Document(file))

    composer.save(output_file)

    return output_file
