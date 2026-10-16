# Tidya designsystem: regler for utvikling

Kort referanse for deg som bygger UI (menneske eller AI). Kilden til sannhet for verdier er `tokens.css`. Se `index.html` for visuelle eksempler.

## Grunnregler

1. Bruk alltid tokens (`var(--color-*)`, `var(--space-*)`, `var(--r-*)`). Aldri hardkodede farger, px-avstander eller radius.
2. Mørk modus er standard. Lys modus følger OS (`prefers-color-scheme`) eller `data-theme="light"` på `<html>`. Alt må fungere i begge.
3. Tekst skal ha minst 4,5:1 kontrast, UI-kanter og ikoner minst 3:1 (WCAG AA).
4. Status (feil, suksess, advarsel) skal alltid bæres av tekst eller ikon, ikke farge alene.
5. Respekter `prefers-reduced-motion`. Fokus bruker alltid `:focus-visible`. Primærknapp og lenker: `outline: 1px solid var(--color-accent-border)`, offset 1px (3:1). Felt og ghost-knapp: kanten skifter til `--color-accent`, ingen outline. Tynt og diskret, men fargeskiftet må alltid være synlig.

## Hvilken token til hva

| Bruk | Token |
|---|---|
| Sidebakgrunn / kort, modaler | `--color-bg` / `--color-surface` |
| Primærtekst / støttetekst / metadata | `--color-text` / `--color-text-secondary` / `--color-text-muted` |
| Etiketter og seksjonsoverskrifter i kort | `--color-label` (uppercase, 0.75rem, 600) |
| Lenke | `--color-link` (alias for `--color-accent`), alltid understreket, hover `--color-accent-hover` |
| Flytende elementer / bakgrunn bak dialog | `--shadow-sm/-md/-lg` / `--color-overlay` |
| Aksent som **tekst**, lenke, kant på fokusert felt | `--color-accent` (hover: `--color-accent-hover`) |
| Aksent som **flate** (primærknapp) | `--color-accent-fill` (hover `--color-accent-fill-hover`) + `--color-on-accent` som tekst |
| Input- og kontrollkanter (min. 3:1) | `--color-border-control` |
| Dekorative skiller, kortkanter | `--color-border`, `--color-border-subtle`, `--color-border-medium` |
| Ghost-knapp og drop-sone kant | `--color-accent-border` / `--color-accent-border-dashed` |
| Feil / suksess / advarsel / info | `--color-error` / `-success` / `-warning` / `-info`, bakgrunn `--color-error-bg` / `-success-bg` / `-warning-bg` / `-info-bg` |

Aksent har to roller fordi lys modus trenger mørk brun som tekst (`#8a5d00`), men beholder amber (`#ffbe0b`) på flater. Ikke bruk `--color-accent` som bakgrunn.

## Typografi

- Fraunces (`--font-display`) til display og overskrifter, Inter (`--font-body`) til alt annet. Selvhostet i `fonts/`. Ingen Google Fonts. Kode: `--font-mono`.
- Størrelser: kun `--text-xs/sm/base/lg/xl/2xl/3xl` (0.75, 0.8125, 0.875, 1.0625, 1.35, 1.5, clamp 2–3 rem). Linjehøyde `--leading-tight` 1.2 (overskrifter) og `--leading-normal` 1.6 (tekst).
- Hierarki: h1 Fraunces 3xl/700, h2 Fraunces xl/600, h3 Inter lg/600, h4 Inter base/600. Brødtekst `base`, støttetekst `sm`, etikett og bildetekst `xs`. Display (`2xl`, Fraunces 600) kun til nøkkeltall.
- Tall i tabeller og nøkkeltall: `font-variant-numeric: tabular-nums` (klassen `.tnum` i guiden).
- Etikett: 0.75rem, 600, uppercase, +0.07em.

## Lenker

`color: var(--color-link)` (= accent), alltid understreket (1px, offset 2px), hover `--color-accent-hover`. Fokus som andre elementer. Aldri lenke bare med farge.

## Dybde

- Flater skilles med `--color-surface` og kant, ikke skygge. Skygge kun på flytende elementer: `--shadow-sm` (sticky, hevet kort), `--shadow-md` (dropdown, popover, tooltip), `--shadow-lg` (dialog, toast).
- Dialog: `--color-surface`, kant `--color-border-subtle`, `--shadow-lg`, over `--color-overlay`.
- z-index: kun `--z-sticky` 10, `--z-dropdown` 20, `--z-overlay` 30, `--z-modal` 40, `--z-toast` 50.

