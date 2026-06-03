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


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        data = {}
    root = data.get("cwd") or os.getcwd()
    sys.stdout.write(build_context(root))
    sys.exit(0)


if __name__ == "__main__":
    main()
