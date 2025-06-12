import re

def summarize_text(text: str) -> str:
    lines = text.split('\n')
    lines = [line.strip() for line in lines if len(line.strip()) > 30]
    return " ".join(lines[:3]) or "Resumen no disponible."

def extract_entities(text: str) -> list:
    pattern = r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b"
    entities = list(set(re.findall(pattern, text)))
    return entities[:10]
