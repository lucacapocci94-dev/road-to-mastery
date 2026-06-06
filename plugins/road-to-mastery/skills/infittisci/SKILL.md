---
name: infittisci
description: Approfondisce ("infittisce") il programma di una materia su più livelli di profondità, senza allungare la durata delle micro-lezioni né spostare la data d'esame. Lavora a squadra — uno specialista per sezione cerca sul web SOLO la sua parte e la espande finché regge l'esame, scrivendo su un foglio di lavoro così il processo è ripartibile; poi fonde tutti i blocchi in un programma unico e ricalcola la copertura del syllabus e il carico di studio.
---

# /infittisci — Approfonditore del programma a squadra

`/organizza` costruisce lo scheletro di base. `/infittisci` lo rende **denso ed
esaustivo** su più livelli, facendo lavorare uno specialista per ogni sezione.
Vincoli fermi: **stessa durata** delle micro-lezioni (5-10 min) e **stessa data
d'esame** — cresce solo la profondità (e quindi il carico, che misura `/carico`).

## Risoluzione della materia
Argomento esplicito → materia attiva in `stato/progressi.md` → altrimenti chiedi.
Tutti i percorsi sono `materie/<materia>/...`.

## Fase 0 — Salva all'ingresso
Se `materie/<materia>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Fase 1 — Ambito e livello
- `/infittisci 3` → modulo 3 · `/infittisci 3.2` → sezione 3.2
- `/infittisci` senza ambito → **chiedi se vuole una sezione/un modulo o tutto il
  programma**, e avvisa che "tutto" è un lavoro lungo (default prudente: non
  partire sull'intero programma senza conferma).
- **Livello**: 1 base · 2 approfondimento · 3 padronanza (collegamenti, insidie
  d'esame — "vedi il mondo e colleghi ogni pezzo").

Leggi `programma-micro.md`, `sincronizzazione.md` e il syllabus in `materiali/`
per sapere com'è fatto il programma attuale e quali sezioni rientrano nell'ambito.

## Fase 2 — La squadra (con foglio di lavoro e ripartenza)

### Il foglio di lavoro (perché il processo sia ripartibile)
Ogni sezione ha un suo file in `materie/<materia>/_lavori/<sezione>.md`. È la
**lavagna condivisa**: ciò che è scritto lì sopravvive a un'interruzione, ciò che
resta solo nella testa di uno specialista no. In testa al file, un campo
**Stato: in corso | completato**.

### Ripartenza intelligente (prima di lanciare chiunque)
Per ogni sezione nell'ambito, guarda il suo foglio di lavoro:
- **Stato completato** → salta, è già fatta.
- **assente o "in corso"** → va (ri)lavorata.
Così, se una sessione precedente è stata interrotta, si rifà **solo ciò che
manca**, mai tutto da capo.

### Lavoro a ondate
Lancia gli specialisti **a gruppi di massimo 3 per volta** (sub-agenti, strumento
Agent/Task), così la macchina non si ingolfa. Quando un gruppo finisce, parte il
successivo, fino a esaurire le sezioni da lavorare. Riferisci l'avanzamento
("sezione 3 fatta · 4 in corso").

### Istruzioni per ogni specialista di sezione
1. **Ricerca web mirata, solo sulla tua sezione**, su fonti aggiornate e
   autorevoli. **Nessun tetto al numero di ricerche**: cerca quanto serve per
   coprire bene tutto l'importante.
2. **Espandi** la sezione in micro-lezioni da 5-10 min al livello richiesto,
   coprendo **tutti** i sotto-aspetti.
3. **Traguardo (quando hai finito)**: quando la sezione è **completa e profonda al
   livello scelto e regge l'esame vero** (controllo **anti-banalità**) — *non*
   "una lezione e via". Il "almeno una micro-lezione per punto del syllabus" è solo
   la **rete di sicurezza** minima, mai il punto d'arrivo.
4. **Scrivi man mano** sul tuo foglio `_lavori/<sezione>.md` (codici lezione,
   titoli, ancora mnemonica, mappatura ai punti di syllabus). Quando hai davvero
   finito, metti **Stato: completato**.
5. **Salta-l'intoppo**: se una singola ricerca web non torna o si pianta, cambia
   domanda e prosegui — non restare appeso a quella.

> **Tempo = sveglia, non ghigliottina.** Un budget di tempo serve solo ad accorgersi
> se uno specialista **non fa più progressi** (foglio fermo): in quel caso lo si
> rilancia su quella sezione. Chi sta ancora producendo non va mai interrotto.

## Fase 3 — Fusione (coordinatore)
Quando tutte le sezioni dell'ambito sono **Stato: completato**:
1. **Fondi** i blocchi dai fogli `_lavori/` dentro `programma-micro.md`,
   rinumerando in modo coerente.
2. **Preserva i progressi**: le lezioni già `✓ completata` / `⚠ punto debole`
   restano tali (tieni una mappatura vecchio→nuovo codice e aggiorna
   `stato/progressi.md`). Non azzerare mai ciò che è già fatto.
3. **Aggiorna `sincronizzazione.md`** (copertura): ogni punto di syllabus mappa su
   ≥1 micro-lezione; segnala eventuali buchi residui.
4. Esegui `python3 ${CLAUDE_PLUGIN_ROOT}/tools/valida_contratto.py .`.
5. A fusione riuscita, i fogli in `_lavori/` possono essere svuotati (servono solo
   come rete per la ripartenza).

## Fase 4 — Prezzo in tempo (sempre)
Esegui subito `/carico` per la materia: l'infittimento ha aumentato le lezioni,
quindi mostra il nuovo carico giornaliero e il semaforo rispetto alla data.

## Fase 5 — Riepilogo
```
🧱 Programma infittito — [materia] — Livello [N]

Sezioni approfondite: [elenco]   (ripartenza: [n] già fatte e saltate)
Micro-lezioni: prima X → ora Y (+Z)
Copertura syllabus: [tutto coperto / N punti ancora scoperti]
Anti-banalità: [ok / rinforzata su: ...]
```

📍 Adesso puoi:
- vedere il nuovo carico con `/carico`
- iniziare ad approfondire con `/tutor`
- se interrotto, **ridai `/infittisci`**: riprende solo le sezioni mancanti
