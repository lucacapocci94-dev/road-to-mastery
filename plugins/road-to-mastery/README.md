# road-to-mastery (plugin)

Motore-tutor distribuibile. Fornisce:

- **3 hook** che salvano i progressi e ricaricano lo stato a ogni sessione
  (anche dopo una compattazione del contesto), indipendentemente da git.
- **Contratto del file system**: dove vivono programmi, stato e materie.
- **Validatore** del contratto (`tools/valida_contratto.py`).
- **9 skill** del nucleo v1 (`/organizza`, `/tutor`, `/testa`, …): generiche e
  materia-aware, agganciate al contratto del file system.

## Hook

| Hook | Evento | Cosa fa |
|---|---|---|
| `carica_e_riconcilia.py` | SessionStart | inietta lo stato nel contesto; segnala sessioni non consolidate |
| `checkpoint.py` | Stop | commit + push (se git disponibile) di `stato/` e `materie/` |
| `chiusura.py` | SessionEnd | consolidamento finale + push di sicurezza |

## Skill (nucleo v1)

| Skill | Cosa fa |
|---|---|
| `/organizza` | bootstrap della cartella-studente: struttura, programmi con controllo di copertura, CLAUDE.md |
| `/tutor` | lezione interattiva con ricerca web e teach-back |
| `/testa` | verifica delle conoscenze pregresse su un modulo |
| `/interrogazione` | domande sul già studiato, priorità ai punti deboli |
| `/simulazione` | prova d'esame realistica su tutto il programma |
| `/infittisci` | approfondisce il programma su più livelli, un sub-agente per sezione, poi fonde |
| `/raddrizza` | corregge il tiro a lezione iniziata: rispiega e, se serve, approfondisce la sezione corrente |
| `/carico` | carico di studio giornaliero e semaforo di fattibilità rispetto alla data |
| `/modalita` | passa tra micro (5-10 min) e standard (30-90 min) |
| `/programma` | mostra il programma con lo stato delle lezioni |
| `/avanzamento` | progressi per materia, ripassi dovuti, copertura del syllabus |
| `/help` | guida completa a tutti i comandi |

Tutte le skill leggono/scrivono **solo** dentro il contratto del file system,
fanno ricerca web prima di generare contenuti didattici, rispondono in italiano e
salvano lo stato in silenzio.
