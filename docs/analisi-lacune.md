# Analisi delle lacune — verso il tutor più performante

**Data:** 2026-06-27
**Scopo:** capire cosa manca a `road-to-mastery` per essere, come plugin, il
miglior tutor possibile a livello di **skill**, **hook** e **prompt/obiettivi**,
e per chi lo usa senza preoccuparsi di git/PR né di tenere traccia a mano.

---

## 1. Da dove parte il motore (sintesi onesta)

Il motore attuale è solido e ha una colonna vertebrale chiara:

- **Contratto del file system** (`stato/` globale + `materie/<slug>/`), una sola
  fonte di verità, multi-materia senza contaminazione.
- **3 hook** (SessionStart carica+riconcilia, Stop checkpoint, SessionEnd
  chiusura): la persistenza è deterministica e indipendente da git.
- **12 skill** orientate a un modello preciso: **esame + syllabus + copertura**.
  `/organizza` scorpora un programma denso, `/tutor` insegna, `/testa`,
  `/interrogazione`, `/simulazione` verificano, `/infittisci`/`/raddrizza`
  approfondiscono, `/carico`/`/avanzamento`/`/programma` governano il piano.

È un eccellente **preparatore d'esame per copertura**. I buchi non sono difetti:
sono le cose che un *tutor da zero, orientato all'obiettivo* fa e che qui mancano.

---

## 2. Buchi a livello di OBIETTIVI (i più importanti)

Il motore ottimizza la **copertura di un syllabus** (% di lezioni fatte). Ma il
vero obiettivo dello studente quasi mai è "coprire il syllabus": è **saper fare
qualcosa, a un certo livello, entro una scadenza**.

1. **L'obiettivo reale non è un cittadino di prima classe.** Esiste solo
   `livello-obiettivo` (base/approfondito/padronanza) + data d'esame. Manca il
   *risultato specifico* ("saper risolvere un tema di diritto in 60 min",
   "passare lo scritto di X") e il **criterio di riuscita** misurabile. → nuova
   skill **`/obiettivo`** (prompt *Learning Path Architect*).
2. **Manca la pianificazione a ritroso (backward design).** Si parte dal
   syllabus in avanti; non dall'obiettivo che si scompone in compiti giornalieri
   con criterio di successo e "cosa NON fare per non sprecare tempo".
3. **Manca l'80/20 spietato.** Tutto è orientato all'esaustività. Non c'è una
   modalità "rendimi operativo in fretta": cosa imparare per primo, cosa
   ignorare, l'unico esercizio che mi mette già davanti alla maggioranza. →
   nuova skill **`/operativo`** (prompt *Learning Curve Destroyer*).

---

## 3. Buchi a livello di SKILL (metodo di apprendimento)

Le verifiche esistenti (`/testa`, `/interrogazione`, `/simulazione`) sono tutte
**Q&A sul già studiato**. Mancano i metodi di apprendimento profondo che rendono
un tutor *bravo davvero*:

1. **Pratica deliberata sull'errore.** Imparare facendo e sbagliando in
   situazioni realistiche, con l'AI che non dà la risposta ma incalza finché non
   trovi tu dove si rompe il ragionamento. → **`/palestra`** (*Real Error
   Simulator*).
2. **Decodifica di materiale ostico.** Prendere un contenuto che confonde
   (dispensa, normativa, paper), trovare l'**unica idea-chiave** che fa andare il
   resto a posto, spiegarla con un'analogia quotidiana, poi 3 domande-cancello.
   È il "grill me with docs": incolli un documento e ti fai interrogare su quello.
   → **`/decifra`** (*Impossible Language Translator*).
3. **Rilevamento delle lacune nascoste.** Quando credi di padroneggiare già un
   tema: 5 domande che sembrano semplici ma espongono i buchi di chi non è mai
   andato in profondità, senza sconti. Diverso da `/testa` (che certifica per
   *saltare*): qui si **smonta l'eccesso di sicurezza**. → **`/lacune`**
   (*Hidden Gap Detector*).
