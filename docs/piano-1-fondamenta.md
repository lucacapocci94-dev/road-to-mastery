# Road to Mastery — Piano 1: Fondamenta del plugin

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Costruire (in staging dentro questo repo) un plugin Claude Code installabile che fornisce il motore-tutor: i 3 hook del motore, un validatore del contratto del file system, e i template di bootstrap — tutto testato con pytest.

**Architecture:** Il plugin vive in `road-to-mastery/` (cartella di staging su questo branch; diventerà il contenuto del nuovo repo `road-to-mastery`). La cartella è insieme **marketplace** (`.claude-plugin/marketplace.json`) e contiene il **plugin** (`plugins/road-to-mastery/`). Gli hook sono script Python autonomi che condividono un modulo `gitsync.py`; sono dichiarati nel `plugin.json` e referenziati con `${CLAUDE_PLUGIN_ROOT}`. Tutta la logica è in funzioni pure testabili; gli script sono wrapper sottili. La migrazione delle skill (organizza, tutor, ecc.) è rinviata al Piano 2.

**Tech Stack:** Python 3 (hook + validatore + tool), pytest (test), JSON (manifest plugin/marketplace), Markdown (template e doc). Nessuna dipendenza esterna oltre a pytest.

---

## Struttura file (decisioni di decomposizione)

```
road-to-mastery/                              # = root del nuovo repo (marketplace)
├── .claude-plugin/
│   └── marketplace.json                      # elenca 1 plugin, source ./plugins/road-to-mastery
├── plugins/
│   └── road-to-mastery/                      # IL PLUGIN
│       ├── .claude-plugin/
│       │   └── plugin.json                   # manifest + dichiarazione hook
│       ├── scripts/
│       │   ├── gitsync.py                    # logica git "se-disponibile" (condivisa)
│       │   ├── carica_e_riconcilia.py        # hook SessionStart
│       │   ├── checkpoint.py                 # hook Stop
│       │   └── chiusura.py                   # hook SessionEnd
│       ├── tools/
│       │   └── valida_contratto.py           # validatore del contratto del file system
│       ├── templates/
│       │   └── CLAUDE.md.template            # regole-tutor generiche (usato da /organizza, Piano 2)
│       └── README.md                         # cosa fa il plugin, come si installa
├── tests/
│   ├── conftest.py                           # fixture: cartella-studente finta, repo git temporaneo
│   ├── test_gitsync.py
│   ├── test_carica_e_riconcilia.py
│   ├── test_checkpoint.py
│   ├── test_chiusura.py
│   └── test_valida_contratto.py
└── README.md                                 # cosa è il marketplace, come aggiungerlo
```

