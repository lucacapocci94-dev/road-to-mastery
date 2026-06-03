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
