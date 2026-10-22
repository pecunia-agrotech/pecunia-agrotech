"""Create a consistent SQLite backup, including active WAL transactions."""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def create_backup(source: Path, folder: Path) -> Path:
    if not source.is_file():
        raise FileNotFoundError("Banco não encontrado. Inicie a aplicação primeiro.")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"farm-{datetime.now(timezone.utc):%Y%m%dT%H%M%S%fZ}.db"
    with sqlite3.connect(source) as origin, sqlite3.connect(target) as destination:
        origin.backup(destination)
    return target


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    source = Path(os.environ.get("PECUNIA_DB_PATH", str(root / "backend/data/farm.db")))
    try:
        result = create_backup(source, root / "backups")
        print(f"Backup consistente salvo em: {result}")
    except (OSError, sqlite3.Error):
        raise SystemExit(
            "Não foi possível criar o backup. Confira o banco e a pasta de destino."
        )
