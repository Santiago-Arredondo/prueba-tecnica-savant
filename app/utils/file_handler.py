
import json
from pathlib import Path

DB_FILE = Path("app/storage.json")
if not DB_FILE.exists():
    DB_FILE.write_text("[]")

def save_document_info(info: dict):
    data = json.loads(DB_FILE.read_text())
    data.append(info)
    DB_FILE.write_text(json.dumps(data, indent=2))

def get_all_documents():
    return json.loads(DB_FILE.read_text())
