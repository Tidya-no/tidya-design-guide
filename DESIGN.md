# Tidya designsystem: regler for utvikling

Kort referanse for deg som bygger UI (menneske eller AI). Verdier: `tokens.css`. Komponenter: `components.css`. Eksempler: `index.html` ([live](https://tidya-no.github.io/tidya-design-guide/)). Bygget for server-rendret HTML med htmx (komponentene er ren CSS og fungerer også i React).

## Regler

1. Bruk alltid tokens (`var(--color-*)`, `--space-*`, `--r-*`, `--text-*`). Aldri hardkodede farger, avstander, radius eller font-størrelser.
2. Mørk modus er standard. Lys modus følger OS (`prefers-color-scheme`) eller `data-theme="light"` på `<html>`. Alt må fungere i begge.
3. Tekst minst 4,5:1 kontrast, UI-kanter og ikoner minst 3:1 (WCAG AA). Status (feil, suksess, advarsel) bæres av tekst eller ikon, ikke farge alene.
4. Hver interaktiv komponent har hvile, hover, fokus og deaktivert (opacity 0.4–0.5, `cursor: not-allowed`). Felt har i tillegg feil.
5. Fokus bruker `:focus-visible`. Knapper og lenker: `outline: 2px solid var(--color-accent-border)`, offset 2px. Felt og ghost-knapp: kant `--color-accent` pluss `box-shadow: 0 0 0 2px var(--color-focus-halo)`, ingen outline. Feilfelt: samme i `--color-error`.
6. Respekter `prefers-reduced-motion`. Overganger: `--t-fast` 0.15s (farge, kant), `--t-lift` 0.1s (1px løft på primærknapp). Ingen andre animasjoner uten behov.

## Tokens: hva brukes til hva

| Bruk | Token |
|---|---|
| Side / kort og dialog | `--color-bg` / `--color-surface` |
| Tekst / støttetekst / metadata og placeholder | `--color-text` / `--color-text-secondary` / `--color-text-muted` |
| Etikett i kort (uppercase, `xs`, 600, +0.07em) | `--color-label` |
| Aksent som **tekst**, lenke, kant på fokusert felt | `--color-accent` (hover `--color-accent-hover`). `--color-link` er alias, lenker er alltid understreket |
| Aksent som **flate** (primærknapp) | `--color-accent-fill` (hover `-fill-hover`) + `--color-on-accent` som tekst. Aldri `--color-accent` som bakgrunn |
| Kanter | `--color-border` (kort), `--color-border-subtle` (skiller, ikke på inputs), `--color-border-control` (inputs, 3:1), `--color-accent-border` (ghost, drop-sone, 3:1) |
| Status | `--color-error` / `-success` / `-warning` / `-info`, bakgrunn `--color-error-bg` osv. Tittel i `--color-text`, farge på kant og ikon |
| Skygge og bakgrunn | `--shadow-md` (dropdown, popover), `--shadow-lg` (dialog), `--color-overlay`. Ikke skygge på vanlige flater. Native `<dialog>`/popover trenger ikke z-index |
| Fonter | Fraunces `--font-display` (overskrifter), Inter `--font-body`, `--font-mono` (kode). Selvhostet i `fonts/`, ingen Google Fonts |
| Størrelser | `--text-xs/sm/base/lg/xl/2xl/3xl` = 0.75, 0.8125, 0.875, 1.0625, 1.35, 1.5, clamp(2, 5vw, 3) rem. Linjehøyde `--leading-tight` 1.2, `--leading-normal` 1.6 |
| Hierarki | h1 Fraunces 3xl/700 · h2 Fraunces xl/600 · h3 Inter lg/600 · h4 Inter base/600 · brødtekst `base` · støtte `sm` · etikett og bildetekst `xs` · nøkkeltall Fraunces `2xl` med `tabular-nums` |
| Avstand | `--space-1…7` = 4, 8, 12, 16, 24, 32, 48 px |
| Radius | `--r-sm` 4 · `--r-md` 6 (knapper) · `--r-lg` 8 (inputs) · `--r-xl` 10 (kort, dialog) |

Aksent har to roller fordi lys modus trenger mørk brun som tekst (`#8a5d00`), men beholder amber (`#ffbe0b`) på flater. `card` har 2px linje øverst og `table th` 1px linje under i dempet amber (`--color-accent-border`). Hold slike aksenter subtile.

## Logo og ikoner (`brand/`)

Merkevaren er en gul prikk: `#ffbe0b`, samme verdi som `--color-accent-fill`. Gult er en fast del av designspråket, så bruk aksentflaten og ikke en egen gul.

| Fil | Bruk |
|---|---|
| `brand/favicon.svg` | Fav-ikon i moderne nettlesere |
| `brand/favicon.ico` | Fallback (16, 32, 48 px) |
| `brand/apple-touch-icon.png` | iOS-hjemmeskjerm (180×180, prikk på mørk `--color-bg`, må være ugjennomsiktig) |

Legg i `<head>` (relative stier, tilpass til appens struktur):

```html
<link rel="icon" href="brand/favicon.ico" sizes="32x32">
<link rel="icon" href="brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="brand/apple-touch-icon.png">
```

Ikonfilene kan ikke lese CSS-variabler, så fargene er hardkodet. Endres `--color-accent-fill` eller mørk `--color-bg`, må ikonene lages på nytt (statisk sjekk feiler ellers). Ikke tegn en egen logo eller endre filene uten at eier sier fra. SVG-er skal være ekte vektor: ingen `<image>`, ingen `shape-rendering`, ingen eksterne `@import`/fonter (tekst som former), og `viewBox` uten faste `width`/`height`.

## Komponenter (ren CSS)

Last `tokens.css` og `components.css`, ingen byggesteg.

| Komponent | Klasser |
|---|---|
| Knapp | `btn-primary`, `btn-ghost`, `btn-danger` (fylt, bekreftelser), `btn-danger-link` |
| Felt | `field` > `label` + `input` / `select` / `textarea` + `hint` / `field-error` |
| Valg | `check` (checkbox, radio), `switch` på `input[type=checkbox][role=switch]` |
| Tabell | `table-wrap` (`tabindex="0" role="region" aria-label="…"`, fordi den scroller sidelengs) > `table`, `num` (tall), `table-empty`, `aria-sort` på `th` |
| Kort / sitat | `card` (`card-title`, `card-body`), `quote` |
| Dialog | `<dialog class="dialog">` med `dialog-title`, `-body`, `-actions`, åpnes med `showModal()` |
| Melding | `alert` + `success` / `warning` / `error`, `alert-icon`, `-title`, `-body` |
| Lasting | `spinner`, htmx-klassene `htmx-request`, `htmx-indicator`, `htmx-swapping` |
| Hjelp | `tnum`, `sr-only`, `h1`–`h4` |

- Feil på felt: `aria-invalid="true"` og `aria-describedby` til en `field-error`, ikke en egen klasse. Synlig `label`, placeholder erstatter den ikke.
- `color-scheme` er satt i `tokens.css`, så native kontroller følger modus.
- Mangler en komponent (tabs, paginering, meny)? Legg den til i `components.css` og guiden først, ikke lokalt i appen. Toast som lukker seg selv er bevisst utelatt (WCAG 2.2.1): bruk `role="status"`-meldingen.

### htmx-mønstre (testet mot htmx 2.0, Chromium, mørk og lys, axe 0 brudd)

- **Validering:** serveren returnerer hele skjemaet på nytt med `aria-invalid`, feilmelding og `autofocus` på første ugyldige felt.
- **Lasting:** `.spinner` i `.htmx-indicator`. Knappen blokkeres under `htmx-request`.
- **Beskjeder:** `<div id="status" role="status" aria-live="polite">` i layouten, oppdatert med `hx-swap-oob="innerHTML:#status"`. Ikke `"true"` (fjerner `role`).
- **Sortering:** bytt hele tabellen (så `aria-sort` oppdateres). Lenken har `id` og beholder fokus.
- **Sletting:** server-rendret `<dialog>` hentet med `hx-get` inn i en tom plass-div, åpnet med `hx-on::load="this.showModal()"`, fjernet ved `close`. `autofocus` på Avbryt. Bekreft-knappen lukker dialogen og flytter fokus til en overskrift med `tabindex="-1"` (raden og knappen er borte). Escape lukker og returnerer fokus til knappen. Krever at CSP tillater inline JS (`hx-on`).
- Ikke testet: paginering, `hx-boost`, View Transitions, dialog med serverside skjemavalidering.

## Norsk UI-tekst og formater

- Bokmål, kort og konkret, «du». `<html lang="nb">`. Aldri æ/ø/å som ae/oe/aa i UI-tekst.
- Store bokstaver kun i første ord og egennavn. Knapper: verb i imperativ med objekt («Lagre», «Legg til kunde»), ikke «OK» eller «Submit».
- Feilmelding: hva som skjedde og hva brukeren kan gjøre («Kunne ikke lagre. Prøv igjen.»), aldri «Feil!» alene. Tom tilstand: forklar og tilby én handling.
- Bruk `Intl` med `nb-NO`, aldri håndformatering. Mellomrom i tall og før `kr`/`%` er hardt mellomrom (U+00A0).

| Hva | Kode | Resultat |
|---|---|---|
| Dato | `new Intl.DateTimeFormat('nb-NO').format(d)` | `16.10.2026` |
| Lang dato / med tid | `{ dateStyle: 'long' }` / `{ dateStyle: 'short', timeStyle: 'short' }` | `16. oktober 2026` / `16.10.2026, 14:30` |
| Tall | `new Intl.NumberFormat('nb-NO').format(n)` | `1 234 567,891` |
| Beløp | `{ style: 'currency', currency: 'NOK' }` | `1 234,50 kr` (negativt `−1 234,50 kr`) |
| Prosent | `{ style: 'percent', maximumFractionDigits: 1 }` | `12,5 %` |
| Sortering | `a.localeCompare(b, 'nb')` | `A, Z, Æ, Ø, Å` |

## Ikke gjør

- Ikke bruk `--color-text-muted` til viktig informasjon, bare metadata og hjelpetekst.
- Ikke bruk `--color-border-subtle` på inputs (1,3:1). Bruk `--color-border-control`.
- Ikke bruk semantiske farger som tekst på tonet bakgrunn (`-bg`) i lys modus. Bruk `--color-text` og la fargen ligge på kant og ikon.
- Ikke finn på nye farger eller avstander. Foreslå dem i guiden først (`tokens.css` og `index.html`).
