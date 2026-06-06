---
name: organizza
description: Bootstrap completo della cartella-studente per qualsiasi esame. Intervista breve (nome, esame, data, syllabus, livello-obiettivo), crea la struttura del contratto del file system, genera in fretta la base di programma.md e programma-micro.md con ricerca web e controllo di copertura, compila il CLAUDE.md del tutor e infine ti fa scegliere se approfondire subito tutto con la squadra di specialisti o strada facendo. Usala alla prima configurazione o per aggiungere una nuova materia.
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
5. **Quanto a fondo vuole arrivare** (il "livello-obiettivo"), spiegato a parole
   semplici — non come numeri:
   - **base** — l'essenziale per orientarsi;
   - **approfondito** — casi, eccezioni, dettagli che spesso chiedono;
   - **padronanza** — collegamenti e visione d'insieme, "padrone della materia".
   È solo l'obiettivo a cui puntare: la base la costruiamo comunque subito, e si
   approfondisce dopo (Passo 8). Se non sa rispondere, default **approfondito**.

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

## Passo 4 — Genera la base del programma (veloce) con controllo di copertura

Qui costruisci sempre la **base rapida** (lo scheletro), così lo studente ha
qualcosa di usabile in pochi minuti. L'approfondimento pesante **non** si fa qui:
è il Passo 8 a deciderlo. Niente squadra di specialisti in questo passo.

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
percentuali a 0, sezione "Punti deboli" vuota, **Modalità attiva: micro**, il
**Livello-obiettivo** scelto al Passo 1 (base / approfondito / padronanza), e un
**Calendario ripassi** (ripasso dilazionato a 1, 3, 7, 16, 35 giorni dopo la
prima padronanza di ogni lezione).

---

## Passo 7 — Verifica

- Esegui il validatore del contratto come guardia di coerenza:
  `python3 ${CLAUDE_PLUGIN_ROOT}/tools/valida_contratto.py .`
- Mostra un riepilogo breve: materia creata, numero di moduli/micro-lezioni,
  eventuali punti del syllabus che richiedono attenzione.

---

## Passo 8 — La scelta sulla profondità (sempre, e la decide lo studente)

La base è pronta. Se il **Livello-obiettivo** è più alto di "base", **proponi
sempre la scelta** e **non decidere tu**: presenta le due strade in modo neutro,
con i loro fatti, senza spingere verso una delle due. (Se il livello scelto è
"base", non c'è nulla da approfondire: salta questo passo.)

Di' qualcosa come:
> "La base è pronta, puoi già studiare. Visto che punti a **[livello-obiettivo]**,
> come preferisci arrivarci?
> - **Strada facendo:** parti subito e approfondiamo dove serve, man mano, con
>   `/infittisci` o `/raddrizza` sul momento. Inizi adesso, niente attese.
> - **Subito, tutto:** mando ora la squadra di specialisti a portare l'intero
>   programma a quel livello. Più completo da subito, ma **richiede parecchi
>   minuti** ed è interrompibile (riprende da dove si ferma)."

Aspetta la sua risposta — entrambe sono scelte legittime:
- **strada facendo** → chiudi qui;
- **subito, tutto** → avvia il motore di `/infittisci` sull'intero programma al
  livello-obiettivo (con foglio di lavoro, ondate di 3, ripartenza), poi `/carico`.

📍 Adesso puoi:
- iniziare a studiare con `/tutor`
- vedere il programma con `/programma`
- approfondire quando vuoi con `/infittisci`
- vedere il carico giornaliero con `/carico`
