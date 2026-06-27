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


def _obiettivo(progressi_text):
    """Estrae il blocco '## Obiettivo attivo' da progressi.md, se presente."""
    righe = progressi_text.splitlines()
    out = []
    dentro = False
    for r in righe:
        if r.strip().lower().startswith("## obiettivo attivo"):
            dentro = True
            out.append(r)
            continue
        if dentro:
            if r.startswith("## "):  # inizio di un'altra sezione → stop
                break
            out.append(r)
    testo = "\n".join(out).strip()
    return testo or None


def _diario_recente(root, max_righe=14):
    """Ultime tappe leggibili dal diario di studio (il blocco di date più recente).

    Il diario è la tracciabilità in chiaro: lo aggiornano le skill, lo rilegge
    l'avvio così lo studente sa subito 'dove sono rimasto', anche senza git.
    """
    testo = _read(os.path.join(root, "stato", "diario.md")).strip()
    if not testo:
        return None
    righe = [r for r in testo.splitlines() if r.strip()]
    # salta l'intestazione e le note introduttive (citazioni '>')
    corpo = [r for r in righe if not r.lstrip().startswith(">")]
    # tieni dalla prima riga-data (## o '- [') in poi, al massimo max_righe
    inizio = 0
    for i, r in enumerate(corpo):
        if r.startswith("## ") or r.lstrip().startswith("- ["):
            inizio = i
            break
    estratto = corpo[inizio:inizio + max_righe]
    return "\n".join(estratto).strip() or None


def _ultimo_salvataggio(root):
    """Ultimo salvataggio git registrato (se lo studente usa git), in chiaro."""
    log = _read(os.path.join(root, ".road-to-mastery.log")).strip()
    if not log:
        return None
    ok = [r for r in log.splitlines() if "OK:" in r]
    return ok[-1].strip() if ok else None


def build_context(root):
    progressi_path = os.path.join(root, "stato", "progressi.md")
    if not os.path.exists(progressi_path):
        return (
            "## Road to Mastery\n"
            "Questa cartella non è ancora configurata come percorso di studio.\n"
            "Avvia **/organizza** (parti dal syllabus) o **/obiettivo** (parti dal "
            "risultato che vuoi e dalla scadenza) per crearla.\n"
        )

    progressi_text = _read(progressi_path).strip()
    parti = ["## Road to Mastery — stato caricato\n"]

    # Sessioni orfane: vanno riconciliate PRIMA di ogni altra cosa → in cima.
    aperte = []
    for sess in sorted(glob.glob(os.path.join(root, "materie", "*", "sessione_corrente.md"))):
        if _read(sess).strip():
            materia = os.path.basename(os.path.dirname(sess))
            aperte.append(materia)
    if aperte:
        parti.append("\n### ⚠ RICONCILIA PRIMA DI TUTTO (obbligatorio)\n")
        for materia in aperte:
            parti.append(
                f"- C'è una sessione non consolidata in **{materia}** "
                f"(`materie/{materia}/sessione_corrente.md`). "
                "Riversala in `stato/progressi.md`, aggiungi la tappa a "
                "`stato/diario.md` e svuotala, **prima** di rispondere ad altro.\n"
            )

    obiettivo = _obiettivo(progressi_text)
    if obiettivo:
        parti.append("\n### 🎯 Obiettivo attivo (tienilo davanti agli occhi)\n")
        parti.append(obiettivo + "\n")

    tappe = _diario_recente(root)
    if tappe:
        parti.append("\n### 🗒️ Dove sei arrivato (ultime tappe dal diario)\n")
        parti.append(tappe + "\n")

    parti.append("\n### stato/progressi.md\n")
    parti.append(progressi_text + "\n")

    salvataggio = _ultimo_salvataggio(root)
    if salvataggio:
        parti.append(f"\n_Salvataggio automatico: {salvataggio}_\n")

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
    # lo impostiamo sulla lezione aperta così la sessione è ritrovabile —
    # MA solo se la sessione non ha già un nome esplicito (dato a mano dallo
    # studente con --name o /rename): un titolo scelto a mano non va mai
    # sovrascritto.
    if source in ("", "startup", "resume") and not (data.get("session_title") or "").strip():
        titolo = session_title(root)
        if titolo:
            output["hookSpecificOutput"]["sessionTitle"] = titolo

    json.dump(output, sys.stdout, ensure_ascii=False)
    sys.exit(0)


if __name__ == "__main__":
    main()
