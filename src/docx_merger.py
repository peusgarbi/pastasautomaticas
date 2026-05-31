from docxcompose.composer import Composer
from docx.enum.text import WD_BREAK
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
        paragraph = composer.doc.add_paragraph()
        paragraph.add_run().add_break(WD_BREAK.PAGE)

        composer.append(Document(file))

    composer.save(output_file)

    return output_file
