import re

def summarize_text(text: str) -> str:
    """
    Genera un resumen básico identificando el tipo de documento.
    """
    resumen = re.search(r"(hoja de confirmación.*?Flock Freight.*?)\n", text, re.IGNORECASE)
    if resumen:
        return resumen.group(1).strip()

    resumen = re.search(r"(Rate\s+Confirmation.*?)\n", text, re.IGNORECASE)
    if resumen:
        return resumen.group(1).strip()

    resumen = re.search(r"(Invoice\s+#?:?\s*\w+-?\d+)", text, re.IGNORECASE)
    if resumen:
        return resumen.group(1).strip()

    return "Resumen no disponible"


def extract_entities(text: str) -> dict:
    def find(pattern, source):
        match = re.search(pattern, source, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def find_all(pattern, source):
        return re.findall(pattern, source, re.IGNORECASE)

    # Correos electrónicos únicos
    emails = list(set(find_all(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)))
    email_result = " / ".join(sorted(set(email.lower() for email in emails)))

    # Teléfonos
    phones = find_all(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    phone_result = phones[0] if phones else ""

    # Carrier
    carrier_raw = find(r"Carrier[:\s]*([^\n\r]+)", text)
    if "confirmation" in carrier_raw.lower():
        carrier = re.sub(r"(rate\s+confirmation\s*)", "", carrier_raw, flags=re.IGNORECASE).strip()
    else:
        carrier = carrier_raw or "Desconocido"

    # PO#
    po = find(r"\bPO[:#\-\s]*([A-Z0-9\-]{3,})\b", text)

    # Paradas - más flexibles
    pickup_company = find(r"Shipper\s*[:\-]*\s*(.*)", text)
    drop_company = find(r"Consignee\s*[:\-]*\s*(.*)", text)

    pickup_time = find(r"Shipping Hours\s*[:\-]*\s*(.*)", text)
    drop_time = find(r"Receiving Hours\s*[:\-]*\s*(.*)", text)

    entities = {
        "Carrier": carrier,
        "Email": email_result,
        "Phone": phone_result,
        "Stops": {
            "Stop 1": {
                "Stop type": "Pick",
                "Company": pickup_company or "-",
                "Date/time": pickup_time or "-",
                "PO#": po or "-",
                "Services": "-",
                "Stop Notes": "-"
            },
            "Stop 2": {
                "Stop type": "Drop",
                "Company": drop_company or "-",
                "Date/time": drop_time or "-",
                "PO#": po or "-",
                "Services": "-",
                "Stop Notes": "-"
            }
        }
    }

    return entities
