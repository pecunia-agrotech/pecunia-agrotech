#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
project_python="${PECUNIA_PYTHON:-}"
if [ -z "$project_python" ]; then
  if command -v python3.12 >/dev/null 2>&1; then
    project_python="$(command -v python3.12)"
  elif python3 -c 'import sys; assert sys.version_info >= (3,12)' 2>/dev/null; then
    project_python="$(command -v python3)"
  elif [ -x "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" ]; then
    project_python="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
  else
    echo "Instale Python 3.12 ou superior e execute novamente."
    exit 1
  fi
fi
"$project_python" -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ necessário"'
node -e 'const [major,minor]=process.versions.node.split(".").map(Number);if(major<20||(major===20&&minor<9))throw new Error("Node.js 20.9+ necessário")'
if command -v uv >/dev/null 2>&1; then
  project_uv="$(command -v uv)"
elif [ -x backend/.venv/bin/uv ]; then
  project_uv="$PWD/backend/.venv/bin/uv"
else
  "$project_python" -m venv .tooling
  .tooling/bin/python -m pip install 'uv==0.13.4'
  project_uv="$PWD/.tooling/bin/uv"
fi
"$project_uv" sync --locked --project backend --python "$project_python"
(cd frontend && npm ci --no-audit --no-fund && npm run contracts:check && NEXT_TELEMETRY_DISABLED=1 npm run build)
echo "Ambiente preparado. Execute ./START.command para operar offline."
