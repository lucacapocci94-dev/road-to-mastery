# road-to-mastery (plugin)

Motore-tutor distribuibile. Fornisce:

- **3 hook** che salvano i progressi e ricaricano lo stato a ogni sessione
  (anche dopo una compattazione del contesto), indipendentemente da git.
- **Contratto del file system**: dove vivono programmi, stato e materie.
- **Validatore** del contratto (`tools/valida_contratto.py`).
- **Le skill** del motore: generiche e materia-aware, agganciate al contratto del
  file system. Due famiglie: il **nucleo da esame** (copertura del syllabus) e gli
  **strumenti di apprendimento profondo** (i 6 prompt del tutor da zero, esplosi).

## Hook

| Hook | Evento | Cosa fa |
|---|---|---|
| `carica_e_riconcilia.py` | SessionStart | inietta lo stato nel contesto + **obiettivo attivo**, **ultime tappe del diario** e **ultimo salvataggio**; segnala sessioni non consolidate |
| `checkpoint.py` | Stop | commit + push (se git disponibile) di `stato/` e `materie/` |
| `chiusura.py` | SessionEnd | consolidamento finale + push di sicurezza |

**Tracciabilità senza fatica.** La storia leggibile del percorso vive in
`stato/diario.md`: lo aggiornano le skill (una riga per tappa, in italiano
semplice) e lo rilegge l'avvio per dire allo studente "dove sei rimasto". Funziona
**anche senza git**: i file su disco sono la verità, git è solo copia di
sicurezza. Allo studente non si parla mai di commit/push/PR.

## Skill — nucleo da esame (copertura del syllabus)

| Skill | Cosa fa |
|---|---|
| `/organizza` | bootstrap della cartella-studente: struttura, programmi con controllo di copertura, CLAUDE.md, diario |
| `/tutor` | lezione interattiva con ricerca web e teach-back |
| `/testa` | verifica delle conoscenze pregresse su un modulo |
| `/interrogazione` | domande sul già studiato, priorità ai punti deboli |
| `/simulazione` | prova d'esame realistica su tutto il programma |
| `/infittisci` | approfondisce il programma su più livelli, un sub-agente per sezione, poi fonde |
| `/rinnova` | aggiorna un programma esistente quando la materia è cambiata: aggiunge, modifica e rimuove (con conferma) da fonti tue o dal web, preservando i progressi |
| `/raddrizza` | corregge il tiro a lezione iniziata: rispiega e, se serve, approfondisce la sezione corrente |
| `/carico` | carico di studio giornaliero e semaforo di fattibilità rispetto alla data |
| `/modalita` | passa tra micro (5-10 min) e standard (30-90 min) |
| `/programma` | mostra il programma con lo stato delle lezioni |
| `/avanzamento` | progressi per materia, ripassi dovuti, copertura del syllabus |
| `/aggiornami` | controlla se c'è una versione più recente del plugin e ti guida all'aggiornamento (`/plugin update`), mostrando le novità dal changelog |
| `/help` | guida completa a tutti i comandi |

## Skill — apprendimento profondo (i 6 prompt del tutor da zero, esplosi)

Funzionano su qualsiasi argomento o esame, **anche senza una cartella configurata**.

| Skill | Cosa fa |
|---|---|
| `/operativo` | 80/20 spietato: cosa imparare per primo, cosa ignorare, l'esercizio che ti mette avanti; poi un passo alla volta |
| `/decifra` | sblocca un contenuto ostico (incollalo o indica un file): idea-chiave + analogia + 3 domande-cancello |
| `/palestra` | impari sull'errore in situazioni reali; l'AI non regala la risposta, ti fa trovare dove ti rompi |
| `/lacune` | 5 domande che smontano l'eccesso di sicurezza ed espongono i buchi nascosti |
| `/spiegamelo` | Feynman forzato: spieghi tu, l'AI ti ferma su termini, salti e semplificazioni sbagliate |
| `/obiettivo` | percorso a ritroso dal risultato+scadenza: un compito al giorno, criterio di riuscita, cosa NON fare |
| `/diario` | la linea del tempo del tuo studio; si aggiorna da solo |

Tutte le skill leggono/scrivono **solo** dentro il contratto del file system,
fanno ricerca web prima di generare contenuti didattici, rispondono in italiano e
salvano lo stato in silenzio.
