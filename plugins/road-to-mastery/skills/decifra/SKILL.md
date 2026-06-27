---
name: decifra
description: Decodifica un contenuto che ti confonde (una dispensa, una norma, un paragrafo, un paper, un appunto) e ti ci fa interrogare sopra. Prima di spiegare qualsiasi cosa trova l'unica idea centrale che, una volta capita, fa andare il resto al suo posto, e la spiega con un'analogia di tutti i giorni senza termini tecnici. Poi ti fa 3 domande che solo chi ha davvero capito saprebbe superare, una alla volta, e non va oltre finché non le superi tutte e tre. Incolla il testo, indica un file o dimmi l'argomento.
---

# /decifra — Sblocca un contenuto ostico ("grill me with docs")

Quando un materiale ti confonde, `/decifra` non lo riassume: lo **rende
afferrabile** e poi ti **interroga su quello**. Si ispira a "dimmi prima l'unica
idea che fa andare il resto a posto, poi mettimi alla prova".

## Cosa può ricevere
- **Testo incollato** dopo il comando (`/decifra <incolla qui il contenuto>`).
- **Un file** indicato ("decifra il file materiali/dispensa.pdf"): leggilo.
- **Solo un argomento**: in quel caso recupera il contenuto con ricerca web.

Funziona **anche senza cartella configurata**.

## Fase 0 — Salva all'ingresso (se configurata)
Se `materie/<materia-attiva>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Fase 1 — Ricerca web (se serve)
Se il contenuto è incollato/da file, usa il web **solo** per chiarire i punti
oscuri o verificare dati e date. Se hai solo l'argomento, cerca fonti aggiornate
e autorevoli. Normative/dati: cita anno e fonte.

## Fase 2 — L'idea-chiave per prima (regola ferrea)
1. **Prima di spiegare qualsiasi dettaglio**, individua l'**unica idea centrale**
   che, capita quella, fa cadere tutto il resto al suo posto.
2. **Spiega solo quell'idea**, con un'**analogia di tutti i giorni** e **senza
   termini tecnici**. Niente elenco di definizioni: una porta d'ingresso.

## Fase 3 — Le 3 domande-cancello (una alla volta)
Poni **3 domande** a cui solo chi ha **davvero capito** quell'idea saprebbe
rispondere (non domande di memoria: domande di comprensione applicata).

- Falle **una alla volta** e **aspetta** ogni risposta.
- Risposta giusta → conferma breve e passa alla successiva.
- Risposta debole → riporta all'analogia, aggiusta, **rifai** una domanda
  equivalente. **Non passare oltre finché non superi tutte e tre.**

## Fase 4 — Poi, e solo poi, il resto
Superato il cancello, spiega il resto del contenuto **costruendo sull'idea-chiave**
ormai solida (dal centro verso i dettagli, dal concreto alla teoria).

## Fase 5 — Salvataggio silenzioso (se la cartella esiste)
- Se il contenuto mappa su una lezione del programma, aggiorna la copertura in
  `sincronizzazione.md` e annota in `domande.md` le 3 domande-cancello.
- Una riga in **`stato/diario.md`** (data · "decifrato [titolo/argomento]:
  idea-chiave = …").

## Tono
Traduttore paziente. L'obiettivo è il momento "ah, ecco!", non l'esibizione di
completezza. Se lo studente resta confuso, cambia analogia, non alza il registro.
