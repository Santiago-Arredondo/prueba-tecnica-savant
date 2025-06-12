import json
from pathlib import Path

DB_FILE = Path("app/utils/storage.json")

def get_all_documents():
    if not DB_FILE.exists():
        DB_FILE.write_text("[]")  # crea archivo si no existe
    content = DB_FILE.read_text().strip()
    if not content:
        return []
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return []
    
def save_document(doc):
    docs = get_all_documents()
    docs.append(doc)
    DB_FILE.write_text(json.dumps(docs, indent=2, ensure_ascii=False))


