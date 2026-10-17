# Tidya Design Guide

Designspråket for Tidya: tokens, komponenter og regler, med mørk og lys modus. Et varmt grensesnitt bygget på amber og brune toner. Statisk, uten byggesteg.

**Live:** https://tidya-no.github.io/tidya-design-guide/

## Filer

| Fil | Formål |
|---|---|
| `tokens.css` | Kilden til sannhet: farger (mørk og lys), typografi, avstand, radius, overganger, `@font-face` |
| `components.css` | Komponenter som ren CSS: knapper, skjema, tabell, kort, melding, dialog, htmx-tilstander |
| `DESIGN.md` | Regler for utviklere og AI: token til bruk, komponenter, htmx-mønstre, norsk UI-tekst |
| `AGENTS.md` | For deg som endrer repoet: hva som må holdes i takt og QA før PR |
| `index.html`, `styles.css`, `theme.js` | Den visuelle guiden |
| `fonts/` | Selvhostede Inter og Fraunces (woff2, SIL OFL 1.1) |

## Bruk

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
```

Mørk modus er standard. Lys modus følger OS (`prefers-color-scheme: light`) eller settes med `data-theme="light"` / `"dark"` på `<html>`. Reglene står i `DESIGN.md`.

## Endre tokens

1. Endre verdiene i `tokens.css`. Lys modus er definert to steder (`prefers-color-scheme` og `data-theme="light"`) som må holdes i takt.
2. Sjekk kontrasten på nytt: tekst 4,5:1, kontroller 3:1.
3. Oppdater fargetabellen i `index.html`.

## Publisering

`.github/workflows/pages.yml` publiserer til GitHub Pages ved push til `main`. Krever Settings → Pages → Source: **GitHub Actions**.

`.github/workflows/kvalitet.yml` kjører en statisk konsistenssjekk (`statisk.py`), html-validate og axe (mørk/lys, 320/1100 px, med dialog) på alle PR-er, og før hver publisering. Config og script ligger i `.github/qa/`.

## Lisens

Fontene er lisensiert under SIL Open Font License 1.1, se `fonts/LICENSE-*.txt`.