Responsabilità:
- `gitsync.py`: tutta e sola la logica git (rileva repo, commit, push se c'è upstream). Generica: pusha sul branch corrente, **non** impone `main` (quel vincolo era specifico di Mariele).
- ogni hook `*.py`: wrapper sottile che legge lo stdin JSON, ricava `cwd`, chiama la logica, esce 0.
- `valida_contratto.py`: verifica che una cartella-studente rispetti il contratto del file system (spec §3).

---

## Task 1: Layout di staging + manifest plugin e marketplace

**Files:**
- Create: `road-to-mastery/.claude-plugin/marketplace.json`
- Create: `road-to-mastery/plugins/road-to-mastery/.claude-plugin/plugin.json`
- Create: `road-to-mastery/README.md`
- Create: `road-to-mastery/plugins/road-to-mastery/README.md`

- [ ] **Step 1: Crea il manifest del plugin con i 3 hook**

`road-to-mastery/plugins/road-to-mastery/.claude-plugin/plugin.json`:

```json
{
  "name": "road-to-mastery",
  "description": "Motore-tutor: trasforma una cartella in un tutor personale per qualsiasi esame. Programmi, micro-lezioni, interrogazioni e salvataggio automatico dei progressi.",
  "version": "0.1.0",
  "author": { "name": "Luca Capocci" },
  "license": "MIT",
  "keywords": ["tutor", "studio", "esami", "concorsi", "spaced-repetition"],
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/carica_e_riconcilia.py" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/checkpoint.py" }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          { "type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/chiusura.py" }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Crea il manifest del marketplace**

`road-to-mastery/.claude-plugin/marketplace.json`:

```json
{
  "name": "road-to-mastery",
  "owner": { "name": "Luca Capocci" },
  "description": "Marketplace del motore-tutor Road to Mastery.",
  "plugins": [
    {
      "name": "road-to-mastery",
      "source": "./plugins/road-to-mastery",
      "description": "Motore-tutor per la preparazione a qualsiasi esame."
    }
  ]
}
```

- [ ] **Step 3: Crea i due README (segnaposto onesti, non vuoti)**

`road-to-mastery/README.md`:

```markdown
# Road to Mastery — Marketplace

Marketplace Claude Code che ospita il plugin **road-to-mastery**, un motore-tutor
per la preparazione a qualsiasi esame.

## Installazione

```
/plugin marketplace add lucacapocci94-dev/road-to-mastery
/plugin install road-to-mastery@road-to-mastery
```

Aggiornamenti: `/plugin update`.

Il plugin vive in `plugins/road-to-mastery/`.
```

`road-to-mastery/plugins/road-to-mastery/README.md`:

```markdown
# road-to-mastery (plugin)

Motore-tutor distribuibile. Fornisce:

- **3 hook** che salvano i progressi e ricaricano lo stato a ogni sessione
  (anche dopo una compattazione del contesto), indipendentemente da git.
- **Contratto del file system**: dove vivono programmi, stato e materie.
- **Validatore** del contratto (`tools/valida_contratto.py`).

Le skill (`/organizza`, `/tutor`, `/testa`, …) arrivano nel Piano 2.

## Hook

| Hook | Evento | Cosa fa |
|---|---|---|
| `carica_e_riconcilia.py` | SessionStart | inietta lo stato nel contesto; segnala sessioni non consolidate |
| `checkpoint.py` | Stop | commit + push (se git disponibile) di `stato/` e `materie/` |
| `chiusura.py` | SessionEnd | consolidamento finale + push di sicurezza |
```

- [ ] **Step 4: Valida i JSON**

Run: `python3 -c "import json; json.load(open('road-to-mastery/.claude-plugin/marketplace.json')); json.load(open('road-to-mastery/plugins/road-to-mastery/.claude-plugin/plugin.json')); print('JSON OK')"`
Expected: stampa `JSON OK` senza eccezioni.

- [ ] **Step 5: Commit**

```bash
git add road-to-mastery/.claude-plugin road-to-mastery/plugins/road-to-mastery/.claude-plugin road-to-mastery/README.md road-to-mastery/plugins/road-to-mastery/README.md
git commit -m "feat(plugin): scaffold marketplace e manifest road-to-mastery"
```

---

## Task 2: `gitsync.py` — logica git "se-disponibile" (condivisa)

**Files:**
- Create: `road-to-mastery/plugins/road-to-mastery/scripts/gitsync.py`
- Test: `road-to-mastery/tests/conftest.py`, `road-to-mastery/tests/test_gitsync.py`

- [ ] **Step 1: Crea le fixture di test**

`road-to-mastery/tests/conftest.py`:

```python
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "road-to-mastery" / "scripts"
TOOLS = Path(__file__).resolve().parents[1] / "plugins" / "road-to-mastery" / "tools"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(TOOLS))


def _run(cwd, *args):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


@pytest.fixture
def non_git_dir(tmp_path):
    """Una cartella che NON è un repo git."""
    return tmp_path


@pytest.fixture
def git_repo(tmp_path):
    """Un repo git inizializzato, senza remote."""
    _run(tmp_path, "git", "init", "-q")
    _run(tmp_path, "git", "config", "user.email", "t@t.t")
    _run(tmp_path, "git", "config", "user.name", "Test")
    (tmp_path / "seed.txt").write_text("seed\n")
    _run(tmp_path, "git", "add", "seed.txt")
    _run(tmp_path, "git", "commit", "-q", "-m", "seed")
    return tmp_path


