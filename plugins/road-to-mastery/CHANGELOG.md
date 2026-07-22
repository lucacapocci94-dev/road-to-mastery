# Changelog — road-to-mastery

Le novità del motore-tutor, dalla più recente. Il comando `/aggiornami` legge
questa lista per dirti **cosa cambia** quando c'è una versione nuova da installare.

Formato: una sezione `## X.Y.Z` per versione, con le novità in elenco.

## 0.13.0 — 2026-07-22
- Auto-installazione del plugin sul web via SessionStart hook (install-plugin.sh); /configura e /organizza aggiornati

## 0.12.0 — 2026-07-21
- Nuovo comando /configura: (ri)crea le configurazioni cloud (marketplace + plugin abilitato, hook di auto-merge, pin del branch) su una cartella già allestita, così i comandi del tutor ricompaiono da soli in ogni sessione web, desktop e mobile. È il Passo 5-bis di /organizza estratto in un comando dedicato e idempotente, per quando le configurazioni mancano o vanno riparate.

## 0.11.0 — 2026-07-21
- Persistenza cloud: /organizza configura da se' ogni cartella (comandi nativi dal marketplace + auto-merge sul branch di consolidamento), cosi' ogni sessione web e mobile parte gia' pronta senza passaggi manuali. Auto-merge generalizzato con rilevamento del branch di default.

## 0.10.1
- `/aggiornami`: ora **rinfresca davvero il marketplace** e confronta la versione
  in uso con quella **disponibile nella cache** (non più con un branch di GitHub),
  poi installa l'aggiornamento. Basta falsi "sei già aggiornato".
- `/condividi`: corretto un bug grave — non tocca più la tua cartella. La sorgente
  è in sola lettura, l'azzeramento avviene solo nella copia, e viene condivisa
  esattamente la materia richiesta (non quella attiva). Rete di sicurezza che
  rifiuta destinazioni dentro la tua cartella di studio.

## 0.10.0
- Nuovo comando `/condividi`: impacchetta uno o più programmi in un `.zip` pulito
  da regalare a chi deve fare lo stesso corso — solo le materie scelte, progressi
  azzerati e nessun dato personale. Condivide il programma, non il motore.

## 0.9.1
- `/aggiornami`: corrette le istruzioni di aggiornamento. Per installare l'ultima
  versione usa il menu `/plugin` → Installed → road-to-mastery → Update, oppure il
  nome qualificato `road-to-mastery@road-to-mastery`.

## 0.9.0
- Nuovo comando `/aggiornami`: controlla se sul marketplace c'è una versione più
  recente del plugin, ti mostra le novità e ti guida all'aggiornamento.

## 0.8.0
- Nuovo comando `/rinnova`: aggiorna un programma già esistente quando la materia
  stessa è cambiata (aggiunge, modifica e rimuove con conferma), preservando i
  progressi già fatti. Diverso da `/infittisci`, che approfondisce senza cambiare
  i concetti né togliere.

## Versioni precedenti
La storia completa delle versioni prima della 0.8.0 è nei commit del repository.
