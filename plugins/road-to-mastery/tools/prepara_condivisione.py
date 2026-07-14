#!/usr/bin/env python3
"""Prepara un pacchetto di studio AUTONOMO da condividere, partendo dalla propria
cartella.

Il pacchetto:
- contiene SOLO le materie scelte (niente tutte le altre);
- ha i **progressi azzerati** (ogni lezione torna "○ da fare") e **nessun dato
  personale** (percentuali, punti deboli, diario, sessioni, domande);
- **include il motore** (il plugin road-to-mastery) come *marketplace locale*, con
  un hook di SessionStart che lo installa da solo al primo avvio: così a chi riceve
  funzionano subito tutti i comandi (/tutor, /programma, …), anche offline e senza
  installare nulla a mano.

Non tocca la cartella di partenza: scrive tutto nella cartella di destinazione.
Il `CLAUDE.md` e il `LEGGIMI.md` li scrive la skill `/condividi` (servono il
template del plugin e il contesto dell'esame).

Uso:
    python3 prepara_condivisione.py <src_root> <dest_dir> <slug-materia> [altri-slug...]
"""
import json
import os
import shutil
import sys
from pathlib import Path

# La radice del plugin (il "motore"): questo script vive in <plugin>/tools/.
ENGINE_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_NAME = "road-to-mastery"
PLUGIN_ID = f"road-to-mastery@{MARKETPLACE_NAME}"

# Stati "personali" delle lezioni → riportati tutti a "da fare".
# Le ⭐ (priorità sul syllabus) e ○ (già "da fare") NON si toccano.
_SOSTITUZIONI = [
    ("✓ completata", "○ da fare"),
    ("⚠ punto debole", "○ da fare"),
    ("↻ da rivedere", "○ da fare"),
    ("✓", "○"),
    ("⚠", "○"),
    ("↻", "○"),
]

_HOOK = """#!/bin/bash
# SessionStart del pacchetto condiviso: installa il motore-tutor (incluso qui come
# marketplace locale) così tutti i comandi funzionano subito, anche offline e senza
# installare nulla a mano. Idempotente: se è già installato, non fa niente.
set -u
command -v claude >/dev/null 2>&1 || exit 0
ROOT="${CLAUDE_PROJECT_DIR:-.}"
claude plugin marketplace add "$ROOT" >/dev/null 2>&1 || true
claude plugin install road-to-mastery@road-to-mastery >/dev/null 2>&1 || true
exit 0
"""


def reset_stati(text: str) -> str:
    """Riporta ogni marcatore di stato-lezione a 'da fare'."""
    for prima, dopo in _SOSTITUZIONI:
        text = text.replace(prima, dopo)
    return text


def _progressi(slugs) -> str:
    righe = "\n".join(f"- {s}: 0%" for s in slugs)
    return (
        "# Progressi\n\n"
        f"Materia attiva: {slugs[0]}\n\n"
        "## Materie\n"
        f"{righe}\n\n"
        "## Punti deboli\n(nessuno ancora)\n\n"
        "## Modalità attiva\nmicro\n\n"
        "## Livello-obiettivo\napprofondito\n\n"
        "## Calendario ripassi\n"
        "(ripasso dilazionato a 1, 3, 7, 16, 35 giorni dopo la prima padronanza "
        "di ogni lezione)\n"
    )


def _marketplace() -> str:
    data = {
        "name": MARKETPLACE_NAME,
        "owner": {"name": "Road to Mastery"},
        "description": "Motore-tutor incluso nel pacchetto (marketplace locale).",
        "plugins": [
            {
                "name": "road-to-mastery",
                "source": "./plugins/road-to-mastery",
                "description": "Motore-tutor per la preparazione a qualsiasi esame.",
            }
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _settings() -> str:
    data = {
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh",
                        }
                    ]
                }
            ]
        },
        "enabledPlugins": {PLUGIN_ID: True},
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _includi_motore(dest: Path):
    """Copia il motore nel pacchetto + marketplace locale + hook + settings."""
    # motore
    shutil.copytree(
        ENGINE_ROOT,
        dest / "plugins" / "road-to-mastery",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )
    # marketplace locale
    (dest / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (dest / ".claude-plugin" / "marketplace.json").write_text(
        _marketplace(), encoding="utf-8"
    )
    # hook di auto-installazione + settings
    hooks_dir = dest / ".claude" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook = hooks_dir / "session-start.sh"
    hook.write_text(_HOOK, encoding="utf-8")
    os.chmod(hook, 0o755)
    (dest / ".claude" / "settings.json").write_text(_settings(), encoding="utf-8")


def prepara(src_root, dest, slugs):
    src_root, dest = Path(src_root), Path(dest)
    materie_src = src_root / "materie"

    mancanti = [s for s in slugs if not (materie_src / s).is_dir()]
    if mancanti:
        raise SystemExit(f"✗ materie non trovate: {', '.join(mancanti)}")

    # motore incluso (autonomo)
    _includi_motore(dest)

    # stato/ pulito
    (dest / "stato").mkdir(parents=True, exist_ok=True)
    (dest / "stato" / "progressi.md").write_text(_progressi(slugs), encoding="utf-8")
    (dest / "stato" / "preferenze.md").write_text(
        "# Preferenze\n\nTono e metodo: (si impostano man mano).\n", encoding="utf-8"
    )
    (dest / "stato" / "diario.md").write_text(
        "# Diario\n\n- cartella di studio pronta per iniziare\n", encoding="utf-8"
    )

    # materie scelte, con progressi azzerati
    for slug in slugs:
        s = materie_src / slug
        d = dest / "materie" / slug
        d.mkdir(parents=True, exist_ok=True)

        if (s / "materiali").is_dir():
            shutil.copytree(s / "materiali", d / "materiali", dirs_exist_ok=True)
        else:
            (d / "materiali").mkdir(exist_ok=True)

        for nome in ("programma.md", "programma-micro.md"):
            if (s / nome).exists():
                (d / nome).write_text(
                    reset_stati((s / nome).read_text(encoding="utf-8")),
                    encoding="utf-8",
                )

        if (s / "sincronizzazione.md").exists():
            shutil.copyfile(s / "sincronizzazione.md", d / "sincronizzazione.md")

        (d / "sessione_corrente.md").write_text("", encoding="utf-8")
        (d / "domande.md").write_text("# Domande\n", encoding="utf-8")

    return dest


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 3:
        raise SystemExit(
            "Uso: prepara_condivisione.py <src_root> <dest_dir> <slug> [altri-slug...]"
        )
    src_root, dest, *slugs = argv
    prepara(src_root, dest, slugs)
    print(f"✓ pacchetto autonomo pronto in: {dest}  (materie: {', '.join(slugs)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
