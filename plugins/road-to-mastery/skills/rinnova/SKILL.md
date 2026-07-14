---
name: rinnova
description: Aggiorna un programma già esistente quando la materia stessa è cambiata (una tecnologia si è evoluta, il syllabus ufficiale è stato rivisto, un concetto o un uso è cambiato). Parte da linee guida, documenti, link o testo che gli passi tu — oppure cerca sul web cosa è cambiato — ri-scansiona il programma e propone un piano di modifica: aggiunge moduli o lezioni, modifica ciò che è cambiato di concetto, rimuove ciò che è obsoleto (solo dopo tua conferma), preservando i progressi già fatti. Poi riallinea copertura, carico e diario. Diverso da /infittisci, che approfondisce senza mai cambiare i concetti né togliere.
---

# /rinnova — Aggiornare il programma quando la materia cambia

`/organizza` crea il programma. `/infittisci` lo rende più denso **senza mai
cambiare i concetti né togliere niente**. `/rinnova` copre il caso diverso: **la
materia stessa è cambiata** — una tecnologia si è evoluta, il syllabus ufficiale
è stato rivisto, un concetto o un uso non è più quello di prima. Quindi qui si può
**aggiungere, modificare e rimuovere**, riallineando il programma alla nuova realtà
senza perdere i progressi già fatti.

Vincoli fermi (come `/infittisci`): **stessa durata** delle micro-lezioni (5-10 min)
e **stessa data d'esame**, salvo che tu non me ne dia una nuova. Cambia il *contenuto*
del programma, non il patto di studio.

## Risoluzione della materia
Argomento esplicito → materia attiva in `stato/progressi.md` → altrimenti chiedi.
Tutti i percorsi sono `materie/<materia>/...`.

## Ambito
- `/rinnova` → tutta la materia attiva.
- `/rinnova 3` → solo il modulo 3 · `/rinnova 3.2` → solo la sezione 3.2.

## Fase 0 — Salva all'ingresso
Se `materie/<materia>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo prima di procedere.

## Fase 1 — Raccogli il "delta" (cosa è cambiato)
Il delta può arrivare da due strade, spesso da entrambe:

1. **Fonti che mi dai tu** — linee guida, un documento, un link, del testo
   incollato, un nuovo syllabus/bando ufficiale, delle note di rilascio. Se me le
   hai passate nel messaggio o indicate come file, **quelle sono la verità
   primaria**: leggile per prime. Se un nuovo syllabus ufficiale è tra queste,
   salvalo in `materie/<materia>/materiali/` sostituendo il vecchio (è il
   riferimento leggero e autorevole del contratto).
2. **Ricerca web mirata** — cerca cosa è cambiato dall'ultima volta, su fonti
   aggiornate e autorevoli:
   ```
   WebSearch: "[materia] novità cambiamenti [anno] cosa è cambiato"
   WebSearch: "[esame] [materia] syllabus aggiornato [anno] differenze"
   ```
   **Nessun tetto al numero di ricerche.** Se una singola ricerca non torna,
   cambia domanda e prosegui.

Se non ti ho fornito fonti **e** la ricerca web non evidenzia cambiamenti reali,
non inventare un aggiornamento: passa in **modalità solo-verifica** (Fase 2, poi
chiudi al piano senza applicare nulla).

## Fase 2 — Ri-scansiona e costruisci il piano di modifica
Leggi lo stato attuale nell'ambito: `programma-micro.md`, `programma.md`,
`sincronizzazione.md`, il syllabus in `materiali/`, e i codici lezione in
`stato/progressi.md`. Confrontalo con il delta della Fase 1 e con la coerenza
interna, e produci un **piano** che classifica ogni voce:

- **➕ AGGIUNGI** — un nuovo modulo, o nuove lezioni dentro un modulo esistente,
  per argomenti comparsi ora. Partono `○ da fare`.
- **✏️ MODIFICA** — una lezione che esiste ma il cui **concetto o uso è cambiato**:
  va riscritta. Se lo studente l'aveva già `✓ completata`, va segnata **`↻ da
  rivedere`** (il contenuto non è più quello su cui si era preparato).
- **🗑️ RIMUOVI** — una lezione o un modulo diventati **obsoleti** (non più nel
  programma, concetto superato). *Non tolgo mai niente in questa fase.*
- **✓ RESTA** — invariato: progressi e codice preservati.

Includi nel piano anche le **difformità interne** che emergono dalla scansione,
indipendentemente dal delta:
- punti del syllabus non coperti da nessuna micro-lezione (buchi di copertura);
- lezioni orfane (non mappate ad alcun punto del syllabus);
- codici lezione citati in `stato/progressi.md` che non esistono più nel programma.

## Fase 3 — Mostra il piano e chiedi conferma (cancello di sicurezza)
Presenta il piano in modo compatto e leggibile:
```
🔄 Piano di rinnovo — [materia] — ambito [tutto | modulo N]