@pytest.fixture
def studente(tmp_path):
    """Cartella-studente conforme al contratto del file system (spec §3)."""
    (tmp_path / "stato").mkdir()
    (tmp_path / "stato" / "progressi.md").write_text("# Progressi\nMateria attiva: matematica\n")
    (tmp_path / "stato" / "preferenze.md").write_text("# Preferenze\n")
    mat = tmp_path / "materie" / "matematica"
    (mat / "materiali").mkdir(parents=True)
    (mat / "programma.md").write_text("# Programma\n")
    (mat / "programma-micro.md").write_text("# Programma micro\n")
    (mat / "sessione_corrente.md").write_text("")
    (mat / "domande.md").write_text("# Domande\n")
    (mat / "sincronizzazione.md").write_text("# Sincronizzazione\n")
    (tmp_path / "CLAUDE.md").write_text("# Tutor\n")
    return tmp_path
```

- [ ] **Step 2: Scrivi i test che falliscono**

`road-to-mastery/tests/test_gitsync.py`:

```python
import gitsync


def test_repo_root_none_se_non_git(non_git_dir):
    assert gitsync.repo_root(str(non_git_dir)) is None


def test_repo_root_trova_radice(git_repo):
    assert gitsync.repo_root(str(git_repo)) == str(git_repo)


def test_checkpoint_no_op_se_non_git(non_git_dir):
    # Non deve sollevare eccezioni né creare nulla.
    gitsync.checkpoint(str(non_git_dir), ["stato"], msg="x")


def test_checkpoint_committa_file_modificati(git_repo):
    (git_repo / "stato").mkdir()
    (git_repo / "stato" / "progressi.md").write_text("nuovo\n")
    gitsync.checkpoint(str(git_repo), ["stato"], msg="aggiorna stato")
    import subprocess
    out = subprocess.run(
        ["git", "log", "--oneline", "-1"], cwd=git_repo, capture_output=True, text=True
    ).stdout
    assert "aggiorna stato" in out


def test_checkpoint_no_commit_se_nulla_cambia(git_repo):
    before = _head(git_repo)
    gitsync.checkpoint(str(git_repo), ["stato"], msg="vuoto")
    assert _head(git_repo) == before


def _head(repo):
    import subprocess
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
```

- [ ] **Step 3: Esegui i test per verificare che falliscano**

Run: `cd road-to-mastery && python3 -m pytest tests/test_gitsync.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'gitsync'` (il modulo non esiste ancora).

- [ ] **Step 4: Implementa `gitsync.py`**

`road-to-mastery/plugins/road-to-mastery/scripts/gitsync.py`:

```python
"""Logica git 'se-disponibile' condivisa dagli hook.

Principi:
- Se la cartella non è un repo git → no-op pulito (lo studente può non usare git).
- I file locali sono la verità primaria; git è solo copia di sicurezza.
- Pusha sul branch CORRENTE (non impone 'main') e solo se esiste un upstream.
- Non solleva mai: ogni fallimento è loggato, l'hook deve poter uscire 0.
"""
import os
import subprocess
from datetime import datetime


def _run(cwd, *args):
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True)


def repo_root(cwd):
    """Radice del repo git che contiene cwd, oppure None se non è un repo."""
    res = _run(cwd, "git", "rev-parse", "--show-toplevel")
    if res.returncode != 0:
        return None
    return res.stdout.strip()


def _log(root, msg):
    try:
        with open(os.path.join(root, ".road-to-mastery.log"), "a") as f:
            f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n")
    except OSError:
        pass


def _has_upstream(root):
    return _run(root, "git", "rev-parse", "--abbrev-ref", "@{u}").returncode == 0


