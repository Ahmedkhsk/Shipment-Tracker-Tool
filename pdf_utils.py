import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def merge_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        pdf_merger.append(pdf)
    pdf_merger.write(output_path)
    pdf_merger.close()
    print("PDF files merged successfully.")

def extract_text_from_pdf(pdf_path):
    # Try PyPDF2 first (fast)
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        if text.strip():
            print("Text extracted from PDF using PyPDF2.")
            return text
    except Exception as e:
        print("PyPDF2 extraction failed, trying OCR...", e)
    # If failed or empty, use OCR (slow)
    try:
        images = convert_from_path(pdf_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        print("Text extracted from PDF using OCR.")
        return text
    except Exception as e:
        print("OCR Error:", e)
        return ""

def extract_bill_of_lading(text):
    patterns = [
        r'BILL OF LADING No\.\s*([A-Z0-9]+)',
        r'B/L No[:\s]*([A-Z0-9]+)',
        r'BL NO[:\s]*([A-Z0-9]+)',
        r'Bill of Lading[:\s]*([A-Z0-9]+)',
        r'MEDU[A-Z0-9]+',
        r'MSDU[A-Z0-9]+',
        r'OOLU[A-Z0-9]+',
        r'MAEU[A-Z0-9]+',
        r'COSU[A-Z0-9]+',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"Bill of Lading number found: {match.group(1) if match.groups() else match.group(0)}")
            return match.group(1) if match.groups() else match.group(0)
    print("Bill of Lading number not found in text.")
    return None