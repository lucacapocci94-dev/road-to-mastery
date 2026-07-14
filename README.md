# Road to Mastery — Marketplace

Marketplace Claude Code che ospita il plugin **road-to-mastery**, un motore-tutor
per la preparazione a qualsiasi esame.

## Installazione

```
/plugin marketplace add lucacapocci94-dev/road-to-mastery
/plugin install road-to-mastery@road-to-mastery
```

Aggiornamenti: `/plugin update`. Dentro una cartella di studio, il comando
`/aggiornami` controlla se c'è una versione nuova e ti guida ad installarla.

Il plugin vive in `plugins/road-to-mastery/`.

## Sviluppo del plugin

Per rilasciare una nuova versione (alza il semver, aggiorna il CHANGELOG e fa
auto-merge diretto su `main`, da cui gli studenti la ricevono con
`/plugin update`):

```
python3 scripts/pubblica.py <patch|minor|major> -m "cosa cambia" --dry-run   # anteprima
python3 scripts/pubblica.py <patch|minor|major> -m "cosa cambia"             # pubblica
```

È anche il comando di sviluppo `/pubblica` (in `.claude/`, non distribuito).
Questo script sta **fuori** da `plugins/`, quindi non finisce nel plugin che
usano gli studenti.
