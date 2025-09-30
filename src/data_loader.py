# src/data_loader.py
import os
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document

def load_files(folder_path: str) -> str:
    """Đọc nhiều định dạng file (PDF, TXT, DOCX, CSV) trong folder và gộp nội dung."""
    text = ""
    for fname in os.listdir(folder_path):
        path = os.path.join(folder_path, fname)
        try:
            if fname.lower().endswith(".pdf"):
                text += "\n".join(page.extract_text() for page in PdfReader(path).pages if page.extract_text())
            elif fname.lower().endswith(".txt"):
                text += open(path, encoding="utf-8").read()
            elif fname.lower().endswith(".docx"):
                text += "\n".join(p.text for p in Document(path).paragraphs)
            elif fname.lower().endswith(".csv"):
                text += pd.read_csv(path, encoding="utf-8", on_bad_lines="skip").to_string()
        except Exception as e:
            print(f"⚠️ Lỗi đọc {fname}: {e}")
    return text.strip()
