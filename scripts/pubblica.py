#!/usr/bin/env python3
"""Pubblica il plugin: alza la versione, aggiorna il CHANGELOG, committa e porta
le modifiche su `main` (auto-merge diretto).

STRUMENTO DI SVILUPPO — vive nel repo del marketplace e NON viene distribuito
agli studenti (sta fuori da `plugins/`).

Uso:
    python3 scripts/pubblica.py [patch|minor|major] [-m "riga di changelog"]
                                [--dry-run] [--no-merge] [--yes]

Passi:
 1. Verifica di essere in un repo git con l'albero di lavoro pulito.
 2. Alza la versione nel plugin.json (semver; default: patch).
 3. Aggiunge in cima al CHANGELOG del plugin una sezione con le novità
    (dalla riga -m, oppure dai messaggi dei commit non ancora su main).
 4. Committa il bump sul branch corrente.
 5. (default) checkout main, merge --no-ff del branch, push origin main, poi
    torna al branch di partenza.

Sicurezze:
 --dry-run  mostra cosa farebbe, senza scrivere/committare/pushare.
 --no-merge si ferma dopo il commit del bump (non tocca main).
 --yes      salta la domanda di conferma prima del merge su main.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "road-to-mastery"
PLUGIN_JSON = PLUGIN / ".claude-plugin" / "plugin.json"
CHANGELOG = PLUGIN / "CHANGELOG.md"
MAIN = "main"


def run(*args, check=True, capture=True):
    res = subprocess.run(
        list(args), cwd=REPO, capture_output=capture, text=True
    )
    if check and res.returncode != 0:
        err = (res.stderr or res.stdout or "").strip()
        raise SystemExit(f"✗ comando fallito: {' '.join(args)}\n{err}")
    return res


# --- versione ---------------------------------------------------------------

def bump_version(version: str, part: str) -> str:
    """'0.8.0' + 'minor' -> '0.9.0'. Reset dei livelli inferiori."""
    nums = [int(x) for x in re.findall(r"\d+", version)[:3]]
    while len(nums) < 3:
        nums.append(0)
    major, minor, patch = nums
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "patch":
        patch += 1
    else:
        raise SystemExit(f"✗ parte di versione sconosciuta: {part}")
    return f"{major}.{minor}.{patch}"


def leggi_versione() -> str:
    return json.loads(PLUGIN_JSON.read_text())["version"]


def scrivi_versione(nuova: str):
    """Sostituzione mirata della riga 'version' per non riformattare il JSON."""
    testo = PLUGIN_JSON.read_text()
    nuovo, n = re.subn(
        r'("version"\s*:\s*")[^"]+(")', rf"\g<1>{nuova}\g<2>", testo, count=1
    )
    if n != 1:
        raise SystemExit("✗ non ho trovato il campo 'version' nel plugin.json")
    PLUGIN_JSON.write_text(nuovo)


# --- changelog --------------------------------------------------------------

def voci_dai_commit() -> list:
    """Messaggi dei commit del branch corrente non ancora su main (soggetti)."""
    res = run("git", "log", f"{MAIN}..HEAD", "--format=%s", check=False)
    if res.returncode != 0:
        return []
    return [r.strip() for r in res.stdout.splitlines() if r.strip()]


def blocco_changelog(nuova: str, righe: list) -> str:
    oggi = date.today().isoformat()
    corpo = "\n".join(f"- {r}" for r in righe) if righe else "- Aggiornamenti vari."
    return f"## {nuova} — {oggi}\n{corpo}\n"


def aggiorna_changelog(nuova: str, righe: list):
    blocco = blocco_changelog(nuova, righe)
    if not CHANGELOG.exists():
        CHANGELOG.write_text(f"# Changelog — road-to-mastery\n\n{blocco}")
        return
    testo = CHANGELOG.read_text()
    idx = testo.find("\n## ")
    if idx == -1:
        # nessuna sezione ancora: appendi dopo l'intestazione
        CHANGELOG.write_text(testo.rstrip() + "\n\n" + blocco)
    else:
        CHANGELOG.write_text(testo[: idx + 1] + blocco + "\n" + testo[idx + 1 :])


# --- flusso -----------------------------------------------------------------

def branch_corrente() -> str:
    return run("git", "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def albero_pulito() -> bool:
    return run("git", "status", "--porcelain").stdout.strip() == ""


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pubblica il plugin road-to-mastery.")
    ap.add_argument("part", nargs="?", default="patch",
                    choices=["patch", "minor", "major"])
    ap.add_argument("-m", "--message", help="riga di changelog (altrimenti dai commit)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-merge", action="store_true")
    ap.add_argument("--yes", action="store_true", help="non chiedere conferma per il merge")
    args = ap.parse_args(argv)

    if run("git", "rev-parse", "--show-toplevel", check=False).returncode != 0:
        raise SystemExit("✗ non è un repo git.")

    branch = branch_corrente()
    attuale = leggi_versione()
    nuova = bump_version(attuale, args.part)
    righe = [args.message] if args.message else voci_dai_commit()

    print(f"Branch: {branch}")
    print(f"Versione: {attuale} → {nuova} ({args.part})")
    print("Novità nel changelog:")
    for r in (righe or ["Aggiornamenti vari."]):
        print(f"  - {r}")

    if args.dry_run:
        merge_txt = "no" if (args.no_merge or branch == MAIN) else f"sì (→ {MAIN})"
        print(f"\n[dry-run] nessuna scrittura. Merge su main: {merge_txt}.")
        return 0

    if not albero_pulito():
        raise SystemExit(
            "✗ ci sono modifiche non committate. Committa il lavoro del plugin "
            "prima di pubblicare (pubblica.py crea solo il commit di versione)."
        )

    # 2-3-4: bump + changelog + commit
    scrivi_versione(nuova)
    aggiorna_changelog(nuova, righe)
    run("git", "add", str(PLUGIN_JSON), str(CHANGELOG))
    run("git", "commit", "-m", f"chore: versione {nuova}")
    print(f"✓ commit del bump a {nuova} su {branch}")

    if args.no_merge:
        print("→ --no-merge: mi fermo qui (main non toccato).")
        return 0

    if branch == MAIN:
        run("git", "push", "origin", MAIN)
        print(f"✓ pushato su {MAIN}")
        return 0

    if not args.yes:
        risposta = input(f"Merge diretto di '{branch}' su '{MAIN}' e push? [s/N] ").strip().lower()
        if risposta not in ("s", "si", "sì", "y", "yes"):
            print("→ annullato: il commit del bump resta sul branch, main intatto.")
            return 0

    run("git", "checkout", MAIN)
    run("git", "pull", "--ff-only", "origin", MAIN, check=False)
    run("git", "merge", "--no-ff", branch, "-m", f"Pubblica {nuova}")
    run("git", "push", "origin", MAIN)
    run("git", "checkout", branch)
    print(f"✓ {nuova} pubblicata su {MAIN}. Gli studenti la vedranno con /plugin update.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
