---
name: carico
description: Calcola il carico di studio realistico per arrivare pronti alla data d'esame — micro-lezioni rimaste, lezioni e minuti al giorno necessari, e un semaforo di fattibilità (verde, giallo, rosso). È il regolatore che bilancia profondità e tempo, e si esegue da solo dopo ogni /infittisci per mostrare quanto costa in tempo ogni approfondimento.
---

# /carico — Il regolatore: quanto studiare al giorno

`/carico` traduce il programma in un **piano realistico**: dato quanto resta e
quanti giorni mancano, ti dice **quante lezioni e quanti minuti al giorno** servono
per arrivare pronto — e se è davvero fattibile.

## Risoluzione della materia
- `/carico` → materia attiva (da `stato/progressi.md`)
- `/carico <materia>` → quella materia
- `/carico tutte` → quadro complessivo su tutte le materie

## Dati da raccogliere
1. **Data di oggi**: `date +%Y-%m-%d`.
2. **Data d'esame**: da `stato/progressi.md` / `CLAUDE.md`.
3. **Modalità attiva** (micro o standard) da `stato/progressi.md`.
4. **Totale e stato lezioni**: conta nel `programma-micro.md` (micro) o
   `programma.md` (standard) della materia quante lezioni esistono e quante sono
   già `✓ completata`.

## Calcolo
- `rimaste = totali − completate`
- `giorni = giorni di calendario da oggi alla data d'esame` (se lo studente ti ha
  detto giorni di pausa o giorni/settimana di studio, usali; altrimenti calendario
  pieno e dillo).
- `lezioni_al_giorno = ceil(rimaste / giorni)`
- `minuti_lezione`: micro ≈ 8 min, standard ≈ 60 min.
- `minuti_al_giorno = lezioni_al_giorno × minuti_lezione` (aggiungi un margine per
  i **ripassi dovuti** dal calendario ripassi in `progressi.md`, se presenti).

## Semaforo di fattibilità (su minuti/giorno)
- 🟢 **fattibile**: ≤ 60 min/giorno
- 🟡 **teso**: 60–120 min/giorno
- 🔴 **non ci sta**: > 120 min/giorno

## Output
```
📊 Carico di studio — [materia] — oggi [data]

Lezioni: [completate]/[totali]  ·  rimaste: [rimaste]
Giorni alla prova: [giorni]

Servono: [lezioni_al_giorno] lezioni/giorno  (~[minuti_al_giorno] min/giorno)
Stato: [🟢 fattibile / 🟡 teso / 🔴 non ci sta]

Ripassi previsti nei prossimi giorni: [n, dal calendario ripassi]
```

## Se è 🟡 o 🔴 — proposte concrete (mai lasciare lo studente nel panico)
Suggerisci, in ordine, le leve realistiche:
1. **Studiare un po' di più al giorno** (di' di quanto servirebbe).
2. **Alleggerire la profondità** di qualche sezione (livello più basso con
   `/infittisci` o chiedendomi di ridurre).
3. **Dare priorità ai temi ⭐** del programma, rimandando i secondari.
Mostra l'effetto stimato di ciascuna leva ("con 20 min in più al giorno torni in 🟢").

## Quando si esegue
- Su richiesta esplicita (`/carico`).
- **Automaticamente alla fine di `/infittisci`**, per mostrare subito il prezzo in
  tempo dell'approfondimento appena fatto.
