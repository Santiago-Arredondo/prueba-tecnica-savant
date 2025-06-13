import requests
import json

def summarize_text(text: str) -> str:
    prompt = (
        "Resume el siguiente documento en 2 o 3 líneas, manteniendo los datos clave si se trata de una orden, factura o guía de carga.\n\n"
        f"{text}"
    )
    response = requests.post("http://host.docker.internal:11434/api/generate",  json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "")

def extract_entities(text: str) -> dict:
    prompt = (
        "A partir del siguiente texto extraído de un documento logístico o comercial, extrae las entidades clave y devuélvelas en formato JSON estructurado.\n"
        "Identifica campos como Carrier, Phone, Email, Stops, PO#, Date/time, etc., y agrúpalos de forma que se entiendan.\n"
        "Ejemplo de formato:\n"
        "{\n"
        "  \"Carrier\": \"...\",\n"
        "  \"Phone\": \"...\",\n"
        "  \"Email\": \"...\",\n"
        "  \"Stops\": {\n"
        "    \"Stop 1\": {\n"
        "      \"Stop type\": \"Pick\",\n"
        "      \"Company\": \"...\",\n"
        "      \"Date/time\": \"...\",\n"
        "      \"Services\": \"...\",\n"
        "      \"Stop Notes\": \"...\",\n"
        "      \"PO#\": \"...\"\n"
        "    }\n"
        "  }\n"
        "}\n"
        "\nTexto:\n"
        f"{text}\n\nDevuelve solo el JSON."
    )

    response = requests.post("http://host.docker.internal:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })

    raw = response.json().get("response", "")
    try:
        return json.loads(raw)
    except Exception:
        return {"error": "No se pudo parsear el JSON", "raw_output": raw}
