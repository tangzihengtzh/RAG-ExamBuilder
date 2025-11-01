# pdf_loader.py (改进)
import fitz  # pip install pymupdf

def extract_chunks(pdf_path, max_len=448):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks, cur, idx = [], "", 0
    for p in paragraphs:
        if len(cur) + len(p) > max_len:
            chunks.append({"index": idx, "text": cur.strip()})
            idx += 1
            cur = p
        else:
            cur += " " + p
    if cur.strip():
        chunks.append({"index": idx, "text": cur.strip()})
    return chunks
