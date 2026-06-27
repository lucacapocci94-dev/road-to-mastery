---
name: diario
description: Mostra in italiano semplice la linea del tempo di tutto il tuo percorso — cosa hai studiato e quando, le tappe raggiunte, i punti deboli emersi e dove sei arrivato adesso — leggendo il diario di studio che il motore aggiorna da solo. Serve a sapere a colpo d'occhio "dove sono rimasto" senza dover ricordare nulla né tenere conti a mano. Niente git, niente tecnicismi — solo il racconto del tuo studio.
---

# /diario — Dove sei arrivato, a colpo d'occhio

`/diario` è la **tracciabilità leggibile** del percorso: legge
`stato/diario.md` — il registro in italiano semplice che il motore aggiorna in
automatico a ogni lezione, verifica, approfondimento o cambio di obiettivo — e te
lo racconta. Non devi tenere nessun conto a mano; non si parla mai di git.

## Comportamento
1. Leggi `stato/diario.md`. Se non esiste ancora, crealo con un'intestazione e
   spiega in una riga che da ora il percorso si registra da solo.
2. Leggi `stato/progressi.md` per **dove sei adesso** (materia attiva, %,
   obiettivo attivo se presente, ripassi dovuti oggi).
3. Mostra la linea del tempo dal più recente, raggruppata per data.

## Varianti
- `/diario` → ultime tappe + dove sei ora + prossimo passo suggerito.
- `/diario tutto` → l'intera storia del percorso.
- `/diario <materia>` → solo le tappe di quella materia.

## Formato
```
🗒️ Il tuo percorso — [oggi] — Giorni alla prova: X

Dove sei ora: [materia attiva] · [%] · obiettivo: [se presente]
Ultimo salvataggio automatico: [da .road-to-mastery.log se c'è, altrimenti
"i tuoi file sono già salvati sul disco"]

Ultime tappe:
- [data] · [materia] · [cosa è successo]
- [data] · [materia] · [cosa è successo]

Punti deboli aperti: [lista o "nessuno"]
Prossimo passo: [/tutor X.Xa o il comando giusto]
```

## Manutenzione del diario (regola per tutte le skill)
Il diario non si compila a mano. **Ogni skill che fa progredire lo studio**
(`/tutor`, `/testa`, `/interrogazione`, `/simulazione`, `/operativo`, `/palestra`,
`/decifra`, `/obiettivo`, `/lacune`, `/spiegamelo`, `/infittisci`, `/raddrizza`)
aggiunge **una riga** a `stato/diario.md` a fine attività, in silenzio:
`- [AAAA-MM-GG] · [materia] · [in una frase: cosa è stato fatto / tappa / lacuna]`.
Le tappe più recenti restano in alto. È questo file che l'hook di avvio rilegge
per dirti "bentornato, l'ultima volta…".

## Tono
Caldo e incoraggiante: è la fotografia dei tuoi passi, non un registro burocratico.
