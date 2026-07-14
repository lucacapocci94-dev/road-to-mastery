---
name: aggiornami
description: Aggiorna il plugin road-to-mastery all'ultima versione. Rinfresca il marketplace, confronta la versione in uso con quella disponibile e, se ce n'è una nuova, la installa e ti dice cosa è cambiato. Aggiorna il MOTORE del tutor (i comandi, gli hook), non il tuo programma di studio — per quello ci sono /rinnova e /infittisci.
---

# /aggiornami — Aggiorna il plugin all'ultima versione

Il motore del tutor (comandi e hook) vive nel plugin `road-to-mastery`. Ogni tanto
esce una versione nuova. `/aggiornami` fa tutto il giro: **rinfresca il
marketplace**, controlla se c'è una versione più recente e — se c'è — la
**installa** e ti dice cosa cambia.

> Da non confondere: `/aggiornami` aggiorna **il motore**. Per aggiornare **il tuo
> programma di studio** quando la materia cambia usa `/rinnova`; per renderlo più
> denso, `/infittisci`.

## Passo 1 — Rinfresca il marketplace e controlla
Esegui il controllo. **Rinfresca da solo il marketplace** (così la cache ha
davvero l'ultima versione) e poi confronta la versione **in uso** con quella
**disponibile**:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/controlla_aggiornamenti.py
```

## Passo 2 — Racconta l'esito, in italiano semplice
- **Già aggiornato** → "Sei già all'ultima versione (X), non c'è niente da fare." Fine.
- **Aggiornamento disponibile** → di' qual è la versione nuova e riporta le novità
  che lo script ha stampato, con parole tue e concrete.
- **Controllo non riuscito** (nessuna rete) → spiega e invita a riprovare più tardi.

## Passo 3 — Installa l'aggiornamento (se disponibile)
Se c'è una versione nuova, **installala tu** con il comando nativo:
```
claude plugin update road-to-mastery@road-to-mastery
```
- Se va a buon fine, avvisa che **l'aggiornamento si applica alla riapertura**:
  "Ho scaricato la versione X: **chiudi e riapri la sessione** e sarà attiva."
- Se quel comando non è disponibile nella sua build o dà errore, guidalo al menu:
  "Scrivi `/plugin`, vai su **Installed** → **road-to-mastery** → **Update**."

Non serve toccare nulla del percorso di studio: i progressi vivono nei file dello
studente, non nel plugin, e restano intatti.

## Passo 4 — Chiudi
Dopo la riapertura, invitalo a dare un `/help` per vedere eventuali comandi nuovi.
