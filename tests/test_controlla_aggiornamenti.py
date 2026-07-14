"""Test della logica pura di controlla_aggiornamenti (niente rete)."""
import importlib

ca = importlib.import_module("controlla_aggiornamenti")

CHANGELOG = """# Changelog — road-to-mastery

## 0.9.0
- Nuovo comando `/aggiornami`.

## 0.8.0
- Nuovo comando `/rinnova`.

## Versioni precedenti
La storia è nei commit.
"""


def test_parse_version_tollerante():
    assert ca.parse_version("1.2.3") == (1, 2, 3)
    assert ca.parse_version("0.9") == (0, 9, 0)
    assert ca.parse_version("2.0.0-beta") == (2, 0, 0)
    assert ca.parse_version("") == (0, 0, 0)


def test_confronto_versioni():
    assert ca.parse_version("0.9.0") > ca.parse_version("0.8.0")
    assert ca.parse_version("0.10.0") > ca.parse_version("0.9.0")
    assert not ca.parse_version("0.8.0") > ca.parse_version("0.8.0")


def test_novita_solo_versioni_piu_alte():
    novita = ca.novita_dal_changelog("0.8.0", CHANGELOG)
    assert "0.9.0" in novita
    assert "/aggiornami" in novita
    # non deve includere la 0.8.0 (uguale al locale) né le sezioni non-versione
    assert "0.8.0" not in novita
    assert "Versioni precedenti" not in novita


def test_novita_vuote_se_gia_aggiornato():
    assert ca.novita_dal_changelog("0.9.0", CHANGELOG) == ""
