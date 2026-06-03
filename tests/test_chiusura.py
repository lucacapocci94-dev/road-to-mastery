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
