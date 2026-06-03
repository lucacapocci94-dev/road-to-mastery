# Design: Road to Mastery — Motore-tutor distribuibile come plugin Claude Code

**Data:** 2026-06-03
**Branch di sviluppo:** `claude/create-another-repo-o2hVB`
**Origine:** generalizzazione di "Road to Posto Comune" (tutor monouso per Mariele Ricci)
   in un motore riutilizzabile per qualsiasi studente e qualsiasi esame.

---

## 0. In una frase

Un **plugin Claude Code pubblico** che trasforma qualsiasi cartella in un tutor
personale per qualsiasi esame. Il plugin non contiene contenuti didattici:
contiene un **motore** (skill + hook) e un **contratto sul file system**. I
contenuti vengono generati al momento, con ricerca web, e salvati in file che
si auto-sostengono nel tempo.

Distinzione che regge tutto il design:

- **Hook** = garanzia *deterministica* di persistenza e caricamento dello stato.
  Partono da soli, sempre, anche quando il modello "si distrae". Servono a non
  perdere pezzi nel tempo.
- **Skill** = *qualità del processo* (come si costruisce una lezione, come si
  scorpora un programma, come si interroga). La bontà della spiegazione non è un
  hook: è il processo dentro la skill.

Non confondere le due cose: un hook non rende una lezione "bella", la rende
*salvata*.

---

## 1. Obiettivo

Partendo dallo scaffold monouso attuale (cucito su una sola candidata, un solo
concorso, file di stato globali), produrre un artefatto distribuibile che:

1. si installa con un comando (`/plugin install`) e si aggiorna con `/plugin update`;
2. funziona per **più materie** nella stessa cartella senza fare casino;
3. non perde mai i progressi, **a prescindere da git**;
4. genera lezioni complete e dense (niente buchi su ciò che l'esame può chiedere);
5. è auto-esplicativo (un `/help` che non lascia nulla al caso + autocompletamento
   dello slash).

---

## 2. Distribuzione

- Repo pubblico = **marketplace di plugin**.
- Lo studente:
  1. `/plugin marketplace add <repo>`
  2. `/plugin install road-to-mastery`
  3. aggiornamenti con `/plugin update`.
- Il plugin è l'**unica fonte di verità** del motore. Niente copia-incolla di
  file `.claude/` tra cartelle.
- Gli **hook di manutenzione** (vedi §4) restano nel repo del plugin e **non**
  vengono distribuiti: servono solo a chi sviluppa il plugin.

---

## 3. Il contratto del file system

Ogni skill legge e scrive **solo** dentro questo schema. Nessuna skill inventa
percorsi propri.

```
<cartella-studente>/
├── CLAUDE.md                 ← GENERATO da /organizza: regole-tutor + profilo studente
├── materie/
│   └── <slug-materia>/
│       ├── materiali/        ← solo il SYLLABUS ufficiale (leggero, autorevole)
│       ├── programma.md      ← STRUTTURA: moduli, lezioni, priorità ⭐ (no contenuti)
│       ├── programma-micro.md← stessa struttura, scorporata in micro-lezioni 5-10 min
│       ├── sessione_corrente.md ← lezione aperta ADESSO (+ a quale materia appartiene)
│       ├── domande.md        ← storico domande + esiti (alimenta la verifica differita)
│       └── sincronizzazione.md ← mappa syllabus ↔ lezioni (controllo di copertura)
└── stato/
    ├── progressi.md          ← REGISTRO GLOBALE: tutte le materie, materia attiva,
    │                            %, punti deboli, calendario ripassi
    └── preferenze.md         ← tono/metodo dello studente
```

Principi:

- **Materia = namespace.** Tutto ciò che è di una materia vive sotto
  `materie/<slug>/`. Nessun file di lezione è condiviso tra materie → zero
  contaminazione.
- **`stato/` è globale**: l'unico posto dove si sa qual è la materia attiva e
  qual è lo stato complessivo.
- **I contenuti non sono nei file.** `programma.md` è solo struttura. La
  spiegazione di una micro-lezione si costruisce a runtime con ricerca web. Così
  niente materiale stantio e contesto leggero.

---

## 4. Hook — lista precisa e concisa

### 4.1 Hook del MOTORE (nel plugin, valgono per ogni studente)

| Nome | Evento | Cosa fa | Garanzia |
|---|---|---|---|
| `carica-e-riconcilia` | **SessionStart** (`startup`, `resume`, `clear`, **`compact`**) | inietta nel contesto: materia attiva, %, punti deboli, ripassi dovuti oggi. Se trova una `sessione_corrente.md` non consolidata (sessione morta male) → segnala di riversarla in `progressi.md` *prima* di ogni altra cosa. | mai partire alla cieca; mai perdere una sessione interrotta; **dopo una compattazione re-inietta lo stato**; la verifica differita parte sempre. |
| `checkpoint` | **Stop** | persiste su disco ciò che è cambiato e fa push se git è disponibile. | checkpoint frequentissimo (ad ogni turno), gratis. |
| `chiusura` | **SessionEnd** | consolidamento finale + push di sicurezza. | backstop su uscita pulita. |

> **Perché NON c'è un hook PreCompact** (decisione di design verificata sulla
> documentazione, 2026-06-03): un hook PreCompact è uno script di shell che **non
> vede** ciò che il modello ha in contesto e non ha ancora scritto su file, e il
> cui **stdout non torna al modello**. Quindi non può "flushare la memoria" come
> avevamo ipotizzato: prometterebbe una cosa che non può mantenere. Il vero
> meccanismo anti-compattazione è che **SessionStart riparte con `source: "compact"`
> ed è l'unico hook il cui stdout viene iniettato nel contesto**: `carica-e-riconcilia`
> ripopola la testa del modello dai file dopo ogni compressione. Combinato con il
> salvataggio incrementale della skill (file sempre aggiornati su disco), la
> perdita è coperta senza PreCompact.

