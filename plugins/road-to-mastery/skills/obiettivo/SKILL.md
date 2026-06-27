---
name: obiettivo
description: Costruisce un percorso di studio partendo dal risultato che vuoi ottenere, non dal syllabus. Parti dal tuo obiettivo concreto e dalla scadenza, da cosa già padroneggi, e ti disegna un percorso a ritroso giorno per giorno — ogni giorno un solo compito che sta in un tempo definito, un criterio chiaro per sapere se l'hai fatto bene, e cosa NON fare quel giorno per non sprecare tempo. Se il percorso non porta davvero all'obiettivo, lo ricostruisce. Registra l'obiettivo nello stato e lo tiene davanti agli occhi a ogni avvio.
---

# /obiettivo — Il percorso a ritroso dal risultato

`/organizza` parte dal **syllabus in avanti** (copertura). `/obiettivo` parte dal
**risultato all'indietro** (backward design): definisci dove vuoi arrivare e per
quando, e costruiamo solo ciò che ti ci porta. Si ispira a "il mio vero obiettivo
non è imparare X in generale: è ottenere un risultato specifico entro una
scadenza".

Invocata come `/obiettivo` (intervista) o `/obiettivo <risultato>`. Funziona
anche su una cartella nuova; se c'è già una materia, si aggancia ad essa.

## Fase 0 — Salva all'ingresso (se configurata)
Se `materie/<materia-attiva>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo.

## Fase 1 — Intervista breve (mai tecnica)
Chiedi, in linguaggio caldo e concreto, solo quattro cose:
1. **Risultato specifico** — cosa vuoi *saper fare* o *superare*, in concreto
   (non "imparare il diritto" ma "risolvere un parere in 60 minuti", "passare lo
   scritto di X").
2. **Scadenza** — entro quando.
3. **Punto di partenza** — cosa già padroneggi (così non si rifà l'ovvio).
4. **Tempo al giorno** realistico che puoi dedicare.

## Fase 2 — Ricerca web obbligatoria
```
WebSearch: "[risultato] cosa serve davvero requisiti criteri di valutazione"
WebSearch: "[risultato] errori che fanno fallire piano di preparazione efficace"
```
Capisci **cosa distingue chi ce la fa** da chi no.

## Fase 3 — Il percorso a ritroso (giorno per giorno)
Costruisci un percorso dalla scadenza all'indietro. Adatta il numero di giorni al
tempo disponibile (se la scadenza è lontana, ragiona a **tappe settimanali** con
un giorno-tipo). Ogni giorno/tappa deve avere **esattamente** tre cose:
- **Un solo compito**, dimensionato sul tempo dichiarato (es. ≤ 45 min).
- **Un criterio di riuscita** chiaro: come capisci da solo di averlo fatto bene.
- **Cosa NON fare** quel giorno, per non sprecare tempo su ciò che non serve
  all'obiettivo.

Parti da ciò che già padroneggia: niente compiti su cose già acquisite.

## Fase 4 — Controllo di tenuta (ferreo)
Verifica tu stesso: **questo percorso, eseguito, porta davvero al risultato entro
la scadenza?** Se no, **ricostruiscilo** (taglia, ridistribuisci, alza il tempo
al giorno) e dillo. Se nemmeno così ci sta, sii onesto sul gap e proponi la leva
(più tempo/giorno, scadenza, ambito ridotto) — come fa `/carico`.

## Fase 5 — Registra l'obiettivo (così non si perde)
- Scrivi/aggiorna in `stato/progressi.md` un blocco **`## Obiettivo attivo`**:
  risultato, scadenza, tempo/giorno, criterio di riuscita complessivo, data di
  definizione. (L'hook di avvio lo rimette davanti agli occhi a ogni sessione.)
- Se serve, salva il percorso giorno-per-giorno in
  `materie/<materia>/percorso-obiettivo.md` (o nella radice se non c'è materia).
- Una riga in **`stato/diario.md`** (data · "obiettivo fissato: [risultato] entro
  [scadenza]").

## Fase 6 — Avvio
Indica il **compito di oggi** e con quale comando eseguirlo (`/tutor`,
`/palestra`, `/operativo`, `/decifra` secondo il tipo di compito). Poi `/carico`
per il quadro tempo.

## Tono
Stratega lucido e onesto. L'obiettivo guida tutto: ogni cosa che non porta lì,
oggi, si taglia senza sensi di colpa.
