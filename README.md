# Tidya Design Guide

Designspråket for Tidya: farger, typografi, komponenter og tokens, med mørk og lys modus. Et varmt grensesnitt bygget på amber og brune toner.

Guiden er en statisk side uten byggesteg. Åpne `index.html` i nettleseren, eller bruk `tokens.css` direkte i egne prosjekter.

## Innhold

| Fil | Formål |
|---|---|
| `index.html` | Visuell guide: farger, typografi, komponenter, kanter, radius, bevegelse og token-tabell |
| `tokens.css` | Kilden til sannhet: CSS-variabler for begge moduser, `@font-face` og radius/overgangstokens |
| `styles.css` | Stiler for selve guiden og komponent-eksemplene |
| `theme.js` | Bryter for mørk/lys modus (følger OS, kan overstyres og huskes) |
| `fonts/` | Selvhostede Inter og Fraunces (woff2, SIL OFL 1.1) |

## Publisering

Guiden publiseres til GitHub Pages av `.github/workflows/pages.yml` ved hver push til `main`. Krever at Settings → Pages → Source er satt til **GitHub Actions**.

## Bruk

```html
<link rel="stylesheet" href="tokens.css">
```

```css
.button {
	background: var(--color-accent-fill);
	color: var(--color-on-accent);
}
```

Mørk modus er standard. Lys modus aktiveres av OS-innstillingen (`prefers-color-scheme: light`), eller eksplisitt med `data-theme="light"` / `data-theme="dark"` på `<html>`.

## Prinsipper

- **Tekstkontrast:** all tekst har minst 4,5:1 mot `--color-bg` og `--color-surface` (WCAG AA).
- **Kontroller:** kanter som markerer UI-elementer (input, ghost-knapp, drop-soner) har minst 3:1. Bruk `--color-border-control` og `--color-accent-border`. De dekorative `--color-border*` er kun for skiller.
- **Aksent har to roller:** `--color-accent` til tekst, lenker og fokusring (mørk brun i lys modus), `--color-accent-fill` til flater som knapper, alltid `#ffbe0b` med `--color-on-accent` som tekst.
- **Fonter:** Fraunces til display og overskrifter, Inter til brødtekst og UI. Selvhostet, ingen Google Fonts og ingen tredjepartsforespørsler.

## Endre tokens

1. Endre verdiene i `tokens.css` (mørk, `prefers-color-scheme: light` og `data-theme="light"` må holdes i takt).
2. Sjekk kontrasten på nytt: tekst 4,5:1, kontroller 3:1.
3. Oppdater `index.html` slik at swatches og token-tabellen stemmer.

## Lisens

Fontene er lisensiert under SIL Open Font License 1.1, se `fonts/LICENSE-*.txt`.
