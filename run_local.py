"""Start and stop only the locally owned backend and frontend processes."""

from __future__ import annotations

import argparse
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def available(port: int) -> bool:
    with socket.socket() as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pecunia AgroTech · execução offline local"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Usar Next.js e FastAPI com recarga automática",
    )
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    python = (
        ROOT
        / "backend"
        / ".venv"
        / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    )
    npm = shutil.which("npm")
    if (
        not python.is_file()
        or not npm
        or not (ROOT / "frontend" / "node_modules").is_dir()
    ):
        print(
            "Dependências ausentes. Execute ./setup.sh primeiro (conexão necessária apenas na instalação)."
        )
        return 1
    for port in (8000, 3000):
        if not available(port):
            print(
                f"A porta {port} já está em uso. A versão anterior pode continuar aberta.\n"
                "Volte ao Terminal em que ela foi iniciada e pressione Ctrl+C.\n"
                "Depois, abra START.command novamente. Fechar apenas o navegador não encerra o servidor.\n"
                "Nenhum processo existente foi encerrado."
            )
            return 1
    env = {**os.environ, "NEXT_TELEMETRY_DISABLED": "1"}
    if not args.dev and not (ROOT / "frontend" / ".next" / "BUILD_ID").is_file():
        result = subprocess.run(
            [npm, "run", "build"], cwd=ROOT / "frontend", env=env, check=False
        )
        if result.returncode:
            return result.returncode
    commands = [
        (
            [
                str(python.with_name("uv")),
                "run",
                "--offline",
                "--no-sync",
                "uvicorn",
                "main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ]
            + (["--reload"] if args.dev else []),
            ROOT / "backend",
        ),
        ([npm, "run", "dev" if args.dev else "start"], ROOT / "frontend"),
    ]
    processes: list[subprocess.Popen[bytes]] = []

    def stop_on_signal(_number: int, _frame: object) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop_on_signal)
    try:
        for command, cwd in commands:
            processes.append(
                subprocess.Popen(
                    command, cwd=cwd, env=env, start_new_session=os.name != "nt"
                )
            )
        deadline = time.monotonic() + 90
        ready = False
        while time.monotonic() < deadline:
            if any(p.poll() is not None for p in processes):
                raise RuntimeError(
                    "Um servidor encerrou antes de ficar pronto. Confira as mensagens acima."
                )
            try:
                for url in (
                    "http://127.0.0.1:8000/api/v1/health",
                    "http://127.0.0.1:3000",
                ):
                    with urllib.request.urlopen(url, timeout=2) as response:
                        if response.status != 200:
                            raise OSError("Aguardando resposta HTTP.")
                ready = True
                break
            except OSError:
                time.sleep(0.3)
        if not ready:
            raise RuntimeError("Tempo de inicialização excedido. Confira os logs.")
        print(
            "\nPecunia AgroTech pronto: http://localhost:3000\nAPI: http://localhost:8000\nCtrl+C encerra ambos os servidores.\n",
            flush=True,
        )
        if not args.no_browser:
            webbrowser.open("http://localhost:3000")
        while all(p.poll() is None for p in processes):
            time.sleep(0.5)
        raise RuntimeError(
            "Um dos servidores foi encerrado inesperadamente. Confira os logs."
        )
    except KeyboardInterrupt:
        print("\nEncerrando os servidores locais…", flush=True)
    except RuntimeError as error:
        print(str(error))
        return 1
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                if os.name == "nt":
                    process.terminate()
                else:
                    os.killpg(process.pid, signal.SIGTERM)
        for process in processes:
            try:
                process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    process.kill()
                else:
                    os.killpg(process.pid, signal.SIGKILL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
