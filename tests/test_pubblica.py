"""Test della logica pura di scripts/pubblica.py (niente git, niente rete)."""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
pub = importlib.import_module("pubblica")


def test_bump_version():
    assert pub.bump_version("0.8.0", "patch") == "0.8.1"
    assert pub.bump_version("0.8.0", "minor") == "0.9.0"
    assert pub.bump_version("0.8.3", "minor") == "0.9.0"  # azzera il patch
    assert pub.bump_version("0.8.3", "major") == "1.0.0"  # azzera minor e patch


def test_blocco_changelog_con_righe():
    blocco = pub.blocco_changelog("0.9.0", ["prima novità", "seconda"])
    assert blocco.startswith("## 0.9.0 — ")
    assert "- prima novità" in blocco
    assert "- seconda" in blocco


def test_blocco_changelog_vuoto():
    assert "- Aggiornamenti vari." in pub.blocco_changelog("0.9.0", [])


def test_aggiorna_changelog_inserisce_in_cima(tmp_path, monkeypatch):
    ch = tmp_path / "CHANGELOG.md"
    ch.write_text(
        "# Changelog — road-to-mastery\n\n## 0.8.0 — 2026-01-01\n- vecchia.\n"
    )
    monkeypatch.setattr(pub, "CHANGELOG", ch)
    pub.aggiorna_changelog("0.9.0", ["nuova"])
    testo = ch.read_text()
    # la sezione nuova precede quella vecchia e l'intestazione resta in testa
    assert testo.index("# Changelog") < testo.index("## 0.9.0")
    assert testo.index("## 0.9.0") < testo.index("## 0.8.0")
    assert "- nuova" in testo
