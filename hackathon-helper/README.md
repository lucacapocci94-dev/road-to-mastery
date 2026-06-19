# hackathon-helper

Un piccolo plugin per **Claude Code** che fa da "regia" durante un hackathon a coppie (stile *Built with Opus* di Anthropic): partire in fretta, non perdere tempo nel setup, e arrivare alla demo con qualcosa che gira.

NON rifa cio che Claude Code e le skill di Pocock gia fanno (brainstorming, PRD, issue, TDD). Aggiunge solo lo strato che manca: la disciplina della giornata a tempo fisso.

## Skill incluse

| Skill | A cosa serve |
|-------|--------------|
| `setup-team-repo` | In un comando: crea la repo GitHub del team (una repo, cartelle `frontend/` e `backend/` con scheletro gia funzionante e Claude cablato), aggiunge il compagno come collaboratore, primo push. |

> Roadmap (prossimi mattoni): `il-via` (intervista + piano time-boxed), `checkpoint` (ricalibra e taglia), `congelamento` (repo + README + video demo 3 min).

## Filosofia

- **Tempo fisso, scope variabile.** Parti dall'orologio, taglia le feature per starci dentro.
- **Scheletro che cammina subito**, demo-freeze alla fine.
- **Niente roba pesante** (CI/CD, GitHub Actions, issue tracker complessi): in 5-6 ore non servono.
