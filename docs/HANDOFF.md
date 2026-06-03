# HANDOFF — Passaggio di consegne verso il repo `road-to-mastery`

> Questo file è il "testimone" tra due sessioni di lavoro. Una nuova sessione di
> Claude **non ricorda** la chat precedente: ricorda solo ciò che è scritto qui e
> negli altri file del repo. Leggi questo documento per intero prima di agire.

**Data redazione:** 2026-06-03
**Autore (utente):** Luca Capocci (`lucacapocci94-dev`), email `ziolums94@gmail.com`
**Lingua di lavoro con l'utente:** italiano sempre. L'utente non è tecnico: niente
gergo informatico nelle risposte.

---

## 1. Il quadro in tre frasi

Stiamo estraendo il motore-tutor da un progetto monouso ("Road to Posto Comune",
un tutor cucito su una sola candidata) e trasformandolo in un **plugin Claude Code
pubblico e riutilizzabile** chiamato `road-to-mastery`, distribuito come
**marketplace** dal repo GitHub `lucacapocci94-dev/road-to-mastery`.

Il plugin **non contiene contenuti didattici**: contiene un **motore** (hook +
skill) e un **contratto sul file system**. I contenuti si generano a runtime con
ricerca web.

Tutto il design è in `docs/design.md`. Il Piano 1 (già fatto) è in
`docs/piano-1-fondamenta.md`. Leggili: sono la fonte di verità.

---

## 2. Dove siamo (stato al 2026-06-03)

- **Piano 1 — Fondamenta del plugin: COMPLETO.** 17/17 test pytest verdi,
  `claude plugin validate` superato. Comprende:
  - scaffold marketplace + manifest (`.claude-plugin/marketplace.json`,
    `plugins/road-to-mastery/.claude-plugin/plugin.json`);
  - i 3 hook del motore (`carica_e_riconcilia.py` su SessionStart,
    `checkpoint.py` su Stop, `chiusura.py` su SessionEnd) + `gitsync.py` condiviso;
  - il validatore del contratto (`tools/valida_contratto.py`);
  - il template di bootstrap (`templates/CLAUDE.md.template`);
  - la suite di test in `tests/`.
- **Il repo `road-to-mastery` su GitHub esiste ed è (era) vuoto.** È stato creato
  dall'utente perché l'integrazione GitHub della sessione precedente non aveva il
  permesso di creare repo (403).
- **Questo contenuto vive ancora come staging** dentro l'altro repo
  (`road_to_posto_comune`), nella cartella `road-to-mastery/`, sul branch
  `claude/create-another-repo-o2hVB`.

**Quello che resta da fare adesso:** il *trapianto* (vedi §3) e poi il **Piano 2**
(vedi §5).

---

## 3. PRIMO COMPITO della nuova sessione: il trapianto

Obiettivo: il contenuto della cartella di staging `road-to-mastery/` deve diventare
la **radice** del repo `road-to-mastery`.

### Prerequisiti di scope
Perché funzioni, questa sessione deve avere nel perimetro **entrambi** i repo:
- `lucacapocci94-dev/road_to_posto_comune` (sorgente: contiene lo staging)
- `lucacapocci94-dev/road-to-mastery` (destinazione)

Se vedi solo uno dei due, fermati e dillo all'utente: non si può trapiantare a metà.

### Procedura consigliata (via git, pulita)
Lavora nella working copy di `road-to-mastery` (destinazione). Porta dentro il
contenuto della cartella di staging dal repo sorgente. In pratica:

1. Copia tutto il contenuto di `road-to-mastery/` (staging, dal repo sorgente) —
   **escludendo** `HANDOFF.md` stesso, che è un documento di passaggio e non serve
   nel repo finale (valuta tu: puoi anche tenerlo sotto `docs/` come memoria
   storica) — nella radice della working copy di `road-to-mastery`.
2. Verifica la struttura: alla radice devono comparire `.claude-plugin/`,
   `plugins/`, `tests/`, `docs/`, `README.md`, `.gitignore`.
3. **Esegui la suite di test** dalla radice: `python3 -m pytest -v` → atteso 17/17
   verdi.
4. **Valida il plugin**: `claude plugin validate .` (se la CLI è disponibile).
5. Committa e pusha sul branch di default del nuovo repo (vedi §4 sui vincoli git).

### ⚠ Fix obbligatorio prima di chiudere il trapianto: hook `enforce-main-push`
Nella sessione precedente l'hook di sviluppo `enforce-main-push` ha causato un
blocco perché era referenziato con **path relativo** e si rompeva quando la working
directory non era la radice del repo. Nel nuovo repo:
- se reintroduci hook di *manutenzione* (NON distribuiti col plugin — vedi
  design §4.2), referenzia gli script con path **assoluto** via
  `$CLAUDE_PROJECT_DIR` (per hook di progetto) o `$CLAUDE_PLUGIN_ROOT` (per hook
  di plugin), **mai** con path relativo;
