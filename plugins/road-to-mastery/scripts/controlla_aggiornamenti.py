#!/usr/bin/env python3
"""Controlla se sul marketplace c'è una versione più nuova del plugin.

Confronta la versione INSTALLATA (il `plugin.json` locale, individuato via
`CLAUDE_PLUGIN_ROOT`) con quella pubblicata su `main` del repo marketplace, e
stampa un riepilogo leggibile + le novità dal CHANGELOG.

Principi (coerenti col resto del motore):
- Non solleva mai e non blocca: senza rete o su errore dice solo che non è
  riuscito a controllare ed esce 0. I file locali restano la verità.
- Nessun effetto collaterale: legge e basta. L'aggiornamento vero lo fa il
  comando nativo `/plugin update`, guidato dalla skill `/aggiornami`.

Uso:
    python3 controlla_aggiornamenti.py
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

OWNER_REPO = "lucacapocci94-dev/road-to-mastery"
RAW = f"https://raw.githubusercontent.com/{OWNER_REPO}/main/plugins/road-to-mastery"


def plugin_root() -> Path:
    """Radice del plugin installato: da CLAUDE_PLUGIN_ROOT, con fallback locale."""
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        return Path(env)
    # fallback: scripts/ -> radice del plugin
    return Path(__file__).resolve().parents[1]


def parse_version(s):
    """'1.2.3' -> (1, 2, 3). Tollerante a suffissi e campi mancanti."""
    parts = []
    for token in (s or "").strip().split("."):
        num = ""
        for ch in token:
            if ch.isdigit():
                num += ch
            else:
                break
        parts.append(int(num) if num else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def local_version() -> str:
    try:
        pj = json.loads((plugin_root() / ".claude-plugin" / "plugin.json").read_text())
        return pj.get("version", "0.0.0")
    except Exception:
        return "0.0.0"


def _fetch(url, timeout=8):
    req = urllib.request.Request(url, headers={"User-Agent": "road-to-mastery"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def remote_version():
    try:
        return json.loads(_fetch(f"{RAW}/.claude-plugin/plugin.json")).get("version")
    except Exception:
        return None


def novita_dal_changelog(local: str, changelog_text: str) -> str:
    """Righe di novità per le versioni > `local`, dal testo del CHANGELOG."""
    loc = parse_version(local)
    blocchi, cattura = [], False
    for riga in (changelog_text or "").splitlines():
        if riga.startswith("## "):
            titolo = riga[3:].strip()
            primo = titolo.split()[0] if titolo else ""
            # cattura solo sezioni con una versione semver più alta di quella locale
            cattura = bool(primo) and primo[0].isdigit() and parse_version(primo) > loc
            if cattura:
                blocchi.append(riga[3:].strip())
        elif cattura and riga.strip():
            blocchi.append(riga.rstrip())
    return "\n".join(blocchi).strip()


def main():
    local = local_version()
    remote = remote_version()

    if remote is None:
        print("⚠️ Non sono riuscito a controllare gli aggiornamenti (nessuna rete?).")
        print(f"Versione installata: {local}.")
        return 0

    if parse_version(remote) <= parse_version(local):
        print(f"✅ Sei già all'ultima versione del plugin ({local}).")
        return 0

    print(f"⬆️ Disponibile la versione {remote} (tu hai la {local}).")
    try:
        novita = novita_dal_changelog(local, _fetch(f"{RAW}/CHANGELOG.md"))
    except Exception:
        novita = ""
    if novita:
        print("\nNovità:")
        print(novita)
    return 0


if __name__ == "__main__":
    sys.exit(main())
