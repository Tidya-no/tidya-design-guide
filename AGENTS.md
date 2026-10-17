# AGENTS.md

Instruksjoner for AI-agenter og utviklere som endrer dette repoet. Regler for *bruk* av designsystemet står i `DESIGN.md`. Denne filen handler om *endring* av det.

## Filer og hva som må holdes i takt

`tokens.css` er eneste kilde til verdier. Alt annet skal følge etter.

| Når du endrer | Må du også oppdatere / sjekke |
|---|---|
| Et token i `tokens.css` | Fargetabellen og kontrasttallene i `index.html`. Tokentabellen og tall i `DESIGN.md`. `README.md` hvis noe nevnes der |
| Lys modus i `tokens.css` | Lys modus er definert **to steder** (`@media (prefers-color-scheme: light)` og `:root[data-theme="light"]`). De må være identiske |
| Nytt eller fjernet token | Tabellen i `index.html` og `DESIGN.md`. Ingen ubrukte og ingen udokumenterte tokens |
| En klasse i `components.css` | Demo i `index.html` og omtale i `DESIGN.md`. Klasser som brukes i `index.html` må finnes i CSS, og motsatt |
| Guide-spesifikk stil i `styles.css` | Bare for selve guiden. Gjenbrukbare komponenter hører hjemme i `components.css` |
| En fil som skal publiseres | `pages.yml` (kopieringen til `_site`) og cache-busting-steget for CSS/JS |
| `--color-accent-fill`, `--color-text` (lys eller mørk) eller mørk `--color-bg` | Ikoner og logoer i `brand/` har fargene hardkodet og må lages på nytt. Logo-panelene i `styles.css` har `--color-bg` hardkodet. Statisk sjekk feiler ellers |
| En fil i `fonts/` eller `brand/` | «Kom i gang» i `DESIGN.md` skal nevne alle filene (statisk sjekk feiler ellers), og `pages.yml` må kopiere mappen |
| Et eksempel i `DESIGN.md` | Eksempelblokken testes i CI. Hold den i takt med komponentene |
| Et htmx-mønster | `DESIGN.md` (htmx-mønstre) og demo i `index.html` |

## Kontrastkrav

- Tekst: minst **4,5:1** (WCAG AA). UI-elementer og fokus: minst **3:1**.
- Kontrast regnes mot `--color-bg`, og mot `--color-surface` for innhold i kort.
- Amber (`--color-accent-fill`) kan aldri være tekst på lys bakgrunn (1,5:1). Bruk `--color-accent` til tekst og `--color-accent-fill` til flater.
- Tonet bakgrunn og hover: `--color-accent-bg-subtle` legges oppå bg/surface, og all tekstfarge må fortsatt ha 4,5:1 oppå den (verste tilfelle var feilfarge på surface).
- Regn ut kontrast etter ethvert fargebytte. Ikke anta.

## QA før du åpner PR

CI (`.github/workflows/kvalitet.yml`) kjører statisk konsistenssjekk (punkt 3), html-validate og axe (mørk/lys, 320/1100 px, med og uten åpen dialog). Det er minimum, ikke hele sjekken: tastatur, utseende og smal skjerm må du sjekke selv. Kjør lokalt:

1. **html-validate:** `html-validate -c .github/qa/htmlvalidate.json index.html` (0 feil).
2. **axe:** `node .github/qa/axe.cjs` (0 brudd). Test gjerne også 375 og 768 px.
3. **Krysssjekk:** `python3 .github/qa/statisk.py` (kjører også i CI). Sjekker at lysblokkene er identiske, at alle `var(--x)` er definert, at tokens og klasser er i bruk og dokumentert, at fargetabellen og kontrasttallene i `index.html` stemmer med `tokens.css`, at filreferanser og publisering henger sammen, og at kontrast (inkl. hover-tint) er over kravene. Tabellen i `index.html` må fortsatt oppdateres for hånd; scriptet sier fra hvis den driver.
4. **Eksemplene i `DESIGN.md`:** `node .github/qa/eksempler.cjs` (kjører også i CI). Henter html-blokken under «Eksempler» og kjører html-validate og axe på den.
5. **Tastatur:** tab gjennom guiden i begge moduser. Alle fokuserbare elementer skal ha synlig fokus (`:focus-visible`), også inne i dialogen.
6. **Visuelt:** ta skjermbilde i mørk, lys og 375 px. Se på det, ikke bare kjør verktøyene. Axe fanger ikke at noe ser blasst eller trangt ut.
7. **Smal skjerm:** ingen horisontal sidescroll (320 px). Tabeller og kodeblokker som scroller skal ha `tabindex="0"`, `role="region"` og `aria-label`.

Ved htmx-endringer: test mot en kjørende server, ikke bare statisk HTML (fokus etter swap, `aria-live`, validering, `aria-sort`).

## Regler for endringer

- Ingen nye avhengigheter, byggesteg eller `package.json`. Repoet er statisk. QA-verktøy installeres utenfor repoet (se `kvalitet.yml`).
- Hold det kort. Mer tekst og flere komponenter er ikke bedre. Fjern heller enn å legge til.
- Ikke commit midlertidige filer (skjermbilder, scratch-filer). `git status` før commit.
- Tabeller og tall i dokumentene skal være utregnet fra `tokens.css`, ikke skrevet fra hukommelsen.
- Logo og ikoner i `brand/` endres ikke uten at eier sier fra. SVG-er skal være ekte vektor (ingen `<image>`, `shape-rendering`, eksterne `@import` eller fonter, tekst som former, `viewBox` uten faste mål). Reglene står i `DESIGN.md`.
- UI-tekst er norsk bokmål med ordentlige æ, ø og å.
- Små endringer i én PR, med en kort beskrivelse av hva som er verifisert og hva som **ikke** er det (live-siden, Safari/Firefox, skjermleser).
- Merge først når CI er grønn og eieren ber om det.

## Kjente hull

- Ikke testet: Safari, Firefox, skjermleser, live github.io.
