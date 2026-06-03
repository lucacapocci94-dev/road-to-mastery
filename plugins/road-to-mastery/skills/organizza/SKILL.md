---
name: organizza
description: Bootstrap completo della cartella-studente per qualsiasi esame. Intervista breve (nome, esame, data, syllabus), crea la struttura del contratto del file system, genera programma.md e programma-micro.md con ricerca web e controllo di copertura, e compila il CLAUDE.md del tutor. Usala alla prima configurazione o per aggiungere una nuova materia.
---

# /organizza — Allestire la cartella di studio

`/organizza` non genera solo un programma: **allestisce** la cartella perché si
auto-sostenga nel tempo. Funziona in due casi:

- **Prima configurazione** (la cartella non ha ancora `CLAUDE.md` / `stato/`):
  crea tutto da zero e aggiunge la prima materia.
- **Cartella già configurata**: aggiunge una **nuova materia** senza toccare le
  altre.

Risolvi quale caso applicare controllando se esiste `stato/progressi.md`.

---

## Passo 0 — Salva all'ingresso (se la cartella è già configurata)

Se esiste già una materia attiva con `materie/<materia-attiva>/sessione_corrente.md`
non vuoto, consolidalo in `stato/progressi.md` e svuotalo prima di procedere.

---

## Passo 1 — Intervista breve (mai tecnica)

Chiedi, in un linguaggio naturale e caldo, solo ciò che serve:

1. **Nome** dello studente (solo alla prima configurazione).
2. **Esame / obiettivo** (es. "concorso ordinario primaria", "maturità",
   "esame di anatomia").
3. **Data della prova** (anche approssimativa).
4. **Materia** da preparare adesso e, se ce l'ha, il **syllabus / programma
   ufficiale** (testo, foto, link, o nome del bando/corso).

Non chiedere mai operazioni su file o cartelle: a quelle pensi tu.

---

## Passo 2 — Ricerca web obbligatoria sul syllabus

Prima di generare qualsiasi struttura, cerca sul web il programma ufficiale e i
contenuti d'esame aggiornati:

```
WebSearch: "[esame] [materia] programma ufficiale syllabus aggiornato [anno]"
WebSearch: "[esame] [materia] argomenti d'esame domande frequenti [anno]"
```

Mai costruire un programma a memoria.

---

## Passo 3 — Crea la struttura del contratto del file system

Crea (solo ciò che manca):

```
CLAUDE.md                      ← dal template del plugin (Passo 5)
stato/
├── progressi.md               ← registro globale (materia attiva, %, punti deboli, calendario ripassi)
└── preferenze.md              ← tono/metodo dello studente
materie/<slug-materia>/
├── materiali/                 ← qui va SOLO il syllabus ufficiale (leggero)
├── programma.md               ← struttura standard (no contenuti)
├── programma-micro.md         ← stessa struttura, in micro-lezioni 5-10 min
├── sessione_corrente.md       ← vuoto all'inizio
├── domande.md                 ← vuoto all'inizio
└── sincronizzazione.md        ← mappa syllabus ↔ lezioni
```

Lo `<slug-materia>` è una versione semplice e minuscola del nome (es.
"Diritto costituzionale" → `diritto-costituzionale`).

---

## Passo 4 — Genera i programmi con controllo di copertura

1. Dal syllabus, costruisci `materie/<slug>/programma.md`: moduli → lezioni, con
   priorità ⭐ sui temi più probabili all'esame. **Solo struttura, niente contenuti.**
2. Scorpora la stessa struttura in `programma-micro.md`: micro-lezioni da 5-10
   minuti, dense ed esaustive (lo studio si fa nei ritagli di tempo — non devono
   restare buchi).
3. **Controllo di copertura**: in `sincronizzazione.md` mappa ogni punto del
   syllabus su ≥1 micro-lezione. Se un punto resta scoperto, segnalalo
   esplicitamente e aggiungi la micro-lezione mancante.

Codifica lezioni in modo coerente (es. `1.1a`, `1.1b`, …). Stato iniziale `○ da fare`.

---

## Passo 5 — Genera il CLAUDE.md del tutor

Alla prima configurazione, compila il template del plugin
(`${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md.template`) sostituendo
`{{NOME}}`, `{{ESAME}}`, `{{DATA_ESAME}}`, e salvalo come `CLAUDE.md` nella radice
della cartella-studente. Da quel momento, ogni volta che lo studente apre Claude
in quella cartella, l'ambiente è già un tutor configurato per lui.

---

## Passo 6 — Inizializza `stato/progressi.md`

Registra: materie presenti, **materia attiva** (= quella appena creata),
percentuali a 0, sezione "Punti deboli" vuota, **Modalità attiva: micro**, e un
**Calendario ripassi** (ripasso dilazionato a 1, 3, 7, 16, 35 giorni dopo la
prima padronanza di ogni lezione).

---

## Passo 7 — Verifica e chiusura

- Esegui il validatore del contratto come guardia di coerenza:
  `python3 ${CLAUDE_PLUGIN_ROOT}/tools/valida_contratto.py .`
- Mostra un riepilogo breve: materia creata, numero di moduli/micro-lezioni,
  eventuali punti del syllabus che richiedono attenzione.

📍 Adesso puoi:
- iniziare a studiare con `/tutor`
- vedere il programma con `/programma`
- testare ciò che già sai con `/testa`
