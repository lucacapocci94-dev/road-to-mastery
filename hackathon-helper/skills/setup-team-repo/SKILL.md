---
name: setup-team-repo
description: Crea in un comando il repository GitHub del team per un hackathon. Una sola repo con cartelle frontend/ e backend/ (scheletro gia funzionante con Claude cablato), aggiunge il compagno come collaboratore e fa il primo push. Usa quando l'utente vuole inizializzare il progetto dell'hackathon, creare la repo del team, partire da zero velocemente in coppia, o "prepara il setup".
---

# Setup repo del team (hackathon)

Obiettivo: in circa 1 minuto, tu e il tuo compagno siete operativi su GitHub con uno scheletro che gia gira (frontend che chiama un backend che parla con Claude).

## Cosa serve PRIMA (preparalo la sera prima)

- Tu e il compagno: **un account GitHub** a testa (sappiate i rispettivi username).
- Sul tuo PC: **git** e la **GitHub CLI `gh`** installati e autenticati (`gh auth login`).
- Per la demo con Claude: una **chiave API** da incollare in `backend/.env` (vedi sotto). All'evento la danno spesso loro.

## Processo

1. Chiedi all'utente, una cosa alla volta:
   - il **nome del progetto** (diventa il nome della repo, es. `team-rocket-poc`)
   - lo **username GitHub del compagno** (per aggiungerlo come collaboratore)
   - se la repo deve essere **privata** (default consigliato) o pubblica

2. Lancia lo script `setup.sh` di questa skill (si trova nella base directory della skill) passando nome progetto e username del compagno:

   ```bash
   bash "<base-directory-skill>/setup.sh" <nome-progetto> <username-compagno>
   ```

   Lo script:
   - copia lo scheletro da `templates/` in una nuova cartella `<nome-progetto>/`
   - fa `git init` + primo commit
   - crea la repo su GitHub con `gh repo create ... --push`
   - aggiunge il compagno come **collaboratore** (deve accettare l'invito)
   - stampa il comando di clone per entrambi

3. Dopo lo script, ricorda all'utente di:
   - copiare `backend/.env.example` in `backend/.env` e incollare la chiave Claude
   - seguire `README.md` dentro il progetto per avviare frontend e backend in locale

## Regole di design (importante)

- **UNA sola repo** con `frontend/` e `backend/`: ognuno lavora nella sua cartella, niente conflitti, **un solo link** da consegnare ai giudici.
- **Niente deploy obbligatorio, niente GitHub Actions/CI**: in un hackathon di 5-6 ore non servono. La demo gira in locale + (eventuale) video.
- Lo scheletro e volutamente minimo: un bottone -> backend -> Claude -> risposta. E gia demolabile; le feature vere si aggiungono sopra.
