"""Hook SessionStart — carica lo stato nel contesto e segnala sessioni orfane.

È l'UNICO hook il cui stdout viene iniettato nel contesto del modello: quindi
qui stampiamo ciò che il modello deve sapere all'avvio (anche dopo una
compattazione, quando SessionStart riparte con source='compact').
"""
import glob
import json
import os
import sys


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def build_context(root):
    progressi_path = os.path.join(root, "stato", "progressi.md")
    if not os.path.exists(progressi_path):
        return (
            "## Road to Mastery\n"
            "Questa cartella non è ancora configurata come percorso di studio.\n"
            "Avvia **/organizza** per creare programma e file di stato.\n"
        )

    parti = ["## Road to Mastery — stato caricato\n"]
    parti.append("### stato/progressi.md\n")
    parti.append(_read(progressi_path).strip() + "\n")

    aperte = []
    for sess in sorted(glob.glob(os.path.join(root, "materie", "*", "sessione_corrente.md"))):
        if _read(sess).strip():
            materia = os.path.basename(os.path.dirname(sess))
            aperte.append(materia)

    if aperte:
        parti.append("\n### ⚠ RICONCILIA prima di tutto\n")
        for materia in aperte:
            parti.append(
                f"- C'è una sessione non consolidata in **{materia}** "
                f"(`materie/{materia}/sessione_corrente.md`). "
                "Riversala in `stato/progressi.md` e svuotala prima di procedere.\n"
            )

    return "".join(parti)


def session_title(root):
    """Titolo da dare alla sessione = la lezione aperta, per ritrovarla dopo.

    Claude Code consente di impostare il titolo solo dall'hook SessionStart
    (avvio/resume): non esiste rinomina a metà sessione. Quindi titoliamo la
    sessione sulla lezione registrata in `sessione_corrente.md`, così quando lo
    studente riapre quella sessione la trova col nome della lezione.

    Prende la prima riga descrittiva di ogni `sessione_corrente.md` non vuota,
    ripulita dagli ornamenti markdown. Una sola sessione aperta → quella; più
    di una → le concatena. Restituisce None se non c'è nulla di aperto.
    """
    titoli = []
    for sess in sorted(glob.glob(os.path.join(root, "materie", "*", "sessione_corrente.md"))):
        testo = _read(sess).strip()
        if not testo:
            continue
        materia = os.path.basename(os.path.dirname(sess))
        prima = next((r.strip() for r in testo.splitlines() if r.strip()), "")
        prima = prima.lstrip("#").strip().lstrip("-*").strip().replace("**", "").strip()
        titoli.append(f"{materia}: {prima}" if prima else materia)
    if not titoli:
        return None
    return " · ".join(titoli)[:70].rstrip()


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        data = {}
    root = data.get("cwd") or os.getcwd()
    source = data.get("source", "")

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": build_context(root),
        }
    }
    # sessionTitle è onorato solo per startup/resume (ignorato su clear/compact):
    # lo impostiamo sulla lezione aperta così la sessione è ritrovabile.
    if source in ("", "startup", "resume"):
        titolo = session_title(root)
        if titolo:
            output["hookSpecificOutput"]["sessionTitle"] = titolo

    json.dump(output, sys.stdout, ensure_ascii=False)
    sys.exit(0)


if __name__ == "__main__":
    main()
