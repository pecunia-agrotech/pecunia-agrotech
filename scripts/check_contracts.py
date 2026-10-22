"""Detect drift between current FastAPI, the checked-in schema, and TypeScript."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from main import create_app  # noqa: E402

current = json.dumps(create_app().openapi(), ensure_ascii=False, indent=2) + "\n"
if current != (ROOT / "backend/openapi.json").read_text():
    raise SystemExit("O contrato OpenAPI mudou. Execute npm run contracts no frontend.")
with tempfile.TemporaryDirectory() as folder:
    source = Path(folder) / "openapi.json"
    target = Path(folder) / "api.generated.ts"
    source.write_text(current)
    subprocess.run(
        [
            str(ROOT / "frontend/node_modules/.bin/openapi-typescript"),
            str(source),
            "-o",
            str(target),
        ],
        check=True,
        capture_output=True,
    )
    if (
        target.read_text()
        != (ROOT / "frontend/src/core/types/api.generated.ts").read_text()
    ):
        raise SystemExit(
            "Os tipos do frontend estão desatualizados. Execute npm run contracts."
        )
print("Contratos compatíveis: FastAPI, OpenAPI e tipos TypeScript.")
