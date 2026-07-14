---
name: condividi
description: Crea un pacchetto AUTONOMO di uno o più programmi di studio da dare a qualcun altro che parte da zero. NON tocca la tua cartella né i tuoi progressi (la tua roba resta intatta) — ne fa solo una COPIA pulita. Nella copia mette solo le materie che scegli (non tutte), azzera i progressi (ogni lezione torna "da fare") e toglie i dati personali, e include il motore-tutor col suo hook, così a chi riceve funzionano subito tutti i comandi senza installare niente. Produce un file .zip pronto da inviare.
---

# /condividi — Impacchetta un programma da regalare a qualcuno

Vuoi passare un programma a un'altra persona che deve fare lo stesso corso, senza
i tuoi progressi e senza le altre materie. `/condividi` prepara un **pacchetto
autonomo** in `.zip`.

> ## ⚠️ Regola d'oro: la TUA cartella non si tocca
> Questo comando **non modifica mai nulla** della tua cartella di studio: non
> azzera i tuoi progressi, non svuota le tue sessioni, non cambia la materia
> attiva, non consolida niente. La tua memoria resta **esattamente com'è**.
> L'azzeramento dei progressi avviene **solo dentro la copia** che finisce nello
> zip. Tutto ciò che scrivi va in una **cartella temporanea separata**, mai dentro
> la tua.

> **Come fa a funzionare senza installare niente.** Nella copia va anche il motore
> (il plugin), incluso come *marketplace locale*, con un hook che al primo avvio
> lo installa da solo. Così a chi riceve `/tutor`, `/programma`… funzionano subito,
> anche offline. I comandi sono generici: lavorano su qualsiasi cartella di studio.

## Fase 1 — Quali materie (esattamente quelle che dici tu)
- `/condividi <materia>` → **quella** materia, e solo quella. Non usare la materia
  attiva al suo posto: se l'argomento è esplicito, si condivide quello.
- `/condividi <m1> <m2>` → più materie.
- `/condividi` senza argomento → mostra le materie presenti (le cartelle in
  `materie/`) e **chiedi quale/i**. **Mai** impacchettare tutto in automatico.

Leggi soltanto (non scrivere) i file della materia scelta per assemblare la copia.

## Fase 2 — Costruisci il pacchetto in una cartella TEMPORANEA separata
Scegli una cartella di lavoro **fuori dalla tua cartella di studio** (sotto la
cartella di sistema per i file temporanei), vuota, con un nome parlante, es.
`<slug>-da-studiare/`. Poi lancia il preparatore: legge la tua cartella (sola
lettura), copia **solo** le materie scelte nella temporanea, **azzera gli stati
delle lezioni nella copia**, rigenera uno `stato/` pulito e **include il motore**.
```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/prepara_condivisione.py . <cartella-tmp> <slug1> [slug2...]
```
Il preparatore si rifiuta di scrivere se la destinazione coincide con la tua
cartella o ci sta dentro: è una rete di sicurezza contro la perdita dei tuoi dati.

## Fase 3 — CLAUDE.md neutro (senza i tuoi dati) — solo nella copia
Compila il template del plugin
(`${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md.template`) e salvalo come `CLAUDE.md`
**nella cartella-tmp**:
- `{{ESAME}}` → l'esame/corso (si tiene);
- `{{NOME}}` → segnaposto neutro, es. "(il tuo nome)";
- `{{DATA_ESAME}}` → `(da impostare)`.

## Fase 4 — LEGGIMI per chi riceve — nella copia
Scrivi un `LEGGIMI.md` breve nella cartella-tmp, in italiano semplice:
```
# Il tuo tutor per [ESAME] — pronto all'uso

Questa cartella è un tutor personale per preparare [ESAME] ([materie]).
I progressi partono da zero: da qui in avanti è tutto tuo.

## Come iniziare
1. Apri questa cartella con Claude Code.
2. La prima volta il motore si installa da solo: se ti viene chiesto, riapri la
   sessione. (Non serve internet: è già tutto incluso.)
3. Poi: `/programma` (vedi il programma) · `/tutor` (studia) · `/help` (tutti i comandi).

I progressi si salvano da soli: non devi sapere niente di file o di git.
```
Adatta `[ESAME]` e `[materie]` ai valori reali.

## Fase 5 — Crea lo .zip
Comprimi la cartella-tmp in un unico file nella cartella corrente
(`<slug>-da-studiare.zip`), poi **rimuovi la cartella-tmp** (era solo di lavoro).

## Fase 6 — Consegna
Di' allo studente, concretamente: **dove** è lo zip, **cosa contiene** (le materie
scelte, progressi azzerati **nella copia**, nessun tuo dato, motore incluso), e
che la **tua** cartella è rimasta intatta. Per chi lo riceve: "scompatta, apri con
Claude Code e segui il LEGGIMI: i comandi ci sono già".

📍 Adesso puoi:
- condividere un'altra materia con `/condividi <altra-materia>`
- continuare a studiare con `/tutor` (i tuoi progressi sono intatti)
