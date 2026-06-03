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
