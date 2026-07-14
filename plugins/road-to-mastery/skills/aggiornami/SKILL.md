---
name: aggiornami
description: Controlla se sul marketplace c'è una versione più recente del plugin road-to-mastery e ti guida all'aggiornamento, mostrandoti cosa è cambiato. Aggiorna il MOTORE del tutor (i comandi, gli hook), non il tuo programma di studio — per quello ci sono /rinnova e /infittisci. È un aiuto amichevole sopra al comando nativo di Claude Code /plugin update.
---

# /aggiornami — Aggiorna il plugin all'ultima versione

Il motore del tutor (comandi e hook) vive nel plugin `road-to-mastery`, che si
installa dal marketplace. Ogni tanto esce una versione nuova con comandi o
migliorie. `/aggiornami` controlla se ce n'è una e ti accompagna ad installarla,
dicendoti **cosa cambia**.

> Da non confondere: `/aggiornami` aggiorna **il motore** (il plugin). Per
> aggiornare **il tuo programma di studio** quando la materia cambia usa
> `/rinnova`; per renderlo più denso, `/infittisci`.

## Passo 1 — Controlla se c'è una versione nuova
Esegui il controllo (non tocca niente, legge soltanto):
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_aggiornamenti.py
```
Lo script confronta la versione installata con quella pubblicata sul marketplace
e, se c'è un aggiornamento, stampa le **novità** dal changelog.

## Passo 2 — Racconta l'esito, in italiano semplice
- **Già aggiornato** → rassicura: "Sei già all'ultima versione (X), non devi fare
  niente." Fine.
- **Aggiornamento disponibile** → di' qual è la versione nuova e riporta le novità
  che lo script ha stampato, con parole tue e concrete ("da adesso c'è il comando
  …", "…").
- **Controllo non riuscito** (nessuna rete) → spiega che non sei riuscito a
  verificare adesso e che può riprovare più tardi. Non bloccare nulla.

## Passo 3 — Guidalo all'aggiornamento (il comando nativo lo esegue lui)
L'installazione vera la fa un **comando nativo di Claude Code**, che io non posso
lanciare al posto tuo. Quindi, se c'è una versione nuova, digli di scrivere questi
due comandi, in quest'ordine:
```
/plugin marketplace update road-to-mastery   ← rinfresca il catalogo
/plugin update road-to-mastery               ← installa l'ultima versione
```
Poi basta riaprire la sessione: gli hook ricaricano lo stato e i comandi nuovi
sono subito disponibili. I progressi di studio **non si toccano**: vivono nei tuoi
file, non nel plugin.

## Passo 4 — Chiudi
Se ha aggiornato, invitalo a dare un `/help` per vedere eventuali comandi nuovi.
Nessuna scrittura di stato è necessaria: questo comando non modifica il tuo
percorso di studio.
