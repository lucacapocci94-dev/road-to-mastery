---
name: infittisci
description: Approfondisce ("infittisce") il programma di una materia su più livelli di profondità, senza allungare la durata delle micro-lezioni né spostare la data d'esame. Lavora a squadra — lancia un sub-agente per ogni sezione, che cerca sul web SOLO la sua parte, la espande in micro-lezioni dense e supera un controllo anti-banalità, poi fonde tutti i blocchi in un programma unico e ricalcola la copertura del syllabus e il carico di studio.
---

# /infittisci — Approfonditore del programma a squadra

`/organizza` costruisce lo scheletro di base. `/infittisci` lo rende **denso ed
esaustivo** su più livelli, facendo lavorare un sub-agente specializzato per ogni
sezione. Vincoli fermi: **stessa durata** delle micro-lezioni (5-10 min) e
**stessa data d'esame** — l'unica cosa che cresce è la profondità (e quindi il
carico giornaliero, che misuriamo con `/carico`).

## Risoluzione della materia
Argomento esplicito → materia attiva in `stato/progressi.md` → altrimenti chiedi.
Tutti i percorsi sono `materie/<materia>/...`.

## Fase 0 — Salva all'ingresso
Se `materie/<materia>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Fase 1 — Ambito e livello
Interpreta il comando:
- `/infittisci` → tutto il programma
- `/infittisci 3` → solo il modulo 3
- `/infittisci 3.2` → solo la sezione 3.2
- **Livello di profondità** (esplicito o a parole, es. "più esteso", "di più"):
  - **Livello 1 — base**: definizione, esempio, cosa è.
  - **Livello 2 — approfondimento**: casi particolari, eccezioni, normativa di
    dettaglio, esempi multipli.
  - **Livello 3 — padronanza**: collegamenti interdisciplinari, applicazioni,
    insidie d'esame — lo studente "vede il mondo e collega ogni pezzo".

Leggi `materie/<materia>/programma-micro.md`, `sincronizzazione.md` e il syllabus
in `materie/<materia>/materiali/` per sapere com'è fatto il programma attuale.

## Fase 2 — Lavoro a squadra (un sub-agente per sezione)
Per **ogni sezione nell'ambito**, lancia un sub-agente dedicato (strumento Agent /
Task), così ognuno lavora a **contesto pulito** e non si diluisce con gli altri.
Istruzioni per ogni "specialista di sezione":

1. **Ricerca web obbligatoria, solo sulla sua sezione**, su fonti aggiornate e
   autorevoli (normative con anno, programmi ufficiali, domande tipiche d'esame).
2. **Espandi** la sezione in micro-lezioni da 5-10 min al livello richiesto,
   coprendo **tutti** i sotto-aspetti (niente buchi).
3. **Controllo anti-banalità**: verifica che la sezione, a quel livello, regga il
   livello reale dell'esame; se è troppo leggera, aggiungi ciò che manca.
4. **Restituisci solo il blocco** della sezione: codici lezione, titoli, ancora
   mnemonica e mappatura ai punti di syllabus. **Non** il contenuto disteso delle
   lezioni (quello si genera a runtime con `/tutor`).

## Fase 3 — Fusione (coordinatore)
1. **Fondi** i blocchi restituiti dentro `programma-micro.md`, rinumerando in modo
   coerente.
2. **Preserva i progressi**: le lezioni già `✓ completata` / `⚠ punto debole`
   devono restare tali. Tieni una mappatura vecchio→nuovo codice e aggiorna
   `stato/progressi.md` di conseguenza. Non azzerare mai ciò che è già fatto.
3. **Aggiorna `sincronizzazione.md`** (libro mastro della copertura): ogni punto
   di syllabus deve mappare su ≥1 micro-lezione. Segnala buchi residui.
4. Esegui il validatore: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/valida_contratto.py .`

## Fase 4 — Prezzo in tempo (sempre)
Esegui subito `/carico` per la materia: l'infittimento ha aumentato le lezioni,
quindi mostra il nuovo carico giornaliero e il semaforo di fattibilità rispetto
alla data. Così lo studente vede subito quanto costa, in tempo, l'approfondimento.

## Fase 5 — Riepilogo
```
🧱 Programma infittito — [materia] — Livello [N]

Sezioni approfondite: [elenco]
Micro-lezioni: prima X → ora Y (+Z)
Copertura syllabus: [tutto coperto / N punti ancora scoperti]
Anti-banalità: [ok / rinforzata su: ...]
```

📍 Adesso puoi:
- vedere il nuovo carico con `/carico`
- iniziare ad approfondire con `/tutor`
- alleggerire tornando indietro (chiedimi di ridurre il livello di una sezione)
