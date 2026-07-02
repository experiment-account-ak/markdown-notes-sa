#!/usr/bin/env sh
cd "$(dirname "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
  exec python3 manage_notes.py
else
  exec python manage_notes.py
fi