def checkpoint(cwd, paths, msg):
    """Commit (e push se possibile) dei `paths` esistenti dentro il repo.

    No-op se cwd non è un repo git. Best-effort: logga e prosegue su ogni errore.
    """
    root = repo_root(cwd)
    if root is None:
        return

    existing = [p for p in paths if os.path.exists(os.path.join(root, p))]
    if not existing:
        return
    _run(root, "git", "add", *existing)

    if _run(root, "git", "diff", "--cached", "--quiet").returncode == 0:
        return  # niente di nuovo da committare

    if _run(root, "git", "commit", "-m", msg).returncode != 0:
        _log(root, f"COMMIT FAIL: {msg}")
        return

    if not _has_upstream(root):
        _log(root, "PUSH SKIP: nessun upstream configurato")
        return

    if _run(root, "git", "fetch").returncode != 0:
        _log(root, "FETCH FAIL")
        return
    if _run(root, "git", "pull", "--rebase").returncode != 0:
        _log(root, "REBASE FAIL")
        _run(root, "git", "rebase", "--abort")
        return
    if _run(root, "git", "push").returncode != 0:
        _log(root, "PUSH FAIL")
        return
    _log(root, f"OK: {msg}")
```

- [ ] **Step 5: Esegui i test per verificare che passino**

Run: `cd road-to-mastery && python3 -m pytest tests/test_gitsync.py -v`
Expected: PASS (5 test verdi).

- [ ] **Step 6: Commit**

```bash
git add road-to-mastery/plugins/road-to-mastery/scripts/gitsync.py road-to-mastery/tests/conftest.py road-to-mastery/tests/test_gitsync.py
git commit -m "feat(plugin): gitsync 'se-disponibile' condiviso con test"
```

---

## Task 3: Hook `carica_e_riconcilia.py` (SessionStart)

**Files:**
- Create: `road-to-mastery/plugins/road-to-mastery/scripts/carica_e_riconcilia.py`
- Test: `road-to-mastery/tests/test_carica_e_riconcilia.py`

Comportamento: legge `cwd` dallo stdin JSON. Costruisce un blocco di contesto (stampato su stdout — l'unico hook il cui stdout raggiunge il modello) che: (a) include `stato/progressi.md` se esiste; (b) per ogni `materie/*/sessione_corrente.md` non vuoto, emette un'istruzione di RICONCILIAZIONE; (c) se la cartella è vuota, suggerisce `/organizza`. La funzione `build_context(root)` è pura e testabile; lo script è il wrapper.

- [ ] **Step 1: Scrivi i test che falliscono**

`road-to-mastery/tests/test_carica_e_riconcilia.py`:

```python
import carica_e_riconcilia as h


def test_cartella_vuota_suggerisce_organizza(tmp_path):
    ctx = h.build_context(str(tmp_path))
    assert "/organizza" in ctx


def test_include_progressi(studente):
    ctx = h.build_context(str(studente))
    assert "Materia attiva: matematica" in ctx


def test_sessione_vuota_nessuna_riconciliazione(studente):
    ctx = h.build_context(str(studente))
    assert "RICONCILIA" not in ctx


def test_sessione_aperta_chiede_riconciliazione(studente):
    (studente / "materie" / "matematica" / "sessione_corrente.md").write_text(
        "Lezione aperta: 3.2a\nPunto: inizio\n"
    )
    ctx = h.build_context(str(studente))
    assert "RICONCILIA" in ctx
    assert "matematica" in ctx
```

- [ ] **Step 2: Esegui i test per verificare che falliscano**

Run: `cd road-to-mastery && python3 -m pytest tests/test_carica_e_riconcilia.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'carica_e_riconcilia'`.

- [ ] **Step 3: Implementa l'hook**

`road-to-mastery/plugins/road-to-mastery/scripts/carica_e_riconcilia.py`:

```python
"""Hook SessionStart — carica lo stato nel contesto e segnala sessioni orfane.

È l'UNICO hook il cui stdout viene iniettato nel contesto del modello: quindi
qui stampiamo ciò che il modello deve sapere all'avvio (anche dopo una
compattazione, quando SessionStart riparte con source='compact').
"""
import glob
import json
import os
import sys


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def build_context(root):
    progressi_path = os.path.join(root, "stato", "progressi.md")
    if not os.path.exists(progressi_path):
        return (
            "## Road to Mastery\n"
            "Questa cartella non è ancora configurata come percorso di studio.\n"
            "Avvia **/organizza** per creare programma e file di stato.\n"
        )

    parti = ["## Road to Mastery — stato caricato\n"]
    parti.append("### stato/progressi.md\n")
    parti.append(_read(progressi_path).strip() + "\n")

    aperte = []
    for sess in sorted(glob.glob(os.path.join(root, "materie", "*", "sessione_corrente.md"))):
        if _read(sess).strip():
            materia = os.path.basename(os.path.dirname(sess))
            aperte.append(materia)

    if aperte:
        parti.append("\n### ⚠ RICONCILIA prima di tutto\n")
        for materia in aperte:
            parti.append(
                f"- C'è una sessione non consolidata in **{materia}** "
                f"(`materie/{materia}/sessione_corrente.md`). "
                "Riversala in `stato/progressi.md` e svuotala prima di procedere.\n"
            )

    return "".join(parti)


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        data = {}
    root = data.get("cwd") or os.getcwd()
    sys.stdout.write(build_context(root))
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Esegui i test per verificare che passino**

