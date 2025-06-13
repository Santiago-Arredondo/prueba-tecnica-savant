import re

def summarize_text(text: str) -> str:
    # Intenta encontrar una línea útil como resumen
    resumen = re.search(r"(hoja de confirmación.*?Flock Freight.*?)\n", text, re.IGNORECASE)
    if resumen:
        return resumen.group(1).strip()

    resumen = re.search(r"(Invoice|Rate Confirmation).*", text, re.IGNORECASE)
    if resumen:
        return resumen.group(0).strip()

    return "Resumen no disponible"

def extract_entities(text: str) -> dict:
    def find(pattern, source_text):
        match = re.search(pattern, source_text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def find_all(pattern, source_text):
        return re.findall(pattern, source_text, re.IGNORECASE)

    # Correos y teléfonos múltiples
    emails = find_all(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phones = find_all(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)

    # Campos clave
    po = find(r"PO[#:\-\s]*([A-Z0-9\-]+)", text)
    carrier = find(r"Carrier[:\s]*([\w\s.&,-]+)", text)
    pickup_company = find(r"1\s+Pick\s+(.*)", text)
    pickup_datetime = find(r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}.*?\d{1,2}:\d{2}.*?(AM|PM)", text)
    delivery_company = find(r"2\s+Drop\s+(.*)", text)
    delivery_datetime = find(r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}.*?\d{1,2}:\d{2}.*?CST", text)

    entities = {
        "Carrier": carrier or "Desconocido",
        "Email": " / ".join(emails) if emails else "",
        "Phone": phones[0] if phones else "",
        "Stops": {
            "Stop 1": {
                "Stop type": "Pick",
                "Company": pickup_company,
                "Date/time": pickup_datetime,
                "PO#": po,
                "Services": "-",
                "Stop Notes": "-"
            },
            "Stop 2": {
                "Stop type": "Drop",
                "Company": delivery_company,
                "Date/time": delivery_datetime,
                "PO#": po,
                "Services": "-",
                "Stop Notes": "-"
            }
        }
    }

    return entities