Origine del cambiamento: [fonti che mi hai dato / ricerca web / entrambe]

➕ Aggiungo:   [elenco moduli/lezioni nuovi]
✏️ Modifico:  [elenco] (di cui [n] già completate → diventeranno "da rivedere")
🗑️ Rimuovo:   [elenco]   ⚠️ richiede la tua conferma
✓ Restano:    [n] lezioni invariate

Difformità trovate: [buchi di copertura / lezioni orfane / codici fantasma]
```
**Le rimozioni non partono senza il tuo "sì" esplicito.** Aggiunte e modifiche di
concetto puoi confermarle in blocco. Se non ci sono rimozioni, chiedi comunque un
via libera prima di riscrivere il programma. In modalità solo-verifica ti fermi
qui: mostri le difformità e non applichi nulla.

## Fase 4 — Applica (preservando i progressi)
Dopo conferma:

1. **Squadra per le aggiunte ampie.** Se le aggiunte/riscritture coprono più
   sezioni, riusa il motore di `/infittisci`: uno specialista per sezione, ricerca
   web solo sulla sua parte, scrive man mano sul foglio `materie/<materia>/_lavori/<sezione>.md`
   (con `Stato: in corso | completato`), a **ondate di massimo 3**. Così il lavoro
   è **ripartibile**: se ti interrompi, ridando `/rinnova` riprende solo ciò che
   manca. Per una singola lezione modificata, fallo direttamente senza squadra.
2. **Fondi** le nuove lezioni e le riscritture in `programma-micro.md` (e riflettile
   in `programma.md`), **rinumerando in modo coerente**.
3. **Mappatura vecchio→nuovo codice.** Le lezioni che restano non perdono mai il
   loro stato: `✓ completata` / `⚠ punto debole` si conservano; aggiorna i codici
   in `stato/progressi.md` di conseguenza. Le lezioni **modificate** già completate
   diventano `↻ da rivedere`; le nuove `○ da fare`.
4. **Rimozioni (solo le confermate).** Togli le lezioni/moduli obsoleti dal
   programma e ripulisci i loro codici in `stato/progressi.md`. **Registra sempre
   nel diario cosa è stato rimosso e perché** (tracciabilità: niente sparisce in
   silenzio).
5. **Syllabus.** Se hai sostituito il syllabus in `materiali/`, assicurati che il
   programma rispecchi la nuova versione.

## Fase 5 — Riallinea copertura e coerenza
1. **Aggiorna `sincronizzazione.md`**: ogni punto del (nuovo) syllabus mappa su ≥1
   micro-lezione; segnala eventuali buchi residui.
2. Esegui `python3 ${CLAUDE_PLUGIN_ROOT}/tools/valida_contratto.py .` come guardia
   di coerenza; se segnala qualcosa, sistemalo.
3. A fusione riuscita, i fogli in `_lavori/` possono essere svuotati.

## Fase 6 — Riprezza in tempo (sempre)
Il programma è cambiato di dimensione: esegui subito **`/carico`** per la materia,
così mostri il nuovo carico giornaliero e il semaforo rispetto alla data.

## Fase 7 — Tappa nel diario e riepilogo
Aggiungi una riga a `stato/diario.md`
(`- [oggi] · [materia] · programma rinnovato: +X nuove, ✏️Y, 🗑️Z`) e mostra:
```
✅ Programma rinnovato — [materia] — ambito [tutto | modulo N]

Aggiunte: +X micro-lezioni     Modificate: Y (di cui Z ora "da rivedere")
Rimosse: W (registrate nel diario)     Copertura: [tutto coperto / N punti scoperti]
Micro-lezioni: prima A → ora B
```

📍 Adesso puoi:
- vedere il nuovo carico con `/carico`
- ripassare ciò che è cambiato con `/tutor` (parte dalle lezioni "da rivedere")
- vedere il programma aggiornato con `/programma`
- se interrotto, **ridai `/rinnova`**: riprende solo le sezioni mancanti
