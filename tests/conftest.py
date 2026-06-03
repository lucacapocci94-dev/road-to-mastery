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
    _run(tmp_path, "git", "config", "commit.gpgsign", "false")
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
