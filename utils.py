from io import BytesIO
from pypdf import PdfReader

MAX_MB = 10
ALLOWED = ["pdf", "txt"]
IMAGE_TYPES = ["png", "jpg", "jpeg", "webp"]


def extract_text(uploaded_file):
    """Return (text, error). Exactly one of them is None."""
    if uploaded_file is None:
        return None, "No file uploaded."

    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED:
        return None, f"Unsupported file type .{ext}. Please upload a PDF or TXT."

    data = uploaded_file.getvalue()
    if len(data) > MAX_MB * 1024 * 1024:
        return None, f"File is larger than {MAX_MB} MB."
    if len(data) == 0:
        return None, "The file is empty."

    try:
        if ext == "txt":
            text = data.decode("utf-8", errors="ignore")
        else:
            reader = PdfReader(BytesIO(data))
            if reader.is_encrypted:
                return None, "This PDF is password protected."
            text = "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception as e:
        return None, f"Could not read the file: {e}"

    text = text.strip()
    if not text:
        return None, ("No text found. This looks like a scanned image PDF. "
                      "Please upload a text PDF or a TXT file.")
    return text, None


def check_image(uploaded_file):
    """Return (bytes, mime, error)."""
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if ext not in IMAGE_TYPES:
        return None, None, f"Unsupported image type .{ext}. Use PNG, JPG or WEBP."
    data = uploaded_file.getvalue()
    if len(data) == 0:
        return None, None, "The image is empty."
    if len(data) > MAX_MB * 1024 * 1024:
        return None, None, f"Image is larger than {MAX_MB} MB."
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    return data, mime, None
