"""
Enterprise File Handler

Handles:
- File Validation
- File Upload
- SHA256 Hash
- MIME Type
- Metadata Extraction
- Duplicate Detection Support
"""

import hashlib
import mimetypes
import shutil
import uuid
from pathlib import Path

import fitz
from docx import Document
from fastapi import HTTPException, UploadFile

from backend.core.config import settings


# ==========================================================
# Upload Directory
# ==========================================================

UPLOAD_DIR = Path(settings.UPLOAD_DIR)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# Supported File Types
# ==========================================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".doc",
    ".txt",
    ".ppt",
    ".pptx",
    ".xlsx",
    ".xls",
    ".csv",
    ".md",
}


# ==========================================================
# Validate File
# ==========================================================

def validate_file(file: UploadFile) -> None:
    """
    Validate uploaded file.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )


# ==========================================================
# Generate Unique Filename
# ==========================================================

def generate_filename(filename: str) -> str:
    """
    Generate unique filename.
    """

    extension = Path(filename).suffix.lower()

    return f"{uuid.uuid4()}{extension}"


# ==========================================================
# Save Uploaded File
# ==========================================================

def save_file(file: UploadFile) -> Path:
    """
    Save uploaded file to uploads directory.
    """

    validate_file(file)

    filename = generate_filename(file.filename)

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


# ==========================================================
# Delete File
# ==========================================================

def delete_file(file_path: str) -> bool:
    """
    Delete uploaded file.
    """

    path = Path(file_path)

    if path.exists():
        path.unlink()
        return True

    return False


# ==========================================================
# File Size
# ==========================================================

def get_file_size(file_path: Path) -> int:
    """
    Returns file size in bytes.
    """

    return file_path.stat().st_size


# ==========================================================
# File Extension
# ==========================================================

def get_extension(filename: str) -> str:
    """
    Returns file extension.
    """

    return Path(filename).suffix.lower()


# ==========================================================
# MIME Type
# ==========================================================

def get_mime_type(filename: str) -> str:
    """
    Returns MIME type.
    """

    mime, _ = mimetypes.guess_type(filename)

    return mime or "application/octet-stream"


# ==========================================================
# SHA256 Hash
# ==========================================================

def calculate_file_hash(file_path: Path) -> str:
    """
    Calculate SHA256 hash.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            chunk = file.read(8192)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# ==========================================================
# PDF Page Count
# ==========================================================

def get_pdf_pages(file_path: Path) -> int:
    """
    Return number of PDF pages.
    """

    pdf = fitz.open(file_path)

    pages = len(pdf)

    pdf.close()

    return pages


# ==========================================================
# DOC/DOCX Word Count
# ==========================================================

def get_docx_word_count(file_path: Path) -> int:
    """
    Count words in DOCX file.
    """

    document = Document(file_path)

    count = 0

    for paragraph in document.paragraphs:
        count += len(paragraph.text.split())

    return count


# ==========================================================
# TXT / CSV / MD Word Count
# ==========================================================

def get_text_word_count(file_path: Path) -> int:
    """
    Count words in text-based files.
    """

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

        text = file.read()

    return len(text.split())


# ==========================================================
# Metadata Extraction
# ==========================================================

def extract_metadata(file_path: Path):
    """
    Extract metadata based on file type.

    Returns:
        pages, words
    """

    extension = get_extension(file_path.name)

    pages = 0

    words = 0

    if extension == ".pdf":

        pages = get_pdf_pages(file_path)

    elif extension in [".doc", ".docx"]:

        words = get_docx_word_count(file_path)

    elif extension in [".txt", ".csv", ".md"]:

        words = get_text_word_count(file_path)

    elif extension in [".ppt", ".pptx"]:

        # Will implement slide count later
        pages = 1

    elif extension in [".xls", ".xlsx"]:

        # Will implement sheet count later
        pages = 1

    return pages, words