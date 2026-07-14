---
name: condividi
description: Crea un pacchetto AUTONOMO di uno o più programmi di studio, pronto da dare a qualcun altro che parte da zero. Copia solo le materie che scegli (non tutte), azzera i tuoi progressi (ogni lezione torna "da fare"), toglie i tuoi dati personali (percentuali, punti deboli, diario, sessioni, domande) e include il motore-tutor col suo hook, così a chi lo riceve funzionano subito tutti i comandi (tutor, programma, ecc.) senza installare niente. Produce un file .zip pronto da inviare.
---

# /condividi — Impacchetta un programma da regalare a qualcuno

Hai costruito un programma e vuoi passarlo a un'altra persona che deve fare lo
stesso corso, **senza i tuoi progressi** e senza le altre materie. `/condividi`
prepara un **pacchetto autonomo** in `.zip`: chi lo riceve apre la cartella e ha
già tutto — programma pulito **e** tutti i comandi funzionanti.

> **Come fa a funzionare senza installare niente.** Nel pacchetto va **anche il
> motore** (il plugin), incluso come *marketplace locale*, con un hook che al
> primo avvio lo installa da solo. Così `/tutor`, `/programma`, `/interrogazione`…
> sono subito disponibili su quel programma, anche offline. I comandi sono
> generici: lavorano su qualsiasi cartella di studio, quindi funzionano sul
> programma condiviso esattamente come sul tuo.

## Fase 0 — Salva all'ingresso
Se `materie/<materia-attiva>/sessione_corrente.md` non è vuoto, consolidalo in
`stato/progressi.md` e svuotalo prima di procedere.

## Fase 1 — Quali materie
- `/condividi <materia>` → quella materia · `/condividi <m1> <m2>` → più materie.
- `/condividi` senza argomento → mostra le materie presenti (le cartelle in
  `materie/`) e **chiedi quale/i** condividere. **Mai** impacchettare tutto in
  automatico: si condivide solo ciò che sceglie.

## Fase 2 — Costruisci il pacchetto autonomo
Scegli una cartella di lavoro temporanea, fuori dalla vista (sotto la cartella di
sistema per i file temporanei), con un nome parlante, es. `<slug>-da-studiare/`.
Poi lancia il preparatore: copia solo le materie scelte, **azzera gli stati delle
lezioni**, rigenera `stato/` pulito e **include il motore** (marketplace locale +
hook di auto-installazione + settings):
```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/prepara_condivisione.py . <cartella-tmp> <slug1> [slug2...]
```

## Fase 3 — CLAUDE.md neutro (senza i tuoi dati)
Compila il template del plugin
(`${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md.template`) e salvalo come `CLAUDE.md`
nella cartella-tmp, **senza dati personali tuoi**:
- `{{ESAME}}` → l'esame/corso (è del corso, si tiene);
- `{{NOME}}` → segnaposto neutro, es. "(il tuo nome)";
- `{{DATA_ESAME}}` → `(da impostare)`.

## Fase 4 — LEGGIMI per chi riceve
Scrivi un `LEGGIMI.md` breve e caloroso nella cartella-tmp, in italiano semplice.
Visto che il motore si installa da solo, le istruzioni sono minime:
```
# Il tuo tutor per [ESAME] — pronto all'uso

Questa cartella è un tutor personale per preparare [ESAME] ([materie]).
I progressi partono da zero: da qui in avanti è tutto tuo.

## Come iniziare
1. Apri questa cartella con Claude Code.
2. La prima volta il motore si installa da solo: se ti viene chiesto, riapri la
   sessione. (Non serve internet: è già tutto incluso.)
3. Poi:
   - `/programma` — vedi il programma
   - `/tutor` — inizia a studiare
   - `/help` — tutti i comandi

Non devi sapere niente di file o di git: i progressi si salvano da soli.
```
Adatta `[ESAME]` e `[materie]` ai valori reali.

## Fase 5 — Crea lo .zip
Comprimi la cartella-tmp in un unico file nella cartella corrente, con un nome
parlante (`<slug>-da-studiare.zip`), poi **rimuovi la cartella-tmp**.

## Fase 6 — Consegna
Di' allo studente, concretamente:
- **dove** si trova lo zip (nome del file, cartella corrente);
- **cosa contiene** (le materie scelte, progressi azzerati, nessun tuo dato, motore incluso);
- **cosa dire** a chi lo riceve: "scompatta, apri la cartella con Claude Code e
  segui il LEGGIMI: i comandi ci sono già".

📍 Adesso puoi:
- condividere un'altra materia con `/condividi <altra-materia>`
- continuare a studiare con `/tutor`
