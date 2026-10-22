#!/bin/bash
cd "$(dirname "$0")" || exit 1
if [ ! -x backend/.venv/bin/python ]; then
  echo "Execute ./setup.sh para preparar o ambiente primeiro."
  read -r -p "Pressione Enter para fechar." response_text
  exit 1
fi
backend/.venv/bin/python run_local.py
launcher_status=$?
if [ "$launcher_status" -ne 0 ]; then
  echo
  echo "O aplicativo não foi iniciado. Confira as instruções acima."
  read -r -p "Pressione Enter para fechar esta janela." response_text
fi
exit "$launcher_status"
