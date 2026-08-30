# Installare il marketplace Road to Mastery su un altro Claude

Istruzioni pronte da consegnare a un'altra sessione di Claude Code per scaricare
il marketplace **road-to-mastery** e avere tutti i comandi del tutor subito
disponibili.

---

## 📋 Versione rapida (due comandi)

Da incollare all'altro Claude:

> Installa e attiva il marketplace **road-to-mastery** su Claude Code. Esegui
> questi due comandi:
>
> ```
> /plugin marketplace add lucacapocci94-dev/road-to-mastery
> /plugin install road-to-mastery@road-to-mastery
> ```
>
> Dopo l'installazione i comandi del tutor sono disponibili in forma "namespata",
> cioè col prefisso del plugin: `/road-to-mastery:organizza`,
> `/road-to-mastery:tutor`, `/road-to-mastery:help`, ecc. Per vedere tutto quello
> che sa fare, lancia `/road-to-mastery:help`.

L'installazione va fatta **una volta sola** e resta attiva anche nelle sessioni
successive.

---

## ⚙️ Versione definitiva — comandi pronti a OGNI avvio di sessione

Se vuoi la **garanzia** che marketplace + plugin siano attivi in automatico
all'apertura di *qualsiasi* nuova sessione (senza ridigitare nulla), crea questo
file nel progetto:

**`.claude/settings.json`**

```json
{
  "extraKnownMarketplaces": {
    "road-to-mastery": {
      "source": {
        "source": "github",
        "repo": "lucacapocci94-dev/road-to-mastery"
      }
    }
  },
  "enabledPlugins": {
    "road-to-mastery@road-to-mastery": true
  }
}
```

Con questo file presente, Claude Code all'avvio conosce già il marketplace e
**abilita il plugin da solo**: tutti i comandi sono subito disponibili senza
passaggi manuali.

---

## Note utili

- **Nome doppio non è un errore:** `road-to-mastery@road-to-mastery` significa
  *plugin `road-to-mastery`* preso dal *marketplace `road-to-mastery`*.
- **Come si digitano i comandi:** basta scrivere `/` e l'inizio del nome
  (es. `/organ…`) e scegliere dal menu la voce completa
  `/road-to-mastery:organizza`.
- **Primo comando consigliato:** `/road-to-mastery:organizza` per configurare la
  cartella di studio, oppure `/road-to-mastery:help` per la guida completa in
  italiano.
- **Aggiornamenti futuri:** `/plugin update`.
