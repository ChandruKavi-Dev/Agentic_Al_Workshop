import io
import docx
from pypdf import PdfReader
from fastapi import UploadFile

def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text content from an uploaded file (PDF, DOCX, TXT).
    """
    content = ""
    file_content = file.file.read()

    if file.filename.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(io.BytesIO(file_content))
            for page in pdf_reader.pages:
                content += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF {file.filename}: {e}")
            return "" # Return empty string on failure

    elif file.filename.endswith(".docx"):
        try:
            doc = docx.Document(io.BytesIO(file_content))
            for para in doc.paragraphs:
                content += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {file.filename}: {e}")
            return ""

    elif file.filename.endswith(".txt"):
        try:
            content = file_content.decode('utf-8')
        except Exception as e:
            print(f"Error reading TXT {file.filename}: {e}")
            return ""
            
    # Reset the file pointer in case it needs to be read again
    file.file.seek(0)
    return content