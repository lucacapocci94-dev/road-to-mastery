"""Hook SessionEnd — consolidamento finale + push di sicurezza.

Backstop su uscita pulita della sessione. Side-effect puro, esce sempre 0.
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
    msg = f"chiusura sessione {datetime.now():%Y-%m-%d %H:%M}"
    try:
        gitsync.checkpoint(cwd, ["stato", "materie"], msg=msg)
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
