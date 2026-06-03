---
name: simulazione
description: Simulazione d'esame severa come una commissione reale, su tutto il programma della materia attiva. Scrive l'esito su file PRIMA di mostrare ogni feedback, non si interrompe mai e non offre lezioni durante la prova. Registra punti deboli e risultati e propone i recuperi alla fine.
---

# /simulazione — Prova d'esame realistica

## Regola fondamentale
**SCRIVI SUL FILE PRIMA di mostrare qualsiasi feedback** (corretto o sbagliato).
La simulazione non si interrompe mai e non offre `/tutor` durante la prova.

## Risoluzione della materia
Argomento esplicito → materia attiva in `stato/progressi.md` → altrimenti chiedi.
Percorsi: `materie/<materia>/...`.

## Fase 0 — Salva all'ingresso
Se `materie/<materia>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Avvio
1. Leggi `materie/<materia>/domande.md` per individuare i punti deboli.
2. Ottieni la data: `date +%Y-%m-%d`.
3. Crea/apri `materie/<materia>/simulazioni/YYYY-MM-DD.md` con intestazione tabella
   (`| # | Domanda | Esito | Note |`).
4. Ricerca web: `WebSearch: "[esame] [materia] domande commissione [anno]"`.
5. Prima domanda.

## Ordine delle domande
1. Argomenti già sbagliati in passato (`domande.md`).
2. Argomenti già studiati (consolidamento).
3. Argomenti non ancora affrontati (test a freddo).

Per ogni domanda: `WebSearch: "[argomento] [esame] [materia] domande orale [anno]"`.

## Ad ogni risposta
Scrivi prima su `simulazioni/YYYY-MM-DD.md`:
- Corretta: `| N | [domanda] | ✅ | |`
- Sbagliata: `| N | [domanda] | ❌ | [concetto mancante] |`

Poi mostra il feedback (correzione breve + risposta corretta completa se sbagliata)
e passa alla prossima.

## Chiusura ("basta"/"fine"/"stop" o dopo 15 domande)
1. Aggiungi al file un `## Riepilogo` (domande, corrette %, sbagliate, punti deboli).
2. Aggiorna `materie/<materia>/domande.md` con le domande sbagliate.
3. Aggiorna `stato/progressi.md` (risultati, punti deboli, calendario ripassi).
4. Svuota/segna chiusa `sessione_corrente.md`.
5. Mostra il riepilogo:
```
🎯 Simulazione completata — [materia]

Domande: X | Corrette: Y | Errate: W

Punti deboli: [concetto] → /tutor [lezione]
Argomenti solidi: [concetto] ✓

Per un'altra simulazione: /simulazione
```
6. Suggerisci `/compact` per ripartire con la memoria fresca.
