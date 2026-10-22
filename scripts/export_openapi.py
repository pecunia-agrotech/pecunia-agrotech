"""Export API contracts without creating or reading a database."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from main import create_app  # noqa: E402

schema = create_app().openapi()
output = ROOT / "backend" / "openapi.json"
output.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n")
print(f"OpenAPI exported: {output}")
