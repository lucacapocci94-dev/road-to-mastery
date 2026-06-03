# Road to Mastery — Piano 2: Migrazione delle skill (nucleo v1)

**Data:** 2026-06-03
**Stato:** nucleo v1 COMPLETO.

## Obiettivo

Costruire, dentro `plugins/road-to-mastery/skills/`, le skill del motore rese
**generiche** (non più cucite su una sola candidata) e **materia-aware**
(agganciate al contratto del file system multi-materia del design §3).

## Cosa è stato fatto

9 skill del nucleo v1 (design §11), ognuna in `skills/<nome>/SKILL.md` con
frontmatter `name` + `description` ricca (alimenta l'autocompletamento dello slash):

| Skill | Origine | Note di generalizzazione |
|---|---|---|
| `organizza` | **nuova** | bootstrap completo: intervista non tecnica, struttura del contratto, programmi con controllo di copertura, compilazione del `CLAUDE.md` dal template |
| `tutor` | `commands/tutor.md` | materia-aware; percorsi `materie/<materia>/...`; teach-back + auto-verifica di copertura |
| `testa` | `commands/testa.md` | niente più 9 moduli fissi: i moduli si leggono dal `programma-micro.md` della materia |
| `interrogazione` | `commands/interrogazione.md` | priorità ai punti deboli; per-materia |
| `simulazione` | `commands/simulazione.md` | simulazioni salvate in `materie/<materia>/simulazioni/` |
| `modalita` | `commands/modalita.md` | preferenza globale micro/standard in `stato/progressi.md` |
| `programma` | `commands/programma.md` | per-materia; giorni alla prova da data esame generica |
| `avanzamento` | `commands/avanzamento.md` | multi-materia + invariante di copertura (syllabus non coperto) + ripassi dovuti |
| `help` | `commands/help.md` | generico: niente riferimenti a Mariele/integrazioni; include `/organizza` |

### Decisioni sui punti aperti (design §13 / handoff §6)
1. **Slug** plugin e repo: confermato `road-to-mastery` per entrambi.
2. **`sincronizzazione.md`**: resta **per-materia** (come da design §3).
3. **Calendario ripassi**: ripasso dilazionato a **1, 3, 7, 16, 35 giorni** dopo
   la prima padronanza di ogni lezione, registrato in `stato/progressi.md`.

### Requisiti trasversali rispettati (design §3, §6, §8, §9)
- Lettura/scrittura **solo** dentro il contratto del file system.
- **Risoluzione materia** in ogni skill: argomento esplicito → materia attiva →
  altrimenti chiedi. Mai indovinare.
- **Salva all'ingresso** (gate) prima di ogni comando.
- **Ricerca web obbligatoria** prima di generare contenuti didattici/normativi.
- **Italiano sempre**, salvataggio silenzioso, nessuna domanda tecnica.
- `tools/valida_contratto.py` come guardia di coerenza (usata da `/organizza`).

## Verifiche

- `claude plugin validate .` → marketplace OK.
- `claude plugin validate plugins/road-to-mastery` → plugin OK.
- `python3 -m pytest` → 17/17 verdi (gli hook/validatore non sono toccati).
- Frontmatter YAML di tutte le 9 skill ben formato (`name` + `description`).

## Cosa resta (fasi successive)

Skill da migrare più avanti (design §11, non in v1):
`dossier`, `anteprima`, `traccia`, `inglese`, `commissaria`, `integrazioni`,
`statistiche`, `perfeziona`, `powerpoint`, `progettazione`, `scaletta`,
`nuova-lezione`.

Altro:
- Migrazione effettiva dei contenuti di Mariele al layout multi-materia (passo
  dedicato, con verifica).
- Pubblicazione del marketplace su GitHub.
- Eventuale prova end-to-end di `/organizza` su una cartella vuota reale.
