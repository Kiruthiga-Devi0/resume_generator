import re

def normalize_text(text: str) -> str:
    text = text or ""
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()

def extract_tokens(text: str) -> set:
    text = normalize_text(text)
    # Simple word tokenization; swap out for spaCy later
    tokens = set(re.findall(r"[a-zA-Z][a-zA-Z\-\+\.]{1,}", text))
    return tokens

def guess_sections(text: str) -> dict:
    """
    Heuristically split resume into sections using headings.
    Improve by using ML or stronger regex later.
    """
    text_norm = normalize_text(text)
    # Split on common headings
    parts = re.split(r"(experience|work experience|employment|education|skills|summary|profile|projects|certifications)\s*[:\n]", text_norm)
    # Re-scan into dict pairs
    sections = {}
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i+1].strip() if i+1 < len(parts) else ""
        sections[heading] = body
    return sections
