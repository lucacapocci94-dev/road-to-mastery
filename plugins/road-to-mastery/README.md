# road-to-mastery (plugin)

Motore-tutor distribuibile. Fornisce:

- **3 hook** che salvano i progressi e ricaricano lo stato a ogni sessione
  (anche dopo una compattazione del contesto), indipendentemente da git.
- **Contratto del file system**: dove vivono programmi, stato e materie.
- **Validatore** del contratto (`tools/valida_contratto.py`).

Le skill (`/organizza`, `/tutor`, `/testa`, …) arrivano nel Piano 2.

## Hook

| Hook | Evento | Cosa fa |
|---|---|---|
| `carica_e_riconcilia.py` | SessionStart | inietta lo stato nel contesto; segnala sessioni non consolidate |
| `checkpoint.py` | Stop | commit + push (se git disponibile) di `stato/` e `materie/` |
| `chiusura.py` | SessionEnd | consolidamento finale + push di sicurezza |
