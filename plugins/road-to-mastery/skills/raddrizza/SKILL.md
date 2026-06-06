---
name: raddrizza
description: Corregge il tiro a lezione iniziata, quando il tutor è andato troppo rapido o troppo in superficie su un concetto. Riprende il punto esatto dove sei (dalla sessione corrente), lo rispiega più disteso con ricerca web e nuovi esempi e, se la lacuna è strutturale, approfondisce quella sezione del programma (motore di /infittisci) così non resta superficiale anche in futuro.
---

# /raddrizza — Correggere il tiro a lezione iniziata

È il gemello **reattivo** di `/infittisci`. Quando durante una lezione senti che
è andato **troppo veloce** o **troppo leggero** su qualcosa, chiami `/raddrizza`
(o dici "più esteso", "vai più piano", "questo non l'ho capito") e si interviene
**sul punto esatto dove sei adesso**.

## Risoluzione della materia
Materia attiva da `stato/progressi.md`. Percorsi `materie/<materia>/...`.

## Fase 1 — Capisci dove sei
Leggi `materie/<materia>/sessione_corrente.md`: campo **Lezione** e **Punto
raggiunto**. È quello il concetto da raddrizzare. Se l'utente indica un punto
diverso a parole, usa quello.

## Fase 2 — Raddrizzamento immediato (sempre)
1. **Ricerca web obbligatoria** sul concetto specifico, con taglio più di
   dettaglio (esempi, casi, eccezioni, come lo chiede l'esame).
2. **Rispiega più disteso**: ritmo più lento, dal concreto alla teoria, 2-3
   esempi nuovi, un'ancora mnemonica diversa da quella già usata.
3. Verifica la comprensione con una domanda di applicazione su un caso nuovo.
4. Aggiorna `sessione_corrente.md` (nota: "punto X raddrizzato / esteso").

## Fase 3 — Raddrizzamento strutturale (solo se la lacuna è vera)
Se ti accorgi che il programma **in sé** è troppo rapido su quel punto (non è solo
un chiarimento momentaneo), rendilo denso anche per il futuro, riusando il motore
di `/infittisci` **sulla sola sezione corrente** (qui basta **un** specialista, non
serve l'ondata):
- lo specialista cerca sul web quanto serve e spezza il concetto in una o più
  micro-lezioni aggiuntive da 5-10 min, fino a che la sezione **regge l'esame** al
  livello giusto (anti-banalità) — non si ferma "alla prima";
- scrive su un foglio `materie/<materia>/_lavori/<sezione>.md` (così, se interrompi,
  riprende da lì invece di rifare da capo);
- inserisci le nuove micro-lezioni in `programma-micro.md` al punto giusto,
  rinumerando con coerenza e **preservando i progressi** già fatti;
- aggiorna `sincronizzazione.md` (copertura) e `stato/progressi.md`.
- Per un approfondimento ampio di tutta la sezione, rimanda a
  `/infittisci <sezione>`.

## Fase 4 — Prezzo in tempo (solo se hai aggiunto lezioni)
Se la Fase 3 ha aggiunto micro-lezioni, esegui `/carico` per mostrare l'effetto
sul carico giornaliero. Un raddrizzamento solo "a voce" (Fase 2) non cambia il
carico e non richiede `/carico`.

## Chiusura
Riprendi la lezione da dove eravate: "Adesso che è più chiaro, andiamo avanti —
scrivi **avanti**, o `/raddrizza` di nuovo se serve ancora più lento."
