---
name: avanzamento
description: Mostra i progressi di studio con le percentuali per modulo e per materia, i punti deboli da ripassare, i ripassi dovuti oggi e — invariante di copertura — gli eventuali punti del syllabus non ancora coperti da alcuna micro-lezione. Niente sparisce in silenzio.
---

# /avanzamento — Quadro dei progressi

Varianti:
- `/avanzamento` → quadro globale (tutte le materie)
- `/avanzamento N` → dettaglio del modulo N della materia attiva

## Comportamento
Leggi `stato/progressi.md` (registro globale: materie, materia attiva, %, punti
deboli, calendario ripassi). Per l'invariante di copertura leggi
`materie/<materia>/sincronizzazione.md`. Calcola le percentuali e mostra i dati.

## Formato `/avanzamento` (globale, multi-materia)
```
📈 I tuoi progressi — [data oggi] — Giorni alla prova: X

**Materia attiva: [materia]**

| Materia | % | Fatte/Totali |
|---|---|---|
| [materia A] | 60% | 11/18 |
| [materia B] | 0% | 0/16 |

**Ripassi dovuti oggi:** [lista lezioni dal calendario ripassi, o "nessuno"]

**Punti deboli da ripassare:**
- [materia] · [lezione X.X] — [concetto]

**⚠ Copertura del syllabus:** [es. "3 punti non ancora coperti da nessuna
micro-lezione" oppure "tutto coperto"]

**Prossima lezione suggerita:** /tutor [X.Xa]
```

## Formato `/avanzamento N`
```
📈 [materia] — Modulo N — [nome]

Completamento: XX%

  ✓ N.1a — completata il [data]
  → N.1c — in corso
  ○ N.1d — da fare
  ⚠ N.1b — punto debole: [concetto]

Ripassi dovuti: [lista o "nessuno"]
Prossimo passo: /tutor N.1c
```

## Invariante di copertura
Se in `sincronizzazione.md` un punto del syllabus non mappa su alcuna
micro-lezione, **dillo esplicitamente**: la completezza non deve dipendere dalla
fortuna. Suggerisci `/organizza` per colmare i buchi.
