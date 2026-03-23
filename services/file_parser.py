import pdfplumber
import docx
import io

class FileParser:

    def parse_pdf(self, file_bytes):
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def parse_docx(self, file_bytes):
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])