---
name: help
description: Guida completa e auto-esplicativa di tutti i comandi del tutor Road to Mastery, in italiano semplice e organizzata per categorie, con cosa fa ogni comando, quando usarlo e un esempio. Include la mappa del file system e il modello di lezione.
---

# /help — Guida ai comandi

Quando invocata, mostra la guida completa in italiano semplice. Personalizza il
nome se disponibile in `CLAUDE.md` / `stato/progressi.md`.

## Output da mostrare

---

**Ecco tutto quello che puoi fare:**

> 💡 **Come si scrivono i comandi.** Essendo un plugin, ogni comando porta davanti
> il nome `road-to-mastery`. Forma completa: `/road-to-mastery:organizza`,
> `/road-to-mastery:tutor`, e così via. In pratica ti basta digitare `/` e l'inizio
> del nome (es. `/organ…`) e **scegliere dal menu** la versione completa. In più
> puoi semplicemente dirmi a parole cosa vuoi (es. "ho una nuova materia da
> preparare") e faccio partire io il comando giusto. Sotto li scrivo in forma corta
> per leggerli meglio.

### 🚀 Configura il tuo studio
- `/organizza` — prepara la cartella per un esame: crea programma e file di stato,
  e aggiunge una nuova materia
  *Usalo la prima volta, o quando vuoi aggiungere una materia*

### 📚 Consulta il programma
- `/programma` — vedi tutto il programma con moduli e lezioni
- `/programma moduli` — solo i moduli, visione veloce
- `/programma 3` — solo le lezioni del Modulo 3

### 🧱 Approfondisci il programma
- `/infittisci` — rende il programma più denso e profondo (più lezioni, stessa
  durata), facendo lavorare uno specialista per ogni sezione
- `/infittisci 3` — approfondisce solo il Modulo 3
  *Usa i livelli: base → approfondimento → padronanza*

### 📊 Quanto studiare al giorno
- `/carico` — quante lezioni e minuti al giorno servono per arrivare pronto, con
  semaforo di fattibilità rispetto alla data

### 📈 I tuoi progressi
- `/avanzamento` — percentuali per materia, ripassi dovuti, copertura del syllabus
- `/avanzamento 1` — dettaglio del Modulo 1 (o qualsiasi numero)

### 🎯 Testa quello che già sai
- `/testa 3` — verifica le tue conoscenze sul Modulo 3
  *Se vai bene, le lezioni vengono certificate — risparmi tempo prezioso*

### 🔄 Modalità di studio
- `/modalita` — vedi quale modalità è attiva
- `/modalita micro` — lezioni da 5-10 minuti ← **attiva per default**
- `/modalita standard` — lezioni complete da 30-90 minuti

### 📖 Studia
- `/tutor` — continua dalla lezione dove hai lasciato
- `/tutor 3.2a` — vai direttamente a una lezione specifica
- `/tutor <materia>` — studia un'altra materia
- `/raddrizza` — se va troppo veloce o troppo in superficie, ferma e approfondisci
  il punto dove sei (anche "più esteso" o "non ho capito" funzionano)

### ✏️ Mettiti alla prova
- `/interrogazione` — domande su quello che hai già studiato (severa ma giusta)
- `/simulazione` — simulazione dell'esame vero, su tutto il programma

---

**Come è organizzato lo studio (mappa):**
- `stato/` — i tuoi progressi e le tue preferenze (validi per tutte le materie)
- `materie/<materia>/` — programma, domande e sessioni di ogni singola materia

**Come funziona una lezione:** spiegazione interattiva durante la sessione +
verifica differita (ripasso dilazionato) all'inizio della sessione successiva.
Tutto si salva da solo: non devi pensarci.

Per rivedere questa guida in qualsiasi momento: scrivi `/help`.
