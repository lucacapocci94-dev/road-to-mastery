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


def test_titolo_nessuna_sessione_aperta(studente):
    assert h.session_title(str(studente)) is None


def test_titolo_da_lezione_aperta(studente):
    (studente / "materie" / "matematica" / "sessione_corrente.md").write_text(
        "# Lezione 3.2a — Le frazioni equivalenti\nPunto: inizio\n"
    )
    titolo = h.session_title(str(studente))
    assert titolo == "matematica: Lezione 3.2a — Le frazioni equivalenti"


def test_titolo_piu_sessioni_aperte(studente):
    (studente / "materie" / "matematica" / "sessione_corrente.md").write_text(
        "# Lezione 3.2a — Le frazioni\n"
    )
    storia = studente / "materie" / "storia"
    storia.mkdir()
    (storia / "sessione_corrente.md").write_text("# Lezione 1.1a — Roma\n")
    titolo = h.session_title(str(studente))
    assert "matematica: Lezione 3.2a — Le frazioni" in titolo
    assert "storia: Lezione 1.1a — Roma" in titolo
    assert " · " in titolo
