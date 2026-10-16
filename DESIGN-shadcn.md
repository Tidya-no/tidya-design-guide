# Valgfritt: React med shadcn/ui

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