4. **Feynman forzato.** Tu spieghi come a un bambino di 10 anni, l'AI ti ferma a
   ogni termine non definito, salto logico o semplificazione errata, e alla fine
   ti dice cosa quegli inciampi rivelano. Oggi il teach-back è solo un *passo*
   dentro `/tutor`; qui diventa uno strumento rigoroso a sé. → **`/spiegamelo`**
   (*Forced Feynman Method*).

Queste 5 + `/obiettivo` sono i 6 prompt esplosi in skill vere, generiche,
applicabili a **qualsiasi materia o esame, da zero o da un certo livello**.

---

## 4. Buchi a livello di HOOK e TRACCIABILITÀ

Obiettivo dichiarato: lo studente non deve mai fare bookkeeping a mano, né
rispondere a domande tecniche, né preoccuparsi di git/PR. Cosa manca:

1. **Nessun diario leggibile da umano.** La storia "dove sono arrivato" vive solo
   in `progressi.md` (stato, non racconto) e nella history git (illeggibile per
   un non tecnico, e assente per chi non usa git). → introdotto **`stato/diario.md`**:
   registro in italiano semplice, una riga per tappa, aggiornato dal motore in
   automatico, **mostrato all'avvio dall'hook** ("Bentornato, l'ultima volta…").
2. **L'avvio non racconta il percorso, mostra solo lo stato.** Il SessionStart
   inietta `progressi.md` ma non le ultime tappe né l'obiettivo in evidenza. →
   l'hook ora **inietta anche le ultime voci del diario e l'obiettivo attivo**.
3. **Il salvataggio è invisibile.** Lo studente non sa che tutto si salva da
   solo. → l'hook di avvio ora segnala in chiaro l'ultimo salvataggio (da
   `.road-to-mastery.log`, per chi usa git) e ricorda che i file locali sono già
   la verità anche senza git.
4. **La riconciliazione di una sessione morta dipende dal modello.** Resta vero
   (un hook di shell non può scrivere contenuti al posto del modello), ma il
   messaggio di avvio è stato reso più imperativo e prioritario.

> Principio che regge le scelte: **l'hook garantisce la persistenza**; il
> **diario** garantisce la *trasparenza* leggibile; le **skill** garantiscono la
> *qualità*. Nessuno dei tre finge di fare il lavoro di un altro.

---

## 5. Niente git, niente PR: come la tracciabilità resta garantita

Per lo studente tipico (locale, senza git) la verità sono **i file su disco** +
**`diario.md`**. Git è solo copia di sicurezza tra dispositivi e, se manca, gli
hook fanno no-op pulito. Per questo la tracciabilità leggibile non è affidata a
git ma al diario, che esiste e si aggiorna **anche senza alcun repo**. Mai si
parla di PR/merge allo studente: è fuori dal suo mondo, per disegno.

---

## 6. Le nuove skill in una riga (i 6 prompt esplosi)

| Skill | Prompt sorgente | A cosa serve |
|---|---|---|
| `/operativo` | The Learning Curve Destroyer | 80/20 spietato: cosa prima, cosa ignorare, l'esercizio che ti mette avanti |
| `/palestra` | The Real Error Simulator | impari sbagliando in situazioni reali; l'AI incalza, non regala risposte |
| `/decifra` | The Impossible Language Translator | decodifica un contenuto ostico: idea-chiave + analogia + 3 domande-cancello |
| `/obiettivo` | The Personal Learning Path Architect | percorso a ritroso da risultato+scadenza: compiti da 45 min, criterio, cosa NON fare |
| `/lacune` | The Hidden Gap Detector | 5 domande che smontano l'eccesso di sicurezza ed espongono i buchi |
| `/spiegamelo` | The Forced Feynman Method | spieghi tu; l'AI ti ferma su termini, salti e semplificazioni sbagliate |

Più **`/diario`**: la linea del tempo leggibile di tutto il percorso.
