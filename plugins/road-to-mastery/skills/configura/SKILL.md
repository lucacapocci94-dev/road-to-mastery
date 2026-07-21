---
name: configura
description: (Ri)crea le configurazioni native di Claude che rendono la cartella-studente auto-configurante in cloud (app web, desktop e mobile) — .claude/settings.json con marketplace e plugin abilitato, hook di auto-merge sul branch di consolidamento e pin del branch. È lo stesso lavoro che /organizza fa in silenzio al Passo 5-bis, estratto in un comando a sé: usalo quando il programma è GIÀ stato creato ma le configurazioni mancano, sono state cancellate o vanno riparate, così i comandi del tutor ricompaiono da soli a ogni avvio di sessione.
---

# /configura — (Ri)crea le configurazioni cloud del tutor

Le sessioni cloud/mobile partono da una macchina **effimera** che riparte pulita
ogni volta. Quello che rende la cartella auto-configurante — cioè che fa
ricomparire da soli i comandi del tutor in **ogni** sessione web, desktop e
mobile — non vive nella macchina, ma **committato nel repo**, dentro `.claude/`.

`/organizza` scrive queste configurazioni da solo (al suo Passo 5-bis) la prima
volta o quando aggiungi una materia. `/configura` fa **solo** quella parte,
in un comando dedicato: usalo quando il programma **è già stato creato** ma le
configurazioni:

- **mancano** (cartella clonata o ripartita senza `.claude/`);
- sono state **cancellate o modificate** per errore;
- non funzionano e vuoi **ripararle**.

È **idempotente** e non tocca il tuo programma di studio: puoi darlo quante volte
vuoi senza rischi. Non fare mai domande tecniche allo studente: è tutto lavoro tuo.

---

## Passo 0 — Verifica che il programma esista già

Questo comando **completa** una cartella già allestita, non la crea. Controlla che
esista `stato/progressi.md` (segno che `/organizza` è già stato dato).

- **Non esiste** → non procedere con la configurazione a mano. Di' con parole
  semplici: "Qui non c'è ancora un programma di studio: partiamo con `/organizza`,
  che crea tutto **e** imposta anche queste configurazioni." Fermati qui.
- **Esiste** → prosegui.

---

## Passo 1 — Config nativa dei comandi (`.claude/settings.json`)

Assicura `.claude/settings.json` nella radice della cartella-studente.

- Se **non esiste**: copialo da
  `${CLAUDE_PLUGIN_ROOT}/templates/settings.json.template`.
- Se **esiste**: **fondi** le chiavi senza cancellare nulla di suo — deve contenere:
  - `extraKnownMarketplaces.road-to-mastery` → source `github`, repo
    `lucacapocci94-dev/road-to-mastery`;
  - `enabledPlugins["road-to-mastery@road-to-mastery"] = true`;
  - lo hook `Stop` che invoca `.claude/hooks/auto-merge-default.sh` (vedi Passo 2).

È così che i comandi del tutor compaiono da soli a ogni avvio di sessione web,
desktop e mobile: Claude Code installa e abilita il plugin dal marketplace
dichiarato qui, in modo nativo.

**Non** creare hook che invocano la CLI `claude` per installare: in cloud la CLI
non è nel PATH e sarebbe un no-op. Serve rete verso GitHub attiva nell'ambiente.

---

## Passo 2 — Hook di auto-merge sul branch di consolidamento

Copia `${CLAUDE_PLUGIN_ROOT}/templates/auto-merge-default.sh.template` in
`.claude/hooks/auto-merge-default.sh` e rendilo eseguibile (`chmod +x`).

A fine di ogni turno consolida il branch di lavoro in quello di consolidamento,
senza toccare il working tree e senza perdere lezioni.

---

## Passo 3 — Pin del branch di consolidamento

Rileva il branch dove far confluire tutto con `git remote show origin` (riga
`HEAD branch`); se fallisce, usa il branch corrente. Scrivi quel nome, da solo su
una riga, in `.claude/merge-target`.

Serve perché in questi ambienti `origin/HEAD` spesso non è impostato: pinnarlo
esplicitamente rende l'auto-merge stabile tra una sessione e l'altra. (Lo studente
può cambiarlo modificando quella singola riga.)

> Se `.claude/merge-target` esiste già e contiene un branch valido, **lascialo com'è**:
> potrebbe essere una scelta dello studente. Riscrivilo solo se manca o è vuoto.

---

## Passo 4 — Verifica e riepilogo

Controlla che i tre pezzi siano a posto e riferisci in italiano semplice, senza
gergo tecnico. Un riepilogo del tipo:

> "Fatto: ho reimpostato le configurazioni. Da ora, ogni volta che apri lo studio
> in una sessione nuova — dal web, dall'app desktop o dal telefono — i comandi del
> tutor ci saranno già e i tuoi progressi si salveranno da soli."

Se qualcosa non è stato possibile (per esempio non c'è rete verso GitHub, quindi
il plugin verrà installato al primo avvio con rete), dillo con parole semplici e
rassicura: i file di configurazione sono comunque scritti e committati, e faranno
effetto appena l'ambiente avrà rete.

---

📍 Adesso puoi:
- continuare a studiare con `/tutor`
- vedere tutti i comandi con `/help`
