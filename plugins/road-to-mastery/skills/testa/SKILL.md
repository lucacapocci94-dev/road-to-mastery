---
name: testa
description: Autovalutazione delle conoscenze pregresse su un modulo intero della materia attiva, per non far perdere tempo su ciò che lo studente già padroneggia. Cerca le domande sul web, le pone una alla volta, certifica le lezioni superate in progressi.md e segnala i punti deboli con la lezione di recupero consigliata.
---

# /testa — Verifica delle conoscenze pregresse

Invocata come `/testa N` (modulo N) o `/testa` (chiede quale modulo). Serve a
certificare ciò che lo studente già sa, senza rifargli studiare l'ovvio.

## Risoluzione della materia
Argomento esplicito → materia attiva in `stato/progressi.md` → altrimenti chiedi.
Tutti i percorsi sono `materie/<materia>/...`.

## Fase 0 — Salva all'ingresso
Se `materie/<materia>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Fase 1 — Scegli il modulo
Leggi `materie/<materia>/programma-micro.md` per l'elenco reale dei moduli (mai
elenchi fissi inventati). Se l'utente non indica il numero, mostragli i moduli
disponibili e chiedi quale testare.

## Fase 2 — Preparazione
- Leggi `materie/<materia>/domande.md`: escludi le domande già risposte
  correttamente.
- Ricerca web:
  `WebSearch: "[esame] [materia] [nome modulo] domande tipiche [anno]"`
- Prepara 6-10 domande distribuite su tutte le lezioni del modulo.

## Fase 3 — Svolgimento (una domanda alla volta)
Tutte le domande nascono da ricerca web, mai a memoria.

- **Corretta e completa**: "Esatto! [conferma]". Salva in `domande.md`
  (data, modulo, domanda, esito = corretta). Segna la lezione `✓` in
  `progressi.md`. Prossima.
- **Imprecisa** (concetto giusto, dettaglio sbagliato): dialogo correttivo breve
  (max 2-3 scambi con esempi). Salva esito = corretta dopo dialogo + nota.
  Segna `✓`. Prossima.
- **Sbagliata** (concetto non capito): spiega il punto chiave in 2-3 righe. Salva
  esito = sbagliata + nota. Segna `⚠ punto debole` in `progressi.md`. Cerca in
  `programma-micro.md` la lezione pertinente e consiglia `/tutor X.Xa`.

Criterio dialogo vs `/tutor`: se si sistema in 2-3 scambi → dialogo; se il
concetto è proprio mancante → `/tutor`.

## Fase 4 — Verdetto finale
```
✅ Test Modulo N completato — [materia]

Domande: X | Corrette: Y | Corrette dopo dialogo: Z | Da approfondire: W

Lezioni certificate: [lista — contano come studiate]
Punti deboli: [lista con /tutor consigliato per ognuno]
```
Aggiorna `progressi.md` (incluso calendario ripassi per le lezioni certificate).