Run: `cd road-to-mastery && python3 -m pytest tests/test_carica_e_riconcilia.py -v`
Expected: PASS (4 test verdi).

- [ ] **Step 5: Test end-to-end dell'hook via stdin**

Run: `cd road-to-mastery && printf '{"cwd":"/tmp/nonesiste-xyz"}' | python3 plugins/road-to-mastery/scripts/carica_e_riconcilia.py; echo "EXIT=$?"`
Expected: stampa il messaggio con `/organizza` e `EXIT=0`.

- [ ] **Step 6: Commit**

```bash
git add road-to-mastery/plugins/road-to-mastery/scripts/carica_e_riconcilia.py road-to-mastery/tests/test_carica_e_riconcilia.py
git commit -m "feat(plugin): hook SessionStart carica_e_riconcilia con test"
```

---

## Task 4: Hook `checkpoint.py` (Stop)

**Files:**
- Create: `road-to-mastery/plugins/road-to-mastery/scripts/checkpoint.py`
- Test: `road-to-mastery/tests/test_checkpoint.py`

Comportamento: legge `cwd` dallo stdin, chiama `gitsync.checkpoint(cwd, ["stato", "materie"], msg)`, esce 0. Lo stdout dello Stop non raggiunge il modello: solo side-effect.

- [ ] **Step 1: Scrivi i test che falliscono**

`road-to-mastery/tests/test_checkpoint.py`:

```python
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "road-to-mastery" / "scripts" / "checkpoint.py"


def _exec(cwd):
    return subprocess.run(
        ["python3", str(SCRIPT)],
        cwd=cwd, input=f'{{"cwd":"{cwd}"}}',
        capture_output=True, text=True,
    )


def test_esce_zero_se_non_git(non_git_dir):
    assert _exec(str(non_git_dir)).returncode == 0


def test_committa_stato(git_repo):
    (git_repo / "stato").mkdir()
    (git_repo / "stato" / "progressi.md").write_text("dati\n")
    assert _exec(str(git_repo)).returncode == 0
    out = subprocess.run(
        ["git", "log", "--oneline", "-1"], cwd=git_repo, capture_output=True, text=True
    ).stdout
    assert "checkpoint" in out.lower()
```

- [ ] **Step 2: Esegui i test per verificare che falliscano**

Run: `cd road-to-mastery && python3 -m pytest tests/test_checkpoint.py -v`
Expected: FAIL (lo script non esiste → `can't open file .../checkpoint.py`, returncode ≠ 0 → assert fallisce).

- [ ] **Step 3: Implementa l'hook**