Note di robustezza:

- Hook dichiarati nel `plugin.json` del plugin; gli script si referenziano con
  `${CLAUDE_PLUGIN_ROOT}/...` (il plugin viene copiato in una cache, i path
  relativi non reggono). Stato persistente del plugin in `${CLAUDE_PLUGIN_DATA}`.
- Tutti gli hook git-dipendenti seguono il pattern **"git-se-disponibile"**: se
  non c'è un repo git (caso studente normale in locale), saltano in modo pulito i
  comandi git ed escono 0. La **scrittura locale dei file resta la verità
  primaria**; git è solo copia di sicurezza/sincronizzazione tra dispositivi.
- Nessun hook deve mai bloccare il flusso: exit 0 sempre, fallimenti loggati.
  Lo stdout iniettato come contesto vale **solo per SessionStart**; Stop e
  SessionEnd fanno solo side-effect su file/git.
- Volutamente **non** mettiamo un hook su ogni prompt né su ogni Write:
  appesantirebbero senza aggiungere garanzie reali.

### 4.2 Hook di MANUTENZIONE (solo nel repo del plugin, NON distribuiti)

| Nome | Evento | Scopo |
|---|---|---|
| `install-superpowers` | SessionStart | scarica le skill di superpowers in ambiente web di sviluppo |
| `enforce-main-push` | PreToolUse(Bash) | guardrail sul branch durante lo sviluppo del plugin |

---

## 5. Strategia di salvataggio — reti anti-perdita

La domanda "quando salvare?" non ha *un* momento: ha più reti sovrapposte,
ognuna con un compito netto. Indipendenti da git.

