import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    texto = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""
    return texto
