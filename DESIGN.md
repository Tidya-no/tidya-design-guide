# Tidya designsystem: regler for utvikling

Kort referanse for deg som bygger UI (menneske eller AI). Verdier: `tokens.css`. Komponenter: `components.css`. Eksempler: `index.html` ([live](https://tidya-no.github.io/tidya-design-guide/)). Bygget for server-rendret HTML med htmx (komponentene er ren CSS og fungerer også i React).

## Kom i gang

Kopier `tokens.css`, `components.css`, `fonts/` og `brand/` inn i appen, og følg reglene. Bruk bare tokens og klasser derfra.

- Hent filene fra repoet (https://github.com/Tidya-no/tidya-design-guide) eller fra den publiserte guiden (https://tidya-no.github.io/tidya-design-guide/). Ikke gjett innholdet.
- Hele mapper skal med: `fonts/` (`inter-latin-wght-normal.woff2`, `inter-latin-wght-italic.woff2`, `fraunces-latin-wght-normal.woff2`, `LICENSE-Inter.txt`, `LICENSE-Fraunces.txt`) og `brand/` (`logo-lys-bakgrunn.svg`, `logo-mork-bakgrunn.svg`, `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`).
- Hold `fonts/` ved siden av `tokens.css`, for fontene lastes med relativ sti. Flytter du dem, endre `url(...)` i `@font-face`.
- I `<head>` (ikon-taggene står under «Logo og ikoner»):

```html
<html lang="nb">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
```

- `index.html` i repoet bruker også en `styles.css`. Den er guidens egen, ikke kopier den. Overskrifter bruker klassene `h1`–`h4`; en `<h1>` uten klasse får ingen stil.
- Layout (container, toppbar) er appens eget ansvar. Minimum med tokens, lagt i appens egen CSS:

```css
body { padding-inline: var(--space-4); padding-block: var(--space-6); }
.page { max-width: 860px; margin: 0 auto; display: flex; flex-direction: column; gap: var(--space-6); }
```

- `<meta name="theme-color">` er valgfri og kan ikke bruke `var()`. Det er det eneste stedet hex er lov (unntak fra regel 1): `--color-bg` for mørk og lys modus: `#1c1712` (mørk) og `#fbf6ea` (lys).

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

Aksent har to roller fordi amber ikke kan være tekst på lys bakgrunn (derfor `#8a5d00` som tekst i lys modus). `card` har 2px linje øverst og `table th` 1px linje under i dempet amber (`--color-accent-border`). Hold slike aksenter subtile.

## Logo og ikoner (`brand/`)

Merkevaren er ordmerket «Tidya» med en gul prikk. Prikken er `#ffbe0b`, samme verdi som `--color-accent-fill`. Gult er en fast del av designspråket, så bruk aksentflaten og ikke en egen gul.

| Fil | Bruk |
|---|---|
| `brand/favicon.svg` | Fav-ikon i moderne nettlesere |
| `brand/favicon.ico` | Fallback (16, 32, 48 px) |
| `brand/apple-touch-icon.png` | iOS-hjemmeskjerm (180×180, prikk på mørk `--color-bg`, må være ugjennomsiktig) |

Logo: velg variant etter bakgrunn, ikke etter modus. `brand/logo-lys-bakgrunn.svg` er mørk logo for lys bakgrunn, `brand/logo-mork-bakgrunn.svg` er lys logo for mørk bakgrunn.

```html
<img src="brand/logo-lys-bakgrunn.svg" alt="Tidya" height="32">
```

Logo som følger modus (bytter ved `prefers-color-scheme` og `data-theme`, uten egen CSS):

```html
<div class="logo">
	<img class="logo-for-dark" src="brand/logo-mork-bakgrunn.svg" alt="Tidya" height="32">
	<img class="logo-for-light" src="brand/logo-lys-bakgrunn.svg" alt="Tidya" height="32">
</div>
```

Minstehøyde 24 px. Frirom minst prikkens diameter på alle sider. Ikke strekk, farge om, legg skygge eller legg logoen på bilder.

Ikoner: legg i `<head>` (relative stier, tilpass til appens struktur):

```html
<link rel="icon" href="brand/favicon.ico" sizes="32x32">
<link rel="icon" href="brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="brand/apple-touch-icon.png">
```

Ikonfilene kan ikke lese CSS-variabler, så fargene er hardkodet. Endres `--color-accent-fill`, `--color-text` eller mørk `--color-bg`, må ikoner og logoer lages på nytt (statisk sjekk feiler ellers). Ikke tegn en egen logo eller endre filene uten at eier sier fra. SVG-er skal være ekte vektor: ingen `<image>`, ingen `shape-rendering`, ingen eksterne `@import`/fonter (tekst som former), og `viewBox` uten faste `width`/`height`.

## Komponenter (ren CSS)

Last `tokens.css` og `components.css`, ingen byggesteg.

| Komponent | Klasser |
|---|---|
| Knapp | `btn-primary`, `btn-ghost`, `btn-danger` (fylt, bekreftelser), `btn-danger-link` |
| Felt | `field` > `<label class="label">` + `<input class="input">` / `<select class="select">` / `<textarea class="textarea">` + `hint` / `field-error` |
| Skjema | `stack` (vertikal avstand mellom felt, også i dialog) |
| Valg | `check` (checkbox, radio), `switch` på `input[type=checkbox][role=switch]` |
| Tabell | `table-wrap` (`tabindex="0" role="region" aria-label="…"`, fordi den scroller sidelengs; navnet må være unikt på siden, ikke det samme som seksjonens overskrift) > `<table class="table">`, `num` (tall), `table-empty`, `aria-sort` på `th` bare der sortering finnes |
| Kort / sitat | `card` (`card-title`, `card-body`), `quote` |
| Dialog | `<dialog class="dialog">` med `dialog-title`, `-body`, `-actions`, åpnes med `showModal()` |
| Melding | `alert` + `success` / `warning` / `error`, `alert-icon`, `-title`, `-body` |
| Lasting | `spinner`, htmx-klassene `htmx-request`, `htmx-indicator`, `htmx-swapping` |
| Hjelp | `tnum`, `sr-only`, `note` (liten forklarende tekst), `h1`–`h4` (klasser, `<h1>` uten klasse er ikke stilet) |
| Logo | `logo` med `logo-for-dark` og `logo-for-light` (se «Logo og ikoner») |

- Knappeklassene fungerer også på `<a>`: bruk `<a>` for navigasjon og `<button>` for handlinger.
- Én `btn-primary` per visning (hovedhandlingen), resten `btn-ghost`. Åpne-knapper og andre sekundære handlinger er `btn-ghost`, men den som åpner den viktigste dialogen på siden kan være `btn-primary`.
- Skjema i dialog: `<dialog class="dialog">` med `dialog-title`, `<form class="stack" method="dialog">` med feltene og `dialog-actions` nederst. `autofocus` på første felt, og Avbryt-knappen har `formnovalidate`. Se eksempelet i guiden.
- Status i en tabellcelle er ren tekst (status bæres ikke av farge alene). Det finnes ingen badge ennå.
- Feil på felt vises ved feltet (`field-error`). En `alert` er for resultatet av hele handlingen («Kunne ikke lagre. Prøv igjen.») og erstatter ikke feltfeilen. Suksess og andre beskjeder legges i `role="status"`-regionen (`#status`), også i statisk HTML.
- Feil på felt: `aria-invalid="true"` og `aria-describedby` til en `field-error`, ikke en egen klasse. Synlig `label`, placeholder erstatter den ikke.
- `color-scheme` er satt i `tokens.css`, så native kontroller følger modus.
- Mangler en komponent (tabs, paginering, meny)? Legg den til i `components.css` og guiden først, ikke lokalt i appen. Toast som lukker seg selv er bevisst utelatt (WCAG 2.2.1): bruk `role="status"`-meldingen.

### Eksempler (kopier og tilpass)

```html
<!-- Knapper -->
<button class="btn-primary" type="button">Lagre</button>
<button class="btn-ghost" type="button">Avbryt</button>
<!-- Lenke som knapp (navigasjon bruker <a>, ikke <button>) -->
<a class="btn-ghost" href="/kunder">Se kunder</a>

<!-- Felt med feil -->
<div class="field">
	<label class="label" for="epost">E-post</label>
	<input class="input" id="epost" name="epost" type="email" aria-invalid="true" aria-describedby="epost-feil">
	<p class="field-error" id="epost-feil">Ugyldig e-postadresse.</p>
</div>

<!-- Tabell (navnet i aria-label er unikt på siden) -->
<div class="table-wrap" tabindex="0" role="region" aria-label="Kundeliste">
	<table class="table">
		<caption class="sr-only">Kunder</caption>
		<thead><tr><th scope="col">Navn</th><th scope="col" class="num">Beløp</th></tr></thead>
		<tbody><tr><td>Fjordbris AS</td><td class="num">48&nbsp;500,00&nbsp;kr</td></tr></tbody>
	</table>
</div>

<!-- Kort og forklarende tekst -->
<div class="card"><p class="card-title">Tittel</p><p class="card-body">Innhold.</p></div>
<p class="note">Vises i oversikten.</p>

<!-- Melding i status-regionen -->
<div id="status" role="status" aria-live="polite">
	<div class="alert success"><span class="alert-icon" aria-hidden="true">✓</span><div><p class="alert-title">Lagret</p><p class="alert-body">Endringene er lagret.</p></div></div>
</div>

<!-- Bekreft-dialog -->
<dialog class="dialog" id="slett" aria-labelledby="slett-tittel" aria-describedby="slett-tekst">
	<h2 class="dialog-title" id="slett-tittel">Slette kunden?</h2>
	<p class="dialog-body" id="slett-tekst">Dette kan ikke angres.</p>
	<form class="dialog-actions" method="dialog">
		<button class="btn-ghost" value="avbryt" autofocus>Avbryt</button>
		<button class="btn-danger" value="slett">Slett kunde</button>
	</form>
</dialog>

<!-- Skjema i dialog -->
<dialog class="dialog" id="ny-kunde" aria-labelledby="ny-kunde-tittel">
	<h2 class="dialog-title" id="ny-kunde-tittel">Ny kunde</h2>
	<form class="stack" method="dialog">
		<div class="field"><label class="label" for="navn">Navn</label><input class="input" id="navn" name="navn" type="text" autofocus></div>
		<div class="dialog-actions">
			<button class="btn-ghost" value="avbryt" formnovalidate>Avbryt</button>
			<button class="btn-primary" value="lagre">Legg til kunde</button>
		</div>
	</form>
</dialog>
```

Åpne en dialog med `document.getElementById('id').showModal()`. Flere eksempler (valg, logo, htmx) står under og i guiden.

### htmx-mønstre (testet mot htmx 2.0, Chromium, mørk og lys, axe 0 brudd)

- **Validering:** serveren returnerer hele skjemaet på nytt med `aria-invalid`, feilmelding og `autofocus` på første ugyldige felt.
- **Lasting:** `.spinner` i `.htmx-indicator`. Knappen blokkeres under `htmx-request`.
- **Beskjeder:** `<div id="status" role="status" aria-live="polite">` i layouten, oppdatert med `hx-swap-oob="innerHTML:#status"`. Ikke `"true"` (fjerner `role`). Selve `alert` ligger inni `#status`.
- **Sortering:** bytt hele tabellen (så `aria-sort` oppdateres). Lenken har `id` og beholder fokus.
- **Sletting:** server-rendret `<dialog>` hentet med `hx-get` inn i en tom plass-div, åpnet med `hx-on::load="this.showModal()"`, fjernet ved `close`. `autofocus` på Avbryt. Bekreft-knappen lukker dialogen og flytter fokus til en overskrift med `tabindex="-1"` (raden og knappen er borte). Escape lukker og returnerer fokus til knappen. Krever at CSP tillater inline JS (`hx-on`).
- Ikke testet: paginering, `hx-boost`, View Transitions, dialog med serverside skjemavalidering.

## Norsk UI-tekst og formater

- Bokmål, kort og konkret, «du». `<html lang="nb">`. Aldri æ/ø/å som ae/oe/aa i UI-tekst.
- Store bokstaver kun i første ord og egennavn. Knapper: verb i imperativ med objekt («Lagre», «Legg til kunde»), ikke «OK» eller «Submit». Unntak: en knapp som bare åpner noe (dialog, side) kan være et substantiv som «Ny kunde».
- Feilmelding: hva som skjedde og hva brukeren kan gjøre («Kunne ikke lagre. Prøv igjen.»), aldri «Feil!» alene. Tom tilstand: forklar og tilby én handling.
- Bruk `Intl` med `nb-NO`, aldri håndformatering. Mellomrom i tall (også tusenskille) og før `kr`/`%` er hardt mellomrom (U+00A0). Beløp skrives med `kr` i UI, ikke «NOK». I statisk HTML skriver du `&nbsp;` mellom tall og enhet og ekte minustegn (`−`, U+2212) for hånd.

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
