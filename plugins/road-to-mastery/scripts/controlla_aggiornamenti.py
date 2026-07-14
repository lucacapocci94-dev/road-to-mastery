#!/usr/bin/env python3
"""Controlla se c'è una versione più recente del plugin road-to-mastery.

A differenza di un controllo "a memoria", qui si fa la cosa giusta:
1. **RINFRESCA il marketplace** (`claude plugin marketplace update`) così la cache
   locale ha davvero l'ultima versione pubblicata;
2. confronta la versione **INSTALLATA / in uso** (da `CLAUDE_PLUGIN_ROOT`) con
   quella **DISPONIBILE nella cache del marketplace** — cioè esattamente ciò che
   `/plugin update` installerebbe. (Non con un branch di GitHub: la versione in
   uso, appena scaricata, non è ancora "applicata", quindi confrontare la propria
   versione con se stessa darebbe sempre "sei aggiornato".)
3. mostra le novità dal CHANGELOG della versione disponibile.

Non installa nulla: l'aggiornamento vero lo fa la skill `/aggiornami`. Non
solleva mai: su errore stampa un avviso ed esce 0.

Uso:
    python3 controlla_aggiornamenti.py [--no-refresh]
"""
import json
import os
import subprocess
import sys
from pathlib import Path

MARKETPLACE = "road-to-mastery"
PLUGIN = "road-to-mastery"


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


def plugin_root() -> Path:
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    return Path(env) if env else Path(__file__).resolve().parents[1]


def installed_version() -> str:
    try:
        pj = json.loads((plugin_root() / ".claude-plugin" / "plugin.json").read_text())
        return pj.get("version", "0.0.0")
    except Exception:
        return "0.0.0"


def refresh_marketplace():
    """Rinfresca il catalogo del marketplace (best-effort, silenzioso)."""
    if not _has_claude():
        return
    try:
        subprocess.run(
            ["claude", "plugin", "marketplace", "update", MARKETPLACE],
            capture_output=True, text=True, timeout=120,
        )
    except Exception:
        pass


def _has_claude():
    from shutil import which
    return which("claude") is not None


def _marketplaces_base() -> Path:
    home = Path(os.environ.get("HOME", str(Path.home())))
    return home / ".claude" / "plugins" / "marketplaces"


def available_version_and_changelog():
    """Versione più alta del plugin trovata nelle cache dei marketplace, e il suo
    CHANGELOG. (None, None) se non trovata."""
    base = _marketplaces_base()
    best_ver, best_dir = None, None
    if base.is_dir():
        for root, _dirs, files in os.walk(base):
            if "plugin.json" in files and Path(root).name == ".claude-plugin" \
                    and Path(root).parent.name == PLUGIN:
                try:
                    ver = json.loads((Path(root) / "plugin.json").read_text()).get("version")
                except Exception:
                    continue
                if ver and (best_ver is None or parse_version(ver) > parse_version(best_ver)):
                    best_ver, best_dir = ver, Path(root).parent  # .../road-to-mastery/
    changelog = None
    if best_dir is not None and (best_dir / "CHANGELOG.md").exists():
        try:
            changelog = (best_dir / "CHANGELOG.md").read_text()
        except Exception:
            changelog = None
    return best_ver, changelog


def novita_dal_changelog(local: str, changelog_text: str) -> str:
    loc = parse_version(local)
    blocchi, cattura = [], False
    for riga in (changelog_text or "").splitlines():
        if riga.startswith("## "):
            titolo = riga[3:].strip()
            primo = titolo.split()[0] if titolo else ""
            cattura = bool(primo) and primo[0].isdigit() and parse_version(primo) > loc
            if cattura:
                blocchi.append(riga[3:].strip())
        elif cattura and riga.strip():
            blocchi.append(riga.rstrip())
    return "\n".join(blocchi).strip()


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--no-refresh" not in argv:
        refresh_marketplace()

    inst = installed_version()
    avail, changelog = available_version_and_changelog()

    if avail is None:
        print("⚠️ Non ho trovato il plugin nel marketplace (nessuna rete o "
              "marketplace non ancora aggiunto).")
        print(f"Versione in uso: {inst}.")
        return 0

    if parse_version(avail) <= parse_version(inst):
        print(f"✅ Sei già all'ultima versione del plugin ({inst}).")
        return 0

    print(f"⬆️ Disponibile la versione {avail} (in uso la {inst}).")
    novita = novita_dal_changelog(inst, changelog or "")
    if novita:
        print("\nNovità:")
        print(novita)
    return 0


if __name__ == "__main__":
    sys.exit(main())
