"""Test del preparatore di pacchetti da condividere."""
import importlib

pc = importlib.import_module("prepara_condivisione")


def test_reset_stati_azzera_i_progressi():
    testo = (
        "- 1.1a ✓ completata\n"
        "- 1.1b ⚠ punto debole\n"
        "- 1.2a ↻ da rivedere\n"
        "- 1.2b ○ da fare ⭐\n"
    )
    out = pc.reset_stati(testo)
    assert "completata" not in out
    assert "punto debole" not in out
    assert "da rivedere" not in out
    assert out.count("○ da fare") == 4  # tutte a "da fare"
    assert "⭐" in out                   # la priorità sul syllabus resta


def _studente(tmp_path):
    """Cartella-studente finta con due materie e progressi sparsi."""
    for slug, prog in (("diritto", "- 1.1a ✓ completata\n"), ("storia", "- 1.1a ○ da fare\n")):
        m = tmp_path / "materie" / slug
        (m / "materiali").mkdir(parents=True)
        (m / "materiali" / "syllabus.md").write_text("# Syllabus\n")
        (m / "programma.md").write_text(f"# Programma\n{prog}")
        (m / "programma-micro.md").write_text(f"# Micro\n{prog}")
        (m / "sincronizzazione.md").write_text("# Sync\n")
        (m / "sessione_corrente.md").write_text("roba aperta")
        (m / "domande.md").write_text("# Domande\nQ1 sbagliata\n")
    (tmp_path / "stato").mkdir()
    (tmp_path / "stato" / "progressi.md").write_text("Materia attiva: diritto\n80%\npunti deboli: tanti\n")
    return tmp_path


def test_pacchetto_solo_materia_scelta_e_pulito(tmp_path):
    src = _studente(tmp_path / "src")
    dest = tmp_path / "pkg"
    pc.prepara(src, dest, ["diritto"])

    # solo la materia scelta
    assert (dest / "materie" / "diritto").is_dir()
    assert not (dest / "materie" / "storia").exists()

    # progressi azzerati nel programma
    assert "completata" not in (dest / "materie" / "diritto" / "programma.md").read_text()

    # niente dati personali: sessione vuota, domande resettate, stato pulito
    assert (dest / "materie" / "diritto" / "sessione_corrente.md").read_text() == ""
    assert "sbagliata" not in (dest / "materie" / "diritto" / "domande.md").read_text()
    prog = (dest / "stato" / "progressi.md").read_text()
    assert "80%" not in prog and "0%" in prog

    # syllabus e mappa di copertura mantenuti
    assert (dest / "materie" / "diritto" / "materiali" / "syllabus.md").exists()
    assert (dest / "materie" / "diritto" / "sincronizzazione.md").exists()


def test_pacchetto_include_il_motore_autonomo(tmp_path):
    src = _studente(tmp_path / "src")
    dest = tmp_path / "pkg"
    pc.prepara(src, dest, ["diritto"])

    # motore incluso + marketplace locale + hook + settings
    assert (dest / "plugins" / "road-to-mastery" / ".claude-plugin" / "plugin.json").exists()
    assert (dest / ".claude-plugin" / "marketplace.json").exists()
    hook = dest / ".claude" / "hooks" / "session-start.sh"
    assert hook.exists()
    settings = (dest / ".claude" / "settings.json").read_text()
    assert "road-to-mastery@road-to-mastery" in settings
    assert "session-start.sh" in settings


def test_materia_inesistente_fallisce(tmp_path):
    src = _studente(tmp_path / "src")
    try:
        pc.prepara(src, tmp_path / "pkg", ["inesistente"])
        assert False, "doveva fallire"
    except SystemExit:
        pass
