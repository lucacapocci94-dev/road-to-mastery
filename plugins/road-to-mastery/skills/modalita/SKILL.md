---
name: modalita
description: Mostra o cambia la modalità di studio tra micro (lezioni da 5-10 minuti, default) e standard (lezioni complete da 30-90 minuti). La preferenza è globale e vale per tutte le materie; viene salvata in stato/progressi.md.
---

# /modalita — Modalità di studio

Tre varianti:
- `/modalita` → mostra la modalità attiva
- `/modalita micro` → attiva il programma micro (default)
- `/modalita standard` → attiva il programma standard

La modalità è una preferenza **globale**, salvata in `stato/progressi.md`
(campo "Modalità attiva"). Determina quale file usano le altre skill:
`programma-micro.md` (micro) o `programma.md` (standard) della materia attiva.

## `/modalita` (senza argomenti)
Leggi `stato/progressi.md`, trova "Modalità attiva", rispondi:
"Stai usando la modalità **[micro/standard]**.
- **Micro**: lezioni da 5-10 minuti, un concetto alla volta ← default
- **Standard**: lezioni complete da 30-90 minuti
Per cambiare: `/modalita standard` oppure `/modalita micro`."

## `/modalita micro`
Aggiorna `stato/progressi.md` → "Modalità attiva: micro". Rispondi:
"Modalità micro attivata ✓ — prossime lezioni da 5-10 minuti. Scrivi `/tutor` quando vuoi."

## `/modalita standard`
Aggiorna `stato/progressi.md` → "Modalità attiva: standard". Rispondi:
"Modalità standard attivata ✓ — prossime lezioni complete (30-90 minuti). Scrivi `/tutor` quando vuoi."
