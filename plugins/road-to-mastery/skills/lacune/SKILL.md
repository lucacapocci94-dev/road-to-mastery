---
name: lacune
description: Smonta l'eccesso di sicurezza su un argomento che credi di padroneggiare già. Ti fa cinque domande che sembrano semplici ma espongono le lacune di chi non è mai andato davvero in profondità, una alla volta, e dopo ogni risposta ti dice esattamente cosa rivela su ciò che ancora manca nelle tue basi. Non ti va leggero — se sei superficiale te lo dice in faccia. Registra in silenzio le lacune trovate come punti deboli, con la lezione di recupero.
---

# /lacune — Trova i buchi che non sai di avere

Diverso da `/testa` (che certifica ciò che sai per **farti saltare** l'ovvio):
`/lacune` parte dal sospetto opposto — **credi di sapere, dimostriamo che c'è un
fondo che manca**. Si ispira a "voglio che tu mi dimostri che mi sbaglio".

Invocata come `/lacune <argomento>` oppure `/lacune` (usa la materia/lezione
attiva o lo chiede). Funziona anche **senza cartella configurata**.

## Risoluzione dell'argomento
Argomento esplicito → materia/lezione attiva da `stato/progressi.md` → altrimenti
chiedi: "Su cosa ti senti già sicuro? Lo metto alla prova." Mai indovinare.

## Fase 0 — Salva all'ingresso (se configurata)
Se `materie/<materia-attiva>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Fase 1 — Ricerca web obbligatoria
```
WebSearch: "[argomento] domande difficili concetti spesso fraintesi [esame/materia]"
WebSearch: "[argomento] eccezioni casi limite dettagli che sfuggono ai più"
```
Ti servono le domande **ingannevolmente semplici** che separano la comprensione
vera dal "l'ho letto una volta".

## Fase 2 — Le 5 domande (una alla volta, senza sconti)
Poni **5 domande** che **sembrano semplici** ma espongono le lacune di chi non è
mai andato davvero in profondità (il "perché", non il "cosa"; le eccezioni; i
confini; il caso che sembra uguale ma non lo è).

- Falle **una alla volta** e **aspetta** ogni risposta.
- **Dopo ogni risposta**, di' esplicitamente **cosa rivela**: cosa è solido e
  cosa, in base a quella risposta, manca ancora nelle basi.
- **Non andarci leggero.** Se la risposta è superficiale, **dillo direttamente**,
  con rispetto ma senza addolcire. Niente complimenti di cortesia.

## Fase 3 — Verdetto e salvataggio silenzioso
```
🔎 Lacune — [argomento]
Solido su: [punti]
Buchi reali: [punti, dal più importante]
Da colmare per primo: [il buco che regge gli altri] → /tutor [lezione] o /decifra
```
Se la cartella esiste:
- ogni buco reale → `materie/<materia>/domande.md` come **punto debole** e `⚠` in
  `stato/progressi.md` con la lezione di recupero;
- una riga in **`stato/diario.md`** (data · "lacune su [argomento]: buchi = …").

## Tono
Onesto fino a essere scomodo, mai umiliante. L'obiettivo è il rispetto della
verità sul proprio livello: meglio scoprire il buco qui che all'esame.
