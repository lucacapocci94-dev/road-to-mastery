"""Hook Stop — checkpoint dei progressi a fine di ogni risposta.

Side-effect puro (lo stdout dello Stop non raggiunge il modello): commit + push
(se git disponibile) di stato/ e materie/. Esce sempre 0.
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gitsync  # noqa: E402


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        data = {}
    cwd = data.get("cwd") or os.getcwd()
    msg = f"checkpoint automatico {datetime.now():%Y-%m-%d %H:%M}"
    try:
        gitsync.checkpoint(cwd, ["stato", "materie"], msg=msg)
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
