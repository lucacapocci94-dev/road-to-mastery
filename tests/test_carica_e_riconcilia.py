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