- ricorda che `enforce-main-push` era un vincolo *specifico del vecchio progetto*
  (forzare push su `main`). Per `road-to-mastery` **non** imporre `main`: il design
  dice esplicitamente che `gitsync` pusha sul branch corrente. Reintroducilo solo
  se serve davvero come guardrail di sviluppo, e in forma generica.

---

## 4. Vincoli git per il nuovo repo

- Il vecchio progetto aveva la regola ferrea "push solo su main". **Quella regola
  NON si applica a `road-to-mastery`.** Qui segui il flusso branch standard:
  sviluppa su un branch di feature, apri PR solo se l'utente lo chiede esplicitamente.
- **Non creare PR senza che l'utente lo chieda.**
- Push: `git push -u origin <branch>`, con retry a backoff esponenziale (2s/4s/8s/16s)
  solo su errori di rete.
- Gli hook del *motore* (`checkpoint`, `chiusura`) usano `gitsync` che pusha sul
  branch corrente e **non** impone main: è corretto così, non cambiarlo.

---

## 5. SECONDO COMPITO: Piano 2 — migrazione delle skill

Dopo il trapianto, costruisci le skill del motore dentro
`plugins/road-to-mastery/skills/`, rese **generiche** e **materia-aware** (oggi, nel
vecchio repo, puntano a file di stato globali e sono cucite su Mariele).

**Nucleo v1 da migrare** (design §11):
`organizza`, `tutor`, `testa`, `interrogazione`, `simulazione`, `modalita`,
`programma`, `avanzamento`, `help`.

Requisiti trasversali per ogni skill (design §3, §6, §8, §9):
- leggono/scrivono **solo** dentro il contratto del file system (vedi sotto);
- ogni skill ha una `description` ricca nel frontmatter (alimenta
  l'autocompletamento dello slash);
- usano `tools/valida_contratto.py` come guardia di coerenza;
- ricerca web obbligatoria prima di generare contenuti didattici;
- italiano sempre; salvataggio silenzioso; nessuna domanda tecnica allo studente.

Skill chiave: **`/organizza`** fa il bootstrap completo della cartella-studente
(crea la struttura del contratto, genera `programma.md` + `programma-micro.md` con
ricerca web e **controllo di copertura**, compila `templates/CLAUDE.md.template`
con nome/esame/data).

Le altre skill del vecchio repo (`dossier`, `anteprima`, `traccia`, `inglese`,
`commissaria`, `integrazioni`, `statistiche`, `perfeziona`, `powerpoint`,
`progettazione`, `scaletta`, `nuova-lezione`, …) si migrano in fasi successive,
non in v1.

**Prima di scrivere il Piano 2 in dettaglio**, conviene leggere le skill esistenti
nel vecchio repo (`road_to_posto_comune`, cartelle `.claude/skills/` o
`.claude/commands/`) per capire cosa riusare. Servono entrambi i repo nello scope.

### Il contratto del file system (riassunto — dettaglio in `docs/design.md` §3)
```
<cartella-studente>/
├── CLAUDE.md                 ← generato da /organizza
├── materie/<slug>/
│   ├── materiali/            ← solo il syllabus ufficiale
│   ├── programma.md          ← struttura (no contenuti)
│   ├── programma-micro.md    ← micro-lezioni 5-10 min
│   ├── sessione_corrente.md  ← lezione aperta adesso (+ materia)
│   ├── domande.md            ← storico domande + esiti
│   └── sincronizzazione.md   ← mappa syllabus ↔ lezioni
└── stato/
    ├── progressi.md          ← registro globale + materia attiva
    └── preferenze.md         ← tono/metodo dello studente
```

---

## 6. Punti aperti da confermare con l'utente (design §13)

1. Slug definitivo del plugin e del repo (al momento entrambi `road-to-mastery`).
2. Se `sincronizzazione.md` resta per-materia (come ora) o diventa globale.
3. Formato del calendario ripassi (intervalli di spaced retrieval) in `progressi.md`.

---

## 7. Tono e modo di lavorare con l'utente

- Risposte in italiano, calde e concrete, senza gergo tecnico.
- L'utente delega volentieri le parti tecniche: proponi, poi agisci.
- Quando una decisione è davvero sua (es. i punti aperti §6), chiedi con opzioni
  chiare; altrimenti procedi con default sensati e spiega cosa hai fatto.
