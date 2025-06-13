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
        "Analiza el siguiente texto proveniente de un documento logístico (como guía, factura o confirmación de carga). "
        "Extrae las entidades clave en formato JSON válido y estructurado. "
        "Incluye campos como: Carrier, Phone, Email, Stops, PO#, Date/time, Company, etc. "
        "Estructura los datos en forma anidada si es necesario.\n\n"
        "IMPORTANTE: Devuelve ÚNICAMENTE un objeto JSON válido. No agregues explicaciones ni etiquetas antes o después.\n"
        "Ejemplo de formato esperado:\n"
        "{\n"
        "  \"Carrier\": \"V TRUCKING\",\n"
        "  \"Phone\": \"346 373-0773\",\n"
        "  \"Email\": \"vtruckinghouston@gmail.com\",\n"
        "  \"Stops\": {\n"
        "    \"Stop 1\": {\n"
        "      \"Stop type\": \"Pick\",\n"
        "      \"Company\": \"Continental Poly 455 Julie Rivers Drive, Sugar Land, TX\",\n"
        "      \"Date/time\": \"12-22-20; 10:00 AM - 4:00 PM CST\",\n"
        "      \"PO#\": \"PO#4608482717\"\n"
        "    }\n"
        "  }\n"
        "}\n\n"
        f"Texto:\n{text}\n\n"
        "Recuerda: devuelve solo un JSON limpio que pueda ser parseado directamente."
    )

    response = requests.post("http://host.docker.internal:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })

    raw = response.json().get("response", "")
    print("Respuesta de Ollama:\n", raw)

    try:
        return json.loads(raw)
    except Exception:
        return {"error": "No se pudo parsear el JSON", "raw_output": raw}