`road-to-mastery/plugins/road-to-mastery/scripts/checkpoint.py`:

```python
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
```

- [ ] **Step 4: Esegui i test per verificare che passino**

Run: `cd road-to-mastery && python3 -m pytest tests/test_checkpoint.py -v`
Expected: PASS (2 test verdi).

- [ ] **Step 5: Commit**

```bash
git add road-to-mastery/plugins/road-to-mastery/scripts/checkpoint.py road-to-mastery/tests/test_checkpoint.py
git commit -m "feat(plugin): hook Stop checkpoint con test"
```

---

## Task 5: Hook `chiusura.py` (SessionEnd)

**Files:**
- Create: `road-to-mastery/plugins/road-to-mastery/scripts/chiusura.py`
- Test: `road-to-mastery/tests/test_chiusura.py`

Comportamento: identico a `checkpoint.py` nella meccanica, ma con messaggio di "chiusura sessione" — è il backstop su uscita pulita.

- [ ] **Step 1: Scrivi il test che fallisce**

`road-to-mastery/tests/test_chiusura.py`:

```python
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "plugins" / "road-to-mastery" / "scripts" / "chiusura.py"


def _exec(cwd, reason="logout"):
    return subprocess.run(
        ["python3", str(SCRIPT)],
        cwd=cwd, input=f'{{"cwd":"{cwd}","reason":"{reason}"}}',
        capture_output=True, text=True,
    )


def test_esce_zero_se_non_git(non_git_dir):
    assert _exec(str(non_git_dir)).returncode == 0


def test_committa_a_fine_sessione(git_repo):
    (git_repo / "stato").mkdir()
    (git_repo / "stato" / "progressi.md").write_text("finale\n")
    assert _exec(str(git_repo)).returncode == 0
    out = subprocess.run(
        ["git", "log", "--oneline", "-1"], cwd=git_repo, capture_output=True, text=True
    ).stdout
    assert "chiusura" in out.lower()
```

- [ ] **Step 2: Esegui il test per verificare che fallisca**

Run: `cd road-to-mastery && python3 -m pytest tests/test_chiusura.py -v`
Expected: FAIL (script inesistente).

- [ ] **Step 3: Implementa l'hook**

`road-to-mastery/plugins/road-to-mastery/scripts/chiusura.py`:

```python
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
```

- [ ] **Step 4: Esegui il test per verificare che passi**

Run: `cd road-to-mastery && python3 -m pytest tests/test_chiusura.py -v`
Expected: PASS (2 test verdi).

- [ ] **Step 5: Commit**

```bash
git add road-to-mastery/plugins/road-to-mastery/scripts/chiusura.py road-to-mastery/tests/test_chiusura.py
git commit -m "feat(plugin): hook SessionEnd chiusura con test"
```

---

## Task 6: Validatore del contratto `valida_contratto.py`

**Files:**
- Create: `road-to-mastery/plugins/road-to-mastery/tools/valida_contratto.py`
- Test: `road-to-mastery/tests/test_valida_contratto.py`

Comportamento: `problemi(root)` ritorna la lista dei problemi (stringhe) rispetto al contratto (spec §3). `main()` stampa i problemi ed esce 0 se conforme, 1 altrimenti. Verifica: `CLAUDE.md`, `stato/progressi.md`, `stato/preferenze.md`, e per ogni `materie/<slug>/` la presenza di `materiali/`, `programma.md`, `programma-micro.md`, `sessione_corrente.md`, `domande.md`, `sincronizzazione.md`. Almeno una materia deve esistere.

- [ ] **Step 1: Scrivi i test che falliscono**

`road-to-mastery/tests/test_valida_contratto.py`:

