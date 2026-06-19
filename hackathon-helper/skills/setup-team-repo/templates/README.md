# {Nome del progetto}

POC per l'hackathon. Una repo, due cartelle: ognuno lavora nella sua, niente conflitti.

```
frontend/   <- l'interfaccia (pagina web, zero build)
backend/    <- il server che parla con Claude
```

## Avvio in locale (la demo gira sul tuo PC, basta cosi)

### 1. Backend
```bash
cd backend
cp .env.example .env        # poi apri .env e incolla la tua chiave Claude
npm install
npm start                   # parte su http://localhost:3001
```

### 2. Frontend
Apri semplicemente `frontend/index.html` nel browser (doppio clic).
Clicca il bottone: il frontend chiama il backend, che chiede a Claude e mostra la risposta.

> Se il browser blocca le richieste, servi la cartella con un mini-server, es:
> `cd frontend && python3 -m http.server 5500` e apri http://localhost:5500

## Come dividerci il lavoro
- Uno tiene `frontend/`, l'altro `backend/`. Vi accordate sul "contratto": il frontend chiama `POST /api/ask` con `{ "prompt": "..." }` e riceve `{ "text": "..." }`.
- Committate spesso. Un solo link da consegnare: questa repo.

## Per la consegna
- Repo GitHub (questa) + un **video demo** di ~3 minuti che mostra l'app che funziona.
- Il deploy online di solito NON e obbligatorio: la demo in locale + video va benissimo.
