---
name: programma
description: Mostra il programma della materia attiva con lo stato di ogni lezione (completata, in corso, da fare, da ripassare), nella modalità attiva. Varianti per vedere tutto il programma, solo i moduli con percentuale, o le lezioni di un singolo modulo.
---

# /programma — Consulta il programma

Varianti:
- `/programma` → tutto il programma attivo con lo stato delle lezioni
- `/programma moduli` → solo i moduli con percentuale
- `/programma N` → solo le lezioni del modulo N

## Risoluzione della materia
Argomento esplicito → materia attiva in `stato/progressi.md` → altrimenti chiedi.

## Comportamento
1. Leggi `stato/progressi.md` per stato lezioni e modalità attiva.
2. Carica `materie/<materia>/programma-micro.md` (micro) o `programma.md` (standard).
3. Mostra il formato richiesto.

## Legenda stati
✓ completata · → in corso · ○ da fare · ⚠ da ripassare (punto debole)

## Formato `/programma`
```
📚 [materia] — Programma completo — Modalità: [micro/standard]
Avanzamento: XX%  |  Giorni alla prova: X

**Modulo 1 — [nome]** (X/Y completate)
  ✓ 1.1a — [titolo]
  → 1.1b — [titolo] ← sei qui
  ○ 1.1c — [titolo]
...
```

## Formato `/programma moduli`
```
📚 [materia] — Panoramica moduli — Giorni alla prova: X

✓ Modulo 1 — [nome] (100%)
→ Modulo 2 — [nome] (30%)
○ Modulo 3 — [nome] (0%)
```

## Formato `/programma N`
```
📚 [materia] — Modulo N — [nome]

  ✓ N.1a — [titolo]
  → N.1b — [titolo] ← sei qui
  ○ N.1c — [titolo]

Completamento: 33% (1/3)
Punti deboli: [lista o "nessuno"]
Prossimo passo: /tutor N.1b
```

I "Giorni alla prova" si calcolano dalla data esame registrata in `CLAUDE.md` /
`stato/progressi.md`.