## Norsk UI-tekst og formater

- Bokmål, kort og konkret, tiltal brukeren med «du». `<html lang="nb">`. Aldri æ/ø/å som ae/oe/aa i UI-tekst.
- Store bokstaver kun i første ord og egennavn (ikke Title Case). Knapper: verb i imperativ med objekt («Lagre», «Legg til kunde», «Slett utkast»), ikke «OK» eller «Submit».
- Feilmelding: si hva som skjedde og hva brukeren kan gjøre («Kunne ikke lagre. Prøv igjen.»). Aldri «Feil!» alene. Tom tilstand: forklar og tilby én handling.
- Formater bruker alltid `Intl` med `nb-NO`, aldri håndformatering:

| Hva | Kode | Resultat |
|---|---|---|
| Dato | `new Intl.DateTimeFormat('nb-NO').format(d)` | `16.10.2026` |
| Lang dato | `{ dateStyle: 'long' }` | `16. oktober 2026` |
| Dato og tid | `{ dateStyle: 'short', timeStyle: 'short' }` | `16.10.2026, 14:30` |
| Tall | `new Intl.NumberFormat('nb-NO').format(n)` | `1 234 567,891` |
| Beløp | `{ style: 'currency', currency: 'NOK' }` | `1 234,50 kr` (negativt: `−1 234,50 kr`) |
| Prosent | `{ style: 'percent', maximumFractionDigits: 1 }` | `12,5 %` |
| Sortering | `a.localeCompare(b, 'nb')` | `A, Z, Æ, Ø, Å` |

Mellomrommene i tall og før `kr`/`%` er hardt mellomrom (U+00A0). Ikke bytt dem med vanlig mellomrom.

## Avstand, radius og bevegelse

- Avstand: kun `--space-1…7` = `--space-1` 4, `-2` 8, `-3` 12, `-4` 16, `-5` 24, `-6` 32, `-7` 48 px.
- Radius: `--r-sm` 4 (små detaljer), `--r-md` 6 (knapper), `--r-lg` 8 (inputs), `--r-xl` 10 (kort/seksjoner).
- Overganger: `--t-fast` 0.15s (farge, kant), `--t-lift` 0.1s (1px løft på primærknapp). Ingen andre animasjoner uten behov.

## Tilstander

Hver interaktiv komponent skal ha hvile, hover, fokus og deaktivert (opacity 0.4–0.5, `cursor: not-allowed`). Felt har i tillegg feil: `aria-invalid="true"`, `--color-error` på kanten og feilmelding som tekst under feltet (`--color-error`, 12px).

## Bruk i shadcn/ui

Forutsetter Tailwind v4-oppsett der shadcn-variablene tar fulle fargeverdier (ikke `hsl(var(--x))`). Importer `tokens.css` og alias:

```css
:root {
	--background: var(--color-bg);
	--foreground: var(--color-text);
	--card: var(--color-surface);
	--card-foreground: var(--color-text);
	--popover: var(--color-surface);
	--popover-foreground: var(--color-text);
	--primary: var(--color-accent-fill);
	--primary-foreground: var(--color-on-accent);
	--secondary: var(--color-surface);
	--secondary-foreground: var(--color-text);
	--muted: var(--color-surface);
	--muted-foreground: var(--color-text-muted);
	--accent: var(--color-accent-bg-subtle);
	--accent-foreground: var(--color-text);
	--destructive: var(--color-error);
	--border: var(--color-border-subtle);
	--input: var(--color-border-control);
	--ring: var(--color-accent);
	--radius: var(--r-lg);

	/* Grafer: hue-spredning amber, blå, grønn, rød, tan. Alle min. 4,5:1 mot --color-bg */
	--chart-1: var(--color-accent);
	--chart-2: var(--color-info);
	--chart-3: var(--color-success);
	--chart-4: var(--color-error);
	--chart-5: var(--color-text-secondary);

	/* Sidebar */
	--sidebar: var(--color-surface);
	--sidebar-foreground: var(--color-text);
	--sidebar-primary: var(--color-accent-fill);
	--sidebar-primary-foreground: var(--color-on-accent);
	--sidebar-accent: var(--color-accent-bg-subtle);
	--sidebar-accent-foreground: var(--color-text);
	--sidebar-border: var(--color-border-subtle);
	--sidebar-ring: var(--color-accent);
}
```

