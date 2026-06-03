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
