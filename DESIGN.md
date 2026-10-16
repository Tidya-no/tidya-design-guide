# Tidya designsystem: regler for utvikling

Kort referanse for deg som bygger UI (menneske eller AI). Kilden til sannhet for verdier er `tokens.css`. Se `index.html` for visuelle eksempler.

## Grunnregler

1. Bruk alltid tokens (`var(--color-*)`, `var(--space-*)`, `var(--r-*)`). Aldri hardkodede farger, px-avstander eller radius.
2. Mørk modus er standard. Lys modus følger OS (`prefers-color-scheme`) eller `data-theme="light"` på `<html>`. Alt må fungere i begge.
3. Tekst skal ha minst 4,5:1 kontrast, UI-kanter og ikoner minst 3:1 (WCAG AA).
4. Status (feil, suksess, advarsel) skal alltid bæres av tekst eller ikon, ikke farge alene.
5. Respekter `prefers-reduced-motion`. Fokus bruker alltid `:focus-visible`-ringen: `2px solid var(--color-accent)`, offset 2px.

## Hvilken token til hva

| Bruk | Token |
|---|---|
| Sidebakgrunn / kort, modaler | `--color-bg` / `--color-surface` |
| Primærtekst / støttetekst / metadata | `--color-text` / `--color-text-secondary` / `--color-text-muted` |
| Etiketter og seksjonsoverskrifter i kort | `--color-label` (uppercase, 0.75rem, 600) |
| Aksent som **tekst**, lenke, fokusring | `--color-accent` (hover: `--color-accent-hover`) |
| Aksent som **flate** (primærknapp) | `--color-accent-fill` + `--color-on-accent` som tekst |
| Input- og kontrollkanter (min. 3:1) | `--color-border-control` |
| Dekorative skiller, kortkanter | `--color-border`, `--color-border-subtle`, `--color-border-medium` |
| Ghost-knapp og drop-sone kant | `--color-accent-border` / `--color-accent-border-dashed` |
| Feil / suksess / advarsel / info | `--color-error` / `-success` / `-warning` / `-info`, bakgrunn `-bg` |

Aksent har to roller fordi lys modus trenger mørk brun som tekst (`#8a5d00`), men beholder amber (`#ffbe0b`) på flater. Ikke bruk `--color-accent` som bakgrunn.

## Typografi

- Fraunces (`--font-display`) til display og overskrifter, Inter (`--font-body`) til alt annet. Selvhostet i `fonts/`. Ingen Google Fonts.
- Brødtekst 0.875rem / 1.6. Etikett 0.75rem, 600, uppercase, +0.07em.

## Avstand, radius og bevegelse

- Avstand: kun `--space-1…7` = 4, 8, 12, 16, 24, 32, 48 px.
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
}
```

Fallgruver:
- Tekst på `--destructive` skal være `--color-bg` (5,2:1+), ikke hvit. Hvit gir for lav kontrast mot den lyse røde i mørk modus.
- shadcn bruker `dark:`-klassen. Sett den i takt med `data-theme`, eller bruk `@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *))`.

## Ikke gjør

- Ikke bruk `--color-text-muted` eller `--color-text-placeholder` til viktig informasjon. De er laget for metadata og hjelpetekst.
- Ikke bruk `--color-border-subtle` på inputs (1,3:1). Bruk `--color-border-control`.
- Ikke bruk semantiske farger som tekst på tonet bakgrunn (`-bg`) i lys modus, bruk `--color-text` og la fargen ligge på kant og ikon.
- Ikke finn på nye farger eller avstander. Foreslå dem i guiden først (`tokens.css` og `index.html`).
