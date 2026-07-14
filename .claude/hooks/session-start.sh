#!/bin/bash
# SessionStart — configurazione di SVILUPPO del repo marketplace.
# NON fa parte del plugin distribuito agli studenti (vive in .claude/, non in
# plugins/road-to-mastery/).
#
# Perché esiste: Claude Code sul web gira in un sandbox effimero che riparte
# pulito a ogni sessione, e il marketplace dichiarato in settings.json non
# risulta configurato al CLI in quell'ambiente. Quindi qui, a ogni avvio,
# (ri)aggiungiamo il marketplace di Matt Pocock e (ri)installiamo il plugin
# `mattpocock-skills` — così le skill di grilling (grill-me, grilling,
# grill-with-docs) e le altre (tdd, code-review, diagnosing-bugs…) sono subito
# disponibili mentre sviluppi il plugin.
#
# In locale i plugin persistono da soli: lì questo hook non serve ed esce subito.
set -u

# Solo nell'ambiente remoto (Claude Code sul web).
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Serve il CLI `claude`; se manca, non bloccare la sessione.
if ! command -v claude >/dev/null 2>&1; then
  exit 0
fi

# Idempotente: se marketplace/plugin ci sono già, i comandi escono 0 senza
# rifare nulla. Best-effort: nessun errore deve impedire l'avvio della sessione.
claude plugin marketplace add mattpocock/skills >/dev/null 2>&1 || true
claude plugin install mattpocock-skills@mattpocock >/dev/null 2>&1 || true

exit 0