| Momento | Chi | Cosa salva | Perché serve |
|---|---|---|---|
| **Durante la lezione** | la skill (`/tutor`), in continuo | aggiorna `sessione_corrente.md` ad ogni blocco | sopravvive a un crash a metà lezione; tiene i file sempre allineati per la compattazione |
| **Lezione finita** | la skill | aggiorna `progressi.md` + `domande.md` + calendario ripassi | il "coperto/non coperto" diventa ufficiale |
| **Stop** (fine di ogni risposta) | hook `checkpoint` | persiste + push se git | checkpoint ad altissima frequenza |
| **SessionStart** (avvio/ripresa/clear/**compact**) | hook `carica-e-riconcilia` | recupera sessioni orfane non consolidate e **re-inietta lo stato dopo la compattazione** | rete di recupero + ripristino contesto |

Questa è la formalizzazione deterministica della "Regola 6 — salva all'ingresso"
del CLAUDE.md attuale: smette di essere una cosa che il modello deve *ricordarsi*
e diventa un hook.

---

## 6. Modello di lezione: interattiva + verifica differita

Scelta pedagogica approvata: **insegnamento interattivo** durante la sessione,
**verifica differita** (spaced retrieval) all'inizio della sessione successiva.

Flusso `/tutor` (processo della skill, non hook):

1. **Aggancio** — una domanda per attivare ciò che già si sa.
2. **Ricerca web** sulla micro-lezione corrente (contenuto fresco, mai a memoria).
3. **Spiegazione a blocchi** + ancora mnemonica.
4. **Auto-verifica di copertura** contro il punto di syllabus mappato in
   `sincronizzazione.md` (la micro-lezione copre davvero quel punto?).
5. **Domande di applicazione** (caso nuovo), non di ripetizione.
6. **Teach-back** finale: lo studente ri-spiega con parole sue.
7. **Scrittura stato** (vedi §5).

La verifica *vera* è differita: all'avvio della sessione dopo, l'hook
`carica-e-riconcilia` segnala le lezioni mature per il ripasso e la skill di
interrogazione le ripropone. L'esito aggiorna `domande.md` e i punti deboli in
`progressi.md`.

---

## 7. Densità del programma: niente buchi

Requisito esplicito: le micro-lezioni vanno bene (studio "ritagliato" nei
momenti liberi), ma lo scorporo deve essere **denso ed esaustivo**, altrimenti si
rischia di non coprire qualcosa che l'esame può chiedere. Questo è lavoro di
skill + verifica, non di hook.

- **`/organizza`** scorpora il syllabus con ricerca web e poi esegue un
  **controllo di copertura**: ogni punto del syllabus deve mappare su ≥1
  micro-lezione, registrato in `sincronizzazione.md`. Se un punto resta scoperto,
  lo segnala.
- **`/tutor`** fa la verifica di copertura per la singola micro-lezione (§6.4).
- **`/avanzamento`** espone l'invariante di copertura: es. *"3 punti del syllabus
  non ancora coperti da nessuna micro-lezione"*. Niente sparisce in silenzio.

Onestà di design: nessun hook può garantire che una spiegazione sia *bella*. La
completezza la garantiscono la densità a monte (`/organizza`) + i controlli di
copertura (`/tutor`, `/avanzamento`).

---

## 8. Multi-materia senza casini

Tre regole rigide:

1. **Tutto sotto `materie/<slug>/`** — nessun file di lezione condiviso. Zero
   contaminazione tra materie.
2. **Un puntatore "materia attiva"** in `progressi.md`. Ogni comando risolve la
   materia in quest'ordine: argomento esplicito (`/tutor matematica`) → materia
   attiva → la chiedo. **Mai indovinare.**
3. **`sessione_corrente.md` registra a quale materia appartiene** → la
   riconciliazione al SessionStart sa *dove* consolidare. Cambiare materia
   applica il salva-all'ingresso (§5) prima dello switch.

`/avanzamento` mostra il progresso per-materia, così nessuna materia resta
indietro in silenzio.

---

## 9. Help e autocompletamento

- In un plugin, **ogni skill è già un comando `/` che appare nel menu di
  autocompletamento** con la sua `description` di frontmatter. Requisito: ogni
  skill ha una `description` chiara e ricca → l'autocompletamento dello slash è
  automatico e completo.
- **`/help`** è un indice esaustivo: ogni comando con cosa fa, quando usarlo, un
  esempio; più la mappa del file system e il modello di lezione. Non lascia nulla
  al caso.

---

## 10. Bootstrap della cartella studente: `/organizza`

`/organizza` non genera solo il programma: **allestisce la cartella** dello
studente perché si auto-sostenga.

1. Intervista breve (non tecnica): nome, esame, data esame, materiali/syllabus.
2. Crea la struttura del §3.
3. Genera `programma.md` + `programma-micro.md` con ricerca web e controllo di
   copertura (§7).
4. **Genera un `CLAUDE.md`** nella cartella: regole-tutor generiche (italiano,
   ricerca web obbligatoria, salvataggio silenzioso, niente domande tecniche,
   ecc.) + il profilo dello studente (nome, esame, data).

Effetto: da lì in poi, ogni volta che lo studente apre Claude in quella cartella,
l'ambiente *è già* un tutor configurato per lui. Il plugin porta il motore;
`/organizza` posa le fondamenta. File system auto-sostenibile.

---

## 11. Skill v1 (nucleo) da migrare al contratto

Tutte le skill esistenti vanno rese **materia-aware** e agganciate al contratto
del §3 (oggi puntano in parte ai vecchi file globali). Nucleo v1:

`organizza`, `tutor`, `testa`, `interrogazione`, `simulazione`, `modalita`,
`programma`, `avanzamento`, `help`.

Le altre skill già presenti nel repo (`dossier`, `anteprima`, `traccia`,
`inglese`, `commissaria`, `integrazioni`, `statistiche`, `perfeziona`,
`powerpoint`, `progettazione`, `scaletta`, `nuova-lezione`, …) vengono
inventariate e migrate in fasi successive: v1 stabilizza il motore e il nucleo,
non tutto in una volta.

---

## 12. Cosa NON è in scope per la v1

- Generazione PDF e slide (resta, ma non è core del motore).
- Migrazione automatica dei contenuti di Mariele al nuovo layout multi-materia
  (lo facciamo come passo dedicato, con verifica).
- Pubblicazione effettiva del marketplace (prima il motore regge, poi si pubblica).

---

## 13. Punti aperti da confermare in fase di piano

1. Nome esatto dello slug del plugin e del repo marketplace.
2. Se `sincronizzazione.md` sta per-materia (come qui) o resta globale.
3. Formato esatto del calendario ripassi (intervalli di spaced retrieval) in
   `progressi.md`.
