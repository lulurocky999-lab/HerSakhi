import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using pdfplumber, falling back to PyPDF2 if it fails.
    """
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        if text.strip():
            return text
    except ImportError:
        logger.warning("pdfplumber not installed. Falling back to PyPDF2.")
    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}. Falling back to PyPDF2.")

    # Fallback to PyPDF2
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        logger.error(f"PyPDF2 fallback failed: {e}")
        return ""