```python
import valida_contratto as v


def test_studente_conforme_nessun_problema(studente):
    assert v.problemi(str(studente)) == []


def test_manca_progressi(studente):
    (studente / "stato" / "progressi.md").unlink()
    probs = v.problemi(str(studente))
    assert any("progressi.md" in p for p in probs)


def test_manca_file_materia(studente):
    (studente / "materie" / "matematica" / "domande.md").unlink()
    probs = v.problemi(str(studente))
    assert any("domande.md" in p and "matematica" in p for p in probs)


def test_nessuna_materia(tmp_path):
    (tmp_path / "stato").mkdir()
    (tmp_path / "stato" / "progressi.md").write_text("x")
    (tmp_path / "stato" / "preferenze.md").write_text("x")
    (tmp_path / "CLAUDE.md").write_text("x")
    probs = v.problemi(str(tmp_path))
    assert any("nessuna materia" in p.lower() for p in probs)
```

- [ ] **Step 2: Esegui i test per verificare che falliscano**

Run: `cd road-to-mastery && python3 -m pytest tests/test_valida_contratto.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'valida_contratto'`.

- [ ] **Step 3: Implementa il validatore**

`road-to-mastery/plugins/road-to-mastery/tools/valida_contratto.py`:

```python
"""Verifica che una cartella-studente rispetti il contratto del file system
(Road to Mastery, spec §3).

Uso: python3 valida_contratto.py [cartella]   (default: cartella corrente)
Esce 0 se conforme, 1 se ci sono problemi.
"""
import os
import sys

FILE_GLOBALI = ["CLAUDE.md", "stato/progressi.md", "stato/preferenze.md"]
FILE_MATERIA = [
    "materiali",
    "programma.md",
    "programma-micro.md",
    "sessione_corrente.md",
    "domande.md",
    "sincronizzazione.md",
]


def problemi(root):
    out = []
    for rel in FILE_GLOBALI:
        if not os.path.exists(os.path.join(root, rel)):
            out.append(f"manca: {rel}")

    materie_dir = os.path.join(root, "materie")
    materie = []
    if os.path.isdir(materie_dir):
        materie = [d for d in os.listdir(materie_dir)
                   if os.path.isdir(os.path.join(materie_dir, d))]

    if not materie:
        out.append("nessuna materia: serve almeno una cartella in materie/<slug>/")

    for m in materie:
        for rel in FILE_MATERIA:
            if not os.path.exists(os.path.join(materie_dir, m, rel)):
                out.append(f"manca: materie/{m}/{rel}")

    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    probs = problemi(root)
    if not probs:
        print("✓ Contratto rispettato.")
        sys.exit(0)
    print("✗ Problemi nel contratto del file system:")
    for p in probs:
        print(f"  - {p}")
    sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Esegui i test per verificare che passino**

Run: `cd road-to-mastery && python3 -m pytest tests/test_valida_contratto.py -v`
Expected: PASS (4 test verdi).

- [ ] **Step 5: Commit**

```bash
git add road-to-mastery/plugins/road-to-mastery/tools/valida_contratto.py road-to-mastery/tests/test_valida_contratto.py
git commit -m "feat(plugin): validatore del contratto del file system con test"
```

---

## Task 7: Template `CLAUDE.md` generico (bootstrap)

**Files:**
- Create: `road-to-mastery/plugins/road-to-mastery/templates/CLAUDE.md.template`

Questo template sarà copiato e compilato da `/organizza` (Piano 2) nella cartella
dello studente. Usa segnaposto `{{NOME}}`, `{{ESAME}}`, `{{DATA_ESAME}}`. Contiene
le regole-tutor **generiche** (non legate a Mariele).

- [ ] **Step 1: Crea il template**

`road-to-mastery/plugins/road-to-mastery/templates/CLAUDE.md.template`:

```markdown
# {{ESAME}} — Tutor personale di {{NOME}}

## Chi sei
Sei il tutor personale di **{{NOME}}**, in preparazione per: {{ESAME}}.
Data della prova: **{{DATA_ESAME}}**.

## Regole fondamentali — non derogabili
1. **Italiano sempre** (tranne quando è attiva una modalità lingua dedicata).
2. **Ricerca web obbligatoria** prima di spiegare qualsiasi concetto o porre
   domande di studio. Mai rispondere a memoria su contenuti didattici/normativi.
