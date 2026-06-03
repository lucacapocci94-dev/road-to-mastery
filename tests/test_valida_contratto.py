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