Status-farger finnes ikke i shadcn. Tokenene heter allerede `--color-success` osv., så de kan ikke eksponeres som Tailwind-farger via `@theme` uten å skape en sirkulær referanse. Bruk dem med arbitrary values i `Alert`- og `Badge`-varianter:

```tsx
success: "border-[var(--color-success)] bg-[var(--color-success-bg)] text-foreground",
warning: "border-[var(--color-warning)] bg-[var(--color-warning-bg)] text-foreground",
info: "border-[var(--color-info)] bg-[var(--color-info-bg)] text-foreground",
```

Det gir samme utseende som meldingskomponenten i guiden: farge på kant og ikon, `--color-text` på teksten. (Vil du ha korte klasser som `bg-success`, må tokenene i `tokens.css` få et annet prefiks enn `--color-`.)

Oppsett i `globals.css`, i denne rekkefølgen:

```css
@import "tailwindcss";
@import "./tokens.css";

@custom-variant dark {
	&:where([data-theme="dark"], [data-theme="dark"] *) { @slot; }
	@media not (prefers-color-scheme: light) {
		&:where(:root:not([data-theme]), :root:not([data-theme]) *) { @slot; }
	}
}

/* :root-aliasene fra over */

@theme inline {
	--color-background: var(--background);
	--color-foreground: var(--foreground);
	--color-card: var(--card);
	--color-card-foreground: var(--card-foreground);
	--color-popover: var(--popover);
	--color-popover-foreground: var(--popover-foreground);
	--color-primary: var(--primary);
	--color-primary-foreground: var(--primary-foreground);
	--color-secondary: var(--secondary);
	--color-secondary-foreground: var(--secondary-foreground);
	--color-muted: var(--muted);
	--color-muted-foreground: var(--muted-foreground);
	--color-accent: var(--accent);
	--color-accent-foreground: var(--accent-foreground);
	--color-destructive: var(--destructive);
	--color-border: var(--border);
	--color-input: var(--input);
	--color-ring: var(--ring);
	--radius-sm: var(--r-sm);
	--radius-md: var(--r-md);
	--radius-lg: var(--r-lg);
	--radius-xl: var(--r-xl);
}

@layer base {
	* { @apply border-border outline-ring/50; }
	body { @apply bg-background text-foreground; }
}
```

Ikke la `shadcn init` skrive egne `oklch`-verdier over dette. Slett de genererte `:root`- og `.dark`-blokkene. Behold `@theme inline`, ellers finnes ikke `bg-primary`, `border-border` osv., og bygget feiler. Radius settes eksplisitt, ellers gir shadcns `calc(var(--radius) + 4px)` 12px på kort i stedet for 10px.

Testet (Tailwind 4.3, Vite 6, React 19, håndskrevne `Button`/`Input`/`Card` etter shadcn-mønsteret; `shadcn add` var ikke tilgjengelig i testmiljøet): bygget går gjennom, `bg-primary`, `text-muted-foreground`, `border-input` og `border-destructive` får riktige tokenverdier i begge moduser, radius blir 6/8/10px, og `data-theme` overstyrer OS-innstillingen. Ikke testet: `Dialog`, `Select`, `Tabs` og andre sammensatte komponenter, og `chart-*`/`sidebar-*` i faktiske komponenter.

Fallgruver:
- shadcns standard `@custom-variant dark (&:is(.dark *))` og varianten med bare `[data-theme="dark"]` gjør at `dark:` **ikke** slår til i standardtilstanden (mørk uten attributt), selv om siden er mørk. Bruk varianten over (testet i fire kombinasjoner av OS-modus og `data-theme`). Tokenene bytter selv, så bruk helst ikke `dark:` i egen kode.
- Tekst på `--destructive` skal være `--color-bg` (mørk 5,5:1, lys 5,2:1), ikke hvit. Endre `text-white` på destructive-variantene til `text-[var(--color-bg)]`.
- Fargevalget i `--chart-*` er ikke testet for fargeblindhet (rød/grønn). Grafer må ha direkte merking eller forklaring, ikke farge alene.

## Ikke gjør

- Ikke bruk `--color-text-muted` eller `--color-text-placeholder` til viktig informasjon. De er laget for metadata og hjelpetekst.
- Ikke bruk `--color-border-subtle` på inputs (1,3:1). Bruk `--color-border-control`.
- Ikke bruk semantiske farger som tekst på tonet bakgrunn (`-bg`) i lys modus, bruk `--color-text` og la fargen ligge på kant og ikon.
- Ikke finn på nye farger eller avstander. Foreslå dem i guiden først (`tokens.css` og `index.html`).