3. **Salvataggio silenzioso**: aggiorna i file in `stato/` e `materie/` senza
   commentarlo e senza chiedere permesso.
4. **Nessuna domanda tecnica** allo studente su file, cartelle o impostazioni.
5. **Salva all'ingresso**: prima di ogni comando, se c'è una sessione aperta in
   `materie/<materia-attiva>/sessione_corrente.md`, consolidala in
   `stato/progressi.md` e svuotala. Solo dopo procedi.
6. **Mai assumere la prossima lezione**: leggi sempre `programma-micro.md` (o
   `programma.md`) della materia attiva per trovare la lezione successiva.

## Contratto del file system
- `stato/progressi.md` — registro globale: materie, **materia attiva**, %, punti
  deboli, calendario ripassi.
- `stato/preferenze.md` — tono e metodo preferiti dallo studente.
- `materie/<slug>/` — tutto ciò che riguarda una materia (programmi, sessione
  corrente, domande, sincronizzazione, materiali). Mai mescolare materie.

## Materia attiva
Ogni comando risolve la materia così: argomento esplicito → materia attiva in
`progressi.md` → in mancanza, chiedi. **Mai indovinare.**
```

- [ ] **Step 2: Verifica che i segnaposto siano coerenti**

Run: `cd road-to-mastery && grep -o '{{[A-Z_]*}}' plugins/road-to-mastery/templates/CLAUDE.md.template | sort -u`
Expected: stampa esattamente `{{DATA_ESAME}}`, `{{ESAME}}`, `{{NOME}}`.

- [ ] **Step 3: Commit**

```bash
git add road-to-mastery/plugins/road-to-mastery/templates/CLAUDE.md.template
git commit -m "feat(plugin): template CLAUDE.md generico per il bootstrap"
```

---

## Task 8: Verifica finale dell'insieme

**Files:** nessuno nuovo (solo verifica).

- [ ] **Step 1: Tutta la suite verde**

Run: `cd road-to-mastery && python3 -m pytest -v`
Expected: PASS su tutti i test (gitsync, carica_e_riconcilia, checkpoint, chiusura, valida_contratto).

- [ ] **Step 2: Validazione del plugin con la CLI (se disponibile)**

Run: `cd road-to-mastery && claude plugin validate . 2>&1 || echo "CLI non disponibile in questo ambiente — salto"`
Expected: o un esito di validazione positivo, o il messaggio di salto (l'ambiente potrebbe non avere la CLI `claude`).

- [ ] **Step 3: Validatore su una cartella-studente reale (questo repo)**

Run: `python3 road-to-mastery/plugins/road-to-mastery/tools/valida_contratto.py . 2>&1 | head -20`
Expected: elenca i problemi (questo repo NON è ancora migrato al contratto multi-materia: è atteso che riporti differenze; serve a confermare che il validatore gira e produce output sensato).

- [ ] **Step 4: Commit finale di stato**

```bash
git add -A road-to-mastery
git commit -m "chore(plugin): verifica finale fondamenta road-to-mastery" || echo "niente da committare"
```

---

## Note di handoff verso il Piano 2

Il Piano 2 (migrazione skill) costruirà, dentro `plugins/road-to-mastery/skills/`,
le versioni generiche e materia-aware di: `organizza` (bootstrap completo: crea la
struttura del contratto, genera i programmi con controllo di copertura, compila il
template CLAUDE.md), `tutor`, `testa`, `interrogazione`, `simulazione`, `modalita`,
`programma`, `avanzamento`, `help`. Ogni skill avrà una `description` ricca nel
frontmatter (per l'autocompletamento dello slash) e userà il validatore di Task 6
come guardia di coerenza.

Trapianto nel repo nuovo: quando `road-to-mastery` esiste su GitHub ed è nel
perimetro della sessione, il contenuto della cartella `road-to-mastery/` di staging
diventa la radice del nuovo repo.
```
