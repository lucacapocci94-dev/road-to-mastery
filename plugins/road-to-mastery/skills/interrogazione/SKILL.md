---
name: interrogazione
description: Interrogazione severa ma motivante SOLO su ciò che lo studente ha già studiato nella materia attiva. Dà priorità ai punti deboli, cerca ogni domanda sul web, premia le risposte giuste e registra in silenzio esiti e nuovi punti deboli, suggerendo la lezione di recupero.
---

# /interrogazione — Mettiti alla prova sul già studiato

## Risoluzione della materia
Argomento esplicito → materia attiva in `stato/progressi.md` → altrimenti chiedi.
Percorsi: `materie/<materia>/...`.

## Fase 0 — Salva all'ingresso
Se `materie/<materia>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Fase 1 — Preparazione
- Leggi `stato/progressi.md`: considera solo lezioni `✓ completata` o `→ in corso`.
- Leggi `materie/<materia>/domande.md`: priorità ai punti deboli; salta ciò che è
  già solido.
- Ricerca web per ogni domanda:
  `WebSearch: "[argomento] [esame] [materia] risposta corretta [anno]"`
- Prepara 5-8 domande: prima i punti deboli, poi le lezioni completate.

## Fase 2 — Svolgimento (una domanda alla volta)
- **Corretta**: "Esatto. [conferma breve]" → avanti.
- **Parziale**: "Quasi — manca [X]. Completa."
- **Sbagliata**: "No. La risposta corretta è [X] perché [Y]." → registra punto debole.

## Fase 3 — Salvataggio dopo ogni risposta
Aggiorna `materie/<materia>/domande.md` e `stato/progressi.md` (stato lezioni,
punti deboli, calendario ripassi).

## Fase 4 — Chiusura
```
📋 Interrogazione completata — [materia]

Domande: X | Corrette: Y | Da rivedere: Z

Punti deboli emersi:
- [lezione X.Xa] — [concetto]

Per studiare i punti deboli: /tutor X.Xa
```

## Tono
Severa ma giusta. Premia esplicitamente le risposte corrette. Non essere
opprimente su risposte giuste ma imprecise nella forma: il feedback negativo
deve essere meritato.
