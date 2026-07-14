---
name: pubblica
description: Comando di SVILUPPO del repo marketplace (non distribuito agli studenti). Pubblica il plugin road-to-mastery — alza la versione (semver), aggiorna il CHANGELOG e porta le modifiche su main con auto-merge diretto — invocando scripts/pubblica.py. Usalo quando hai finito una modifica del motore e vuoi renderla disponibile via /plugin update.
---

# /pubblica — Rilascia una nuova versione del plugin (dev)

Comando per chi **sviluppa** il plugin, non per lo studente. Vive in `.claude/`
del repo marketplace, quindi non finisce nel plugin distribuito.

Pubblica lo stato attuale del plugin: alza la versione, scrive il changelog,
committa e fa **auto-merge diretto su `main`** (da lì il `/plugin update` degli
studenti pesca l'ultima versione).

## Cosa fare quando è invocato

1. **Assicurati che il lavoro del plugin sia già committato** sul branch corrente
   (lo script pubblica solo il commit di versione, non il resto).
2. Scegli il salto di versione in base alle modifiche:
   - `patch` — correzioni piccole;
   - `minor` — un comando nuovo o migliorie visibili (default sensato per una skill nuova);
   - `major` — cambiamenti che rompono l'uso esistente.
3. Prima fai sempre un giro a vuoto per mostrare il piano:
   ```
   python3 scripts/pubblica.py <patch|minor|major> -m "riga di changelog" --dry-run
   ```
4. Se il piano è giusto, esegui davvero (chiederà conferma prima del merge su main;
   `--yes` per saltarla, `--no-merge` per fermarti al commit senza toccare main):
   ```
   python3 scripts/pubblica.py <patch|minor|major> -m "riga di changelog"
   ```
5. Riporta l'esito: versione pubblicata e che gli studenti la riceveranno con
   `/plugin update`.

> Se `-m` non è dato, lo script compone il changelog dai messaggi dei commit del
> branch non ancora su main.
